from telebot import types
from config import ADMIN_IDS
from database import get_total_users, get_all_user_ids

WAITING_FOR_BROADCAST = set()


def is_admin(user_id):
    return user_id in ADMIN_IDS


def register(bot):
    @bot.message_handler(commands=["admin"])
    @bot.message_handler(func=lambda m: m.text == "👨‍💼 Admin panel")
    def admin_panel(message):

        if not is_admin(message.from_user.id):
            bot.send_message(message.chat.id, "⛔ Sizda admin huquqi yo'q.")
            return

        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("📊 Statistika", callback_data="admin_stats"),
            types.InlineKeyboardButton("📢 Xabar yuborish", callback_data="admin_broadcast"),
        )
        bot.send_message(message.chat.id, "👨‍💼 Admin panel", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "admin_stats")
    def admin_stats(call):
        if not is_admin(call.from_user.id):
            return
        total = get_total_users()
        bot.send_message(call.message.chat.id, f"📊 Jami foydalanuvchilar: {total}")
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data == "admin_broadcast")
    def ask_broadcast(call):
        if not is_admin(call.from_user.id):
            return
        WAITING_FOR_BROADCAST.add(call.from_user.id)
        bot.send_message(call.message.chat.id, "✉️ Barcha foydalanuvchilarga yuboriladigan xabarni kiriting:")
        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda m: m.from_user.id in WAITING_FOR_BROADCAST)
    def send_broadcast(message):
        WAITING_FOR_BROADCAST.discard(message.from_user.id)
        user_ids = get_all_user_ids()
        sent, failed = 0, 0

        for uid in user_ids:
            try:
                bot.send_message(uid, f"📢 {message.text}")
                sent += 1
            except Exception:
                failed += 1

        bot.send_message(
            message.chat.id,
            f"✅ Xabar yuborildi.\nMuvaffaqiyatli: {sent}\nXato: {failed}"
        )
