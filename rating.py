from database import get_top_users, update_streak


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "🏆 Reyting")
    def show_rating(message):
        update_streak(message.from_user.id)
        top_users = get_top_users(10)

        if not top_users:
            bot.send_message(message.chat.id, "Hozircha reyting bo'sh.")
            return

        medals = ["🥇", "🥈", "🥉"]
        lines = ["🏆 <b>TOP-10 reyting</b>\n"]
        for i, user in enumerate(top_users):
            prefix = medals[i] if i < 3 else f"{i + 1}."
            name = user["full_name"] or "Foydalanuvchi"
            lines.append(f"{prefix} {name} — {user['points']} ball")

        bot.send_message(message.chat.id, "\n".join(lines), parse_mode="HTML")
