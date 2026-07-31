"""
Courses handler
"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


async def show_courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show available courses"""
    text = """
📚 **KURSLAR**

6 ta daraja mavjud:

1️⃣ **A1 - Beginner** (Boshlanuvchi)
   • 20 dars
   • Asosiy frazeologiya

2️⃣ **A2 - Elementary** (Boshlang'ich)
   • 20 dars
   • Kundalik suhbat

3️⃣ **B1 - Intermediate** (O'rta)
   • 20 dars
   • Murakkab mavzular

4️⃣ **B2 - Upper-Intermediate** (Yuqori o'rta)
   • 20 dars
   • Professional English

5️⃣ **C1 - Advanced** (Yuqori)
   • 20 dars
   • Chuqur bilim

Jami: **120 dars**

Daralni tanlang:
    """
    
    keyboard = [
        [InlineKeyboardButton("🔵 A1 - Boshlanuvchi", callback_data="course_a1")],
        [InlineKeyboardButton("🟢 A2 - Boshlang'ich", callback_data="course_a2")],
        [InlineKeyboardButton("🟡 B1 - O'rta", callback_data="course_b1")],
        [InlineKeyboardButton("🟠 B2 - Yuqori o'rta", callback_data="course_b2")],
        [InlineKeyboardButton("🔴 C1 - Yuqori", callback_data="course_c1")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
