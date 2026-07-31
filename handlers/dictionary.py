"""
Updated dictionary handler with callback support
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
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text, reply_markup=reply_markup)


async def handle_dictionary_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle dictionary category selection"""
    query = update.callback_query
    await query.answer()
    
    category = query.data.replace('dict_', '').upper()
    
    category_names = {
        'FAMILY': 'Oila',
        'SCHOOL': 'Maktab',
        'FOOD': 'Ovqat',
        'HEALTH': 'Sog\'liq',
        'TRAVEL': 'Sayohat',
        'WORK': 'Ish',
        'EXPRESSIONS': 'Ifodalar'
    }
    
    text = f"""
📚 **{category_names.get(category, category)}**

Bu kategoriya bo'yicha so'z va iboralari:

🔸 English translation
🔹 Uzbek tarjimasi
🎯 Pronunciation
📝 Misollar

⏳ So'zlar yuklanmoqda...
    """
    
    keyboard = [
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_dict")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)
