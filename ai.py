import requests
from database import update_streak
from config import ANTHROPIC_API_KEY

WAITING_FOR_AI = set()


def ask_claude(prompt: str) -> str:
    """Anthropic API orqali javob oladi. API kalit sozlanmagan bo'lsa xabar qaytaradi."""
    if not ANTHROPIC_API_KEY:
        return "⚠️ AI funksiyasi hali sozlanmagan (ANTHROPIC_API_KEY kiritilmagan)."

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        data = response.json()
        return data["content"][0]["text"]
    except Exception as e:
        return f"❌ AI bilan bog'lanishda xatolik: {e}"


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "🤖 AI")
    def ai_intro(message):
        update_streak(message.from_user.id)
        WAITING_FOR_AI.add(message.from_user.id)
        bot.send_message(
            message.chat.id,
            "🤖 <b>AI yordamchi</b>\n\n"
            "Ingliz tili bo'yicha istalgan savolingizni yozing "
            "(grammatika, so'z ma'nosi, gap tuzish va h.k.)",
            parse_mode="HTML",
        )

    @bot.message_handler(func=lambda m: m.from_user.id in WAITING_FOR_AI and not m.text.startswith("/"))
    def ai_chat(message):
        # Boshqa menyu tugmalari bilan chalkashmasligi uchun tekshiruv
        menu_buttons = {
            "📚 So'zlar", "📝 Testlar", "📖 Grammar", "🗣 Speaking",
            "🎯 IELTS", "🤖 AI", "🏆 Reyting", "👤 Profil", "❤️ Favorite"
        }
        if message.text in menu_buttons:
            return

        bot.send_chat_action(message.chat.id, "typing")
        answer = ask_claude(
            f"Sen ingliz tili o'qituvchisisan. O'zbek tilida, tushunarli va qisqa javob ber. "
            f"Talabaning savoli: {message.text}"
        )
        bot.send_message(message.chat.id, answer)
