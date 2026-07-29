import json
import random
from telebot import types
from database import add_points, add_favorite, update_streak

with open("data/words.json", "r", encoding="utf-8") as f:
    WORDS = json.load(f)


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "📚 So'zlar")
    def send_word(message):
        update_streak(message.from_user.id)
        word = random.choice(WORDS)

        text = (
            f"🇬🇧 <b>{word['en']}</b>\n"
            f"🇺🇿 {word['uz']}\n\n"
            f"💬 <i>{word['example']}</i>"
        )

        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(
                "❤️ Saqlash", callback_data=f"fav_{word['en']}_{word['uz']}"
            ),
            types.InlineKeyboardButton("🔄 Keyingi so'z", callback_data="next_word"),
        )

        bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "next_word")
    def next_word(call):
        send_word(call.message)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data.startswith("fav_"))
    def save_favorite(call):
        _, en, uz = call.data.split("_", 2)
        add_favorite(call.from_user.id, en, uz)
        add_points(call.from_user.id, 1)
        bot.answer_callback_query(call.id, "❤️ Saqlandi! (+1 ball)")
