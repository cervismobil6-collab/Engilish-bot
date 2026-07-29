import json
import random
from telebot import types
from database import add_points, update_streak

with open("data/tests.json", "r", encoding="utf-8") as f:
    TESTS = json.load(f)

# user_id -> {"questions": [...], "index": int, "correct": int}
active_sessions = {}

QUESTIONS_PER_ROUND = 5


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "📝 Testlar")
    def start_test(message):
        update_streak(message.from_user.id)
        questions = random.sample(TESTS, min(QUESTIONS_PER_ROUND, len(TESTS)))
        active_sessions[message.from_user.id] = {
            "questions": questions,
            "index": 0,
            "correct": 0,
        }
        send_question(message.chat.id, message.from_user.id)

    def send_question(chat_id, user_id):
        session = active_sessions.get(user_id)
        if session is None:
            return

        if session["index"] >= len(session["questions"]):
            finish_test(chat_id, user_id)
            return

        q = session["questions"][session["index"]]
        kb = types.InlineKeyboardMarkup()
        for i, option in enumerate(q["options"]):
            kb.add(types.InlineKeyboardButton(option, callback_data=f"ans_{i}"))

        bot.send_message(
            chat_id,
            f"❓ Savol {session['index'] + 1}/{len(session['questions'])}:\n\n{q['question']}",
            reply_markup=kb,
        )

    def finish_test(chat_id, user_id):
        session = active_sessions.pop(user_id, None)
        if session is None:
            return
        correct = session["correct"]
        total = len(session["questions"])
        points_earned = correct * 2
        add_points(user_id, points_earned)

        bot.send_message(
            chat_id,
            f"✅ Test yakunlandi!\n\n"
            f"To'g'ri javoblar: {correct}/{total}\n"
            f"Qo'shilgan ball: +{points_earned} 🏆"
        )

    @bot.callback_query_handler(func=lambda c: c.data.startswith("ans_"))
    def check_answer(call):
        user_id = call.from_user.id
        session = active_sessions.get(user_id)
        if session is None:
            bot.answer_callback_query(call.id, "Sessiya topilmadi, qaytadan boshlang.")
            return

        chosen = int(call.data.split("_")[1])
        q = session["questions"][session["index"]]

        if chosen == q["answer"]:
            session["correct"] += 1
            bot.answer_callback_query(call.id, "✅ To'g'ri!")
        else:
            correct_text = q["options"][q["answer"]]
            bot.answer_callback_query(call.id, f"❌ Xato! To'g'ri javob: {correct_text}")

        session["index"] += 1
        send_question(call.message.chat.id, user_id)
