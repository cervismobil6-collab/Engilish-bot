import json
from telebot import types

with open("data/grammar.json", "r", encoding="utf-8") as f:
    GRAMMAR = json.load(f)


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "📖 Grammar")
    def grammar_menu(message):
        kb = types.InlineKeyboardMarkup()
        for i, topic in enumerate(GRAMMAR):
            kb.add(types.InlineKeyboardButton(topic["title"], callback_data=f"gr_{i}"))
        bot.send_message(message.chat.id, "📖 Mavzuni tanlang:", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data.startswith("gr_"))
    def show_grammar(call):
        index = int(call.data.split("_")[1])
        topic = GRAMMAR[index]
        text = f"📖 <b>{topic['title']}</b>\n\n{topic['explanation']}"
        bot.send_message(call.message.chat.id, text, parse_mode="HTML")
        bot.answer_callback_query(call.id)
