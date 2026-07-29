import logging
import telebot

from config import BOT_TOKEN
from database import init_db

from handlers import start, words, tests, grammar, speaking, ielts, ai, rating, profile, favorite, admin

# --- Loglash sozlamalari ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# --- Bot obyektini yaratish ---
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# --- Ma'lumotlar bazasini tayyorlash ---
init_db()

# --- Barcha modullarni ro'yxatdan o'tkazish ---
start.register(bot)
words.register(bot)
tests.register(bot)
grammar.register(bot)
speaking.register(bot)
ielts.register(bot)
ai.register(bot)
rating.register(bot)
profile.register(bot)
favorite.register(bot)
admin.register(bot)

if __name__ == "__main__":
    logger.info("Bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True)
