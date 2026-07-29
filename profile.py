from database import get_user_stats, get_favorites, update_streak


def level_from_points(points):
    if points < 20:
        return "🌱 Beginner"
    elif points < 60:
        return "📘 Elementary"
    elif points < 150:
        return "📗 Intermediate"
    elif points < 300:
        return "📙 Upper-Intermediate"
    else:
        return "🏆 Advanced"


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "👤 Profil")
    def show_profile(message):
        update_streak(message.from_user.id)
        user = get_user_stats(message.from_user.id)
        favorites_count = len(get_favorites(message.from_user.id))

        if user is None:
            bot.send_message(message.chat.id, "Iltimos avval /start bosing.")
            return

        text = (
            f"👤 <b>Profil</b>\n\n"
            f"Ism: {user['full_name']}\n"
            f"🏆 Ball: {user['points']}\n"
            f"📊 Daraja: {level_from_points(user['points'])}\n"
            f"🔥 Daily streak: {user['streak']} kun\n"
            f"❤️ Saqlangan so'zlar: {favorites_count}"
        )
        bot.send_message(message.chat.id, text, parse_mode="HTML")
