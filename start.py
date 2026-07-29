from telebot import types
from database import get_or_create_user, update_streak
from config import ADMIN_IDS


def get_main_menu(user_id=None):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton("📚 So'zlar"),
        types.KeyboardButton("📝 Testlar"),
        types.KeyboardButton("📖 Grammar"),
        types.KeyboardButton("🗣 Speaking"),
        types.KeyboardButton("🎯 IELTS"),
        types.KeyboardButton("🤖 AI"),
        types.KeyboardButton("🏆 Reyting"),
        types.KeyboardButton("👤 Profil"),
        types.KeyboardButton("❤️ Favorite"),
    )
    if user_id in ADMIN_IDS:
        kb.add(types.KeyboardButton("👨‍💼 Admin panel"))
    return kb


def register(bot):
    @bot.message_handler(commands=["start"])
    def start_handler(message):
        user = message.from_user
        get_or_create_user(user.id, user.username or "", user.full_name)
        update_streak(user.id)

        text = (
            f"Assalomu alaykum, {user.first_name}! 👋\n\n"
            "Bu bot orqali ingliz tilini professional darajada o'rganasiz:\n\n"
            "📚 10000+ so'z\n"
            "📝 5000+ test\n"
            "📖 Grammar\n"
            "🗣 Speaking\n"
            "🎯 IELTS\n"
            "🤖 AI yordamchi\n\n"
            "Quyidagi menyudan bo'limni tanlang 👇"
        )
        bot.send_message(message.chat.id, text, reply_markup=get_main_menu(user.id))

    @bot.message_handler(commands=["help"])
    def help_handler(message):
        bot.send_message(
            message.chat.id,
            "Yordam kerak bo'lsa /start ni bosing va menyudan kerakli bo'limni tanlang."
        )
