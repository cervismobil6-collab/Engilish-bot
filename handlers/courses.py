"""
Updated courses handler with callback support
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
        [InlineKeyboardButton("🟡 A2 - Boshlang'ich", callback_data="course_a2")],
        [InlineKeyboardButton("🟠 B1 - O'rta", callback_data="course_b1")],
        [InlineKeyboardButton("🔴 B2 - Yuqori o'rta", callback_data="course_b2")],
        [InlineKeyboardButton("⚫ C1 - Yuqori", callback_data="course_c1")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text, reply_markup=reply_markup)


async def handle_course_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle course selection from callback button"""
    query = update.callback_query
    await query.answer()
    
    level = query.data.replace('course_', '').upper()
    
    course_details = {
        'A1': 'Boshlanuvchi',
        'A2': 'Boshlang\'ich',
        'B1': 'O\'rta',
        'B2': 'Yuqori o\'rta',
        'C1': 'Yuqori'
    }
    
    text = f"""
📖 **{level} - {course_details.get(level, 'Noma\'lum')}**

Bu kursda quyidagilar mavjud:
✅ 20 ta to'liq dars
✅ Har darsda nazariyaviy asoslar
✅ Amaliy misollar
✅ 10 ta test savoli
✅ Performance analytics

🎓 Ushbu daraja tugallangandan keyin siz o'z darajani oshira olasiz.

📝 Darslarni boshlash uchun "Boshlash" tugmasini bosing yoki /menu dan foydalaning.
    """
    
    keyboard = [
        [InlineKeyboardButton("🚀 Boshlash", callback_data=f"start_course_{level}")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_courses")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)
