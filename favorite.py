from database import get_favorites, update_streak


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "❤️ Favorite")
    def show_favorites(message):
        update_streak(message.from_user.id)
        favorites = get_favorites(message.from_user.id)

        if not favorites:
            bot.send_message(
                message.chat.id,
                "❤️ Hali saqlangan so'zlar yo'q.\n"
                "📚 So'zlar bo'limida so'zni saqlash uchun ❤️ tugmasini bosing."
            )
            return

        lines = ["❤️ <b>Saqlangan so'zlaringiz:</b>\n"]
        for word in favorites:
            lines.append(f"🇬🇧 {word['word_en']} — 🇺🇿 {word['word_uz']}")

        bot.send_message(message.chat.id, "\n".join(lines), parse_mode="HTML")
