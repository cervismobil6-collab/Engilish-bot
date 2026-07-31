"""
AI Tutor handler
"""

from telegram import Update
from telegram.ext import ContextTypes
from ai.openai_service import ask_ai_tutor


async def ai_tutor_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start AI tutor conversation"""
    text = """
🤖 **AI USTOZ**

English haqida har qanday savolni berishingiz mumkin:

✅ Grammatika tushuntirishlari
✅ Gaplarni tekshirish
✅ Yangi so'z o'rganish
✅ Telaffuz yordami
✅ IELTS imtihoniga tayyorlash

Savolog bering va men javob beraman!
    """
    await update.message.reply_text(text)
    context.user_data['mode'] = 'ai_tutor'


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle voice messages for AI tutor"""
    await update.message.reply_text(
        "🎙️ Ovozli xabar qabul qilindi. Tekshtirilmoqda..."
    )
    # TODO: Implement speech-to-text conversion
