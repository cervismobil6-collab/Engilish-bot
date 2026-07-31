"""
Dictionary handler
"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


async def show_dictionary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show dictionary menu"""
    text = """
📖 **LUG'AT**

Tematik lug'atlar:

👨 **Oila** - Oila a'zolari
🏫 **Maktab** - Maktab va o'quv vositalari
🍔 **Ovqat** - Taomlar va ichimliklar
🏥 **Sog'liq** - Kasallik va dori-darmonlar
✈️ **Sayohat** - Seyohatlash va transport
💼 **Ish** - Professional lexika
❤️ **Ifodalar** - Kundalik iboralar

Ro'yxatlardan birini tanlang:
    """
    
    keyboard = [
        [InlineKeyboardButton("👨 Oila", callback_data="dict_family")],
        [InlineKeyboardButton("🏫 Maktab", callback_data="dict_school")],
        [InlineKeyboardButton("🍔 Ovqat", callback_data="dict_food")],
        [InlineKeyboardButton("🏥 Sog'liq", callback_data="dict_health")],
        [InlineKeyboardButton("✈️ Sayohat", callback_data="dict_travel")],
        [InlineKeyboardButton("💼 Ish", callback_data="dict_work")],
        [InlineKeyboardButton("❤️ Ifodalar", callback_data="dict_expressions")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
