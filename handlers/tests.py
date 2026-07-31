"""
Tests handler
"""

from telegram import Update
from telegram.ext import ContextTypes


async def show_tests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show tests menu"""
    text = """
📝 **TESTLAR**

Har bir dars uchun 10 ta test savoli mavjud.

Testlarni yechish orqali:
✅ O'z bilimingizni tekshirasiz
✅ Xatolarni tezda tapirasiz
✅ Balliar toplanasiz
✅ Sertifikat olasiz

Darsni tanlang va testni boshlang:
    """
    await update.message.reply_text(text)
