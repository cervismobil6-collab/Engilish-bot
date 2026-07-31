"""
Start command handler
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.queries import get_or_create_user, get_user_stats


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    
    # Get or create user in database
    await get_or_create_user({
        'telegram_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    })
    
    welcome_text = f"""
👋 Assalamu alaikum, {user.first_name}!

🎓 English AI Academy ga xush kelibsiz!

📚 Bu yerda siz:
• 120 ta dars bilan 6 daraja o'rganishingiz mumkin
• 🤖 AI Ustoz bilan savollarni berishingiz mumkin
• 📖 Lug'at va misollardan foydalanishingiz mumkin
• 📝 Testlar yechishingiz mumkin
• 👑 Premium xizmatdan foydalanishingiz mumkin

Boshlash uchun /menu tugmasini bosing yoki quyidagi tugmalardan foydalaning.
    """
    
    keyboard = [
        ['📚 Kurslar', '🤖 AI Ustoz'],
        ['📖 Lug\'at', '📝 Testlar'],
        ['👤 Profil', '💳 Premium']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = """
📖 **YORDAM**

🎯 **Asosiy buyruqlar:**
/start - Botni qayta boshlash
/menu - Asosiy menyu
/courses - Kurslarni ko'rish
/ai_tutor - AI Ustoz bilan gaplashish
/dictionary - Lug'atni ochish
/tests - Testlarni yechish
/profile - Profilni ko'rish
/premium - Premium rejalarni ko'rish
/help - Bu yordamni ko'rish

👨‍💼 **Admin buyruqlar:**
/admin - Admin paneli
/stats - Statistika
/broadcast - Xabar yuborish

❓ **Savolllar:**
Har qanday savol yoki muammo bo'lsa, admin bilan bog'laning: @jasurdos
    """
    await update.message.reply_text(help_text)
