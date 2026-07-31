"""
Main menu handler
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show main menu"""
    menu_text = """
📚 **ASOSIY MENYU**

Quyidagi variantlardan birini tanlang:
    """
    
    keyboard = [
        ['📚 Kurslar', '🤖 AI Ustoz'],
        ['📖 Lug\'at', '📝 Testlar'],
        ['👤 Profil', '💳 Premium'],
        ['🏆 Leaderboard', '⚙️ Sozlamalar']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(menu_text, reply_markup=reply_markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages"""
    text = update.message.text
    
    if text == '📚 Kurslar':
        from . import courses
        await courses.show_courses(update, context)
    elif text == '🤖 AI Ustoz':
        from . import ai_tutor
        await ai_tutor.ai_tutor_start(update, context)
    elif text == '📖 Lug\'at':
        from . import dictionary
        await dictionary.show_dictionary(update, context)
    elif text == '📝 Testlar':
        from . import tests
        await tests.show_tests(update, context)
    elif text == '👤 Profil':
        from . import profile
        await profile.show_profile(update, context)
    elif text == '💳 Premium':
        from . import premium
        await premium.show_premium(update, context)
    else:
        await update.message.reply_text(
            "Kechirasiz, bu buyriqni tushunmadim. /menu buyrug'ini bosing."
        )
