from database import add_points, update_streak
from handlers.ai import ask_claude

WAITING_FOR_ESSAY = set()

IELTS_TOPICS = [
    "Some people think technology has made our lives easier, while others believe it has "
    "made life more complicated. Discuss both views and give your opinion.",
    "Many people believe that university education should be free for everyone. "
    "To what extent do you agree or disagree?",
    "Some people prefer to live in a big city, while others prefer a small town. "
    "Discuss the advantages and disadvantages of each.",
]


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "🎯 IELTS")
    def ielts_menu(message):
        update_streak(message.from_user.id)
        import random
        topic = random.choice(IELTS_TOPICS)
        WAITING_FOR_ESSAY.add(message.from_user.id)
        bot.send_message(
            message.chat.id,
            "🎯 <b>IELTS Writing Task 2</b>\n\n"
            f"Mavzu:\n<i>{topic}</i>\n\n"
            "Kamida 250 so'zdan iborat insho yozib yuboring. "
            "AI uni baholab, tavsiya beradi.",
            parse_mode="HTML",
        )

    @bot.message_handler(func=lambda m: m.from_user.id in WAITING_FOR_ESSAY and len(m.text.split()) > 30)
    def check_essay(message):
        WAITING_FOR_ESSAY.discard(message.from_user.id)
        bot.send_chat_action(message.chat.id, "typing")

        feedback = ask_claude(
            "Sen IELTS examinerisan. Quyidagi Writing Task 2 insho matnini IELTS mezonlari "
            "(Task Response, Coherence, Lexical Resource, Grammar) bo'yicha baholab, "
            "taxminiy band ball (1-9) va o'zbek tilida 4-5 gaplik qisqa tavsiya yoz.\n\n"
            f"Insho matni:\n{message.text}"
        )
        bot.send_message(message.chat.id, f"📊 Baholash natijasi:\n\n{feedback}")
        add_points(message.from_user.id, 5)
