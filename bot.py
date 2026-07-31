#!/usr/bin/env python3
"""
English AI Academy Bot - Simple Start Version
To'g'rilangan va soddalashtirigan versiya
"""

import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Get token from .env
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'engilishpromax_bot')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'jasurdos')

if not BOT_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN topilmadi! .env faylni tekshiring.")
    exit(1)

logger.info(f"✅ Bot token yuklandi")
logger.info(f"🤖 Bot username: @{BOT_USERNAME}")


class SimpleBot:
    """Oddiy va to'g'ri ishlaydi"""
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start command handler"""
        user = update.effective_user
        logger.info(f"👤 Yangi foydalanuvchi: {user.first_name} (@{user.username}) - ID: {user.id}")
        
        welcome_text = f"""
✅ Assalamu alaikum, {user.first_name}!

🎓 English AI Academy botga xush kelibsiz!

📚 Bu botda quyidagilar mavjud:
• 120 ta English darslar (6 daraja)
• 🤖 AI Ustoz - Ingliz tilida savol berishingiz mumkin
• 📖 Lug'at - So'zlar va iboralar
• 📝 Testlar - Bilimni tekshirish
• 👤 Profil - Progressing ko'rish
• 💳 Premium - Kurs va xususiyatlar

👇 Quyidagi tugmalardan foydalaning:
        """
        
        keyboard = [
            ['📚 Kurslar', '🤖 AI Ustoz'],
            ['📖 Lug\'at', '📝 Testlar'],
            ['👤 Profil', '💳 Premium'],
            ['/menu', '/help']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Main menu"""
        menu_text = """
📚 **ASOSIY MENYU**

Quyidagi variantlardan birini tanlang:
        """
        
        keyboard = [
            ['📚 Kurslar', '🤖 AI Ustoz'],
            ['📖 Lug\'at', '📝 Testlar'],
            ['👤 Profil', '💳 Premium'],
            ['⭐ Leaderboard', '❓ Yordam']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(menu_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Help command"""
        help_text = """
📖 **YORDAM**

🤖 **Bot buyruqlari:**
/start - Botni qayta boshlash
/menu - Asosiy menyu
/courses - Kurslarni ko'rish
/ai_tutor - AI Ustoz bilan gaplashish
/dictionary - Lug'atni ochish
/tests - Testlarni yechish
/profile - Profilni ko'rish
/premium - Premium rejalarni ko'rish
/help - Bu yordamni ko'rish

💬 **Tugmalardan foydalaning:**
Asosiy menyu tugmalaridan birini bosing yoki /menu dan foydalaning.

📞 **Muammo bo'lsa:**
Admin bilan bog'laning: @jasurdos
        """
        
        await update.message.reply_text(help_text)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle text messages"""
        text = update.message.text
        user_id = update.effective_user.id
        username = update.effective_user.username or "noma'lum"
        
        logger.info(f"💬 Xabar qabul qilindi: @{username} - {text}")
        
        # Handle button clicks
        if text == '📚 Kurslar':
            courses_text = """
📚 **KURSLAR**

6 ta daraja mavjud:
1️⃣ A1 - Boshlanuvchi (20 dars)
2️⃣ A2 - Boshlang'ich (20 dars)
3️⃣ B1 - O'rta (20 dars)
4️⃣ B2 - Yuqori o'rta (20 dars)
5️⃣ C1 - Yuqori (20 dars)

Jami: **120 dars**

Daralni boshlash uchun tanlang!
            """
            await update.message.reply_text(courses_text)
        
        elif text == '🤖 AI Ustoz':
            ai_text = """
🤖 **AI USTOZ**

English haqida har qanday savolni berishingiz mumkin:
✅ Grammatika tushuntirishlari
✅ Gaplarni tekshirish
✅ Yangi so'z o'rganish
✅ Telaffuz yordami
✅ IELTS imtihoniga tayyorlash

Savolog bering va men javob beraman!
            """
            await update.message.reply_text(ai_text)
        
        elif text == '📖 Lug\'at':
            dict_text = """
📖 **LUG'AT**

Tematik so'zlar va iboralar:
👨 Oila
🏫 Maktab
🍔 Ovqat
🏥 Sog'liq
✈️ Sayohat
💼 Ish
❤️ Ifodalar

Har biriga misollar va tarjima bilan!
            """
            await update.message.reply_text(dict_text)
        
        elif text == '📝 Testlar':
            tests_text = """
📝 **TESTLAR**

Har bir dars uchun 10 ta test savoli.

✅ Testni yechgandan keyin:
• Darhol natija ko'rasiz
• Xatolar haqida ma'lumot
• Ballar toplanadi
• Sertifikat olasiz
            """
            await update.message.reply_text(tests_text)
        
        elif text == '👤 Profil':
            profile_text = f"""
👤 **PROFIL**

📋 Ma'lumotlar:
• Foydalanuvchi ID: {user_id}
• Username: @{username}
• Daraja: A1
• Tugatilgan darslar: 0/120
• Streyk: 0 kun
• Coin'lar: 0 🪙

💳 Premium: Faol emas
            """
            await update.message.reply_text(profile_text)
        
        elif text == '💳 Premium':
            premium_text = """
💳 **PREMIUM REJALAR**

🥉 **1 OY**
   Narxi: 29,999 som
   ✅ Barcha darslar
   ✅ AI Ustoz cheksiz

🥈 **3 OY**
   Narxi: 79,999 som
   ✅ Barcha darslar
   ✅ Priority support

🥇 **UMRBOYI**
   Narxi: 299,000 som ⭐
   ✅ Barcha darslar
   ✅ Premium support
   ✅ Barcha yangilanishlar

💳 To'lov uchun:
Karta: 5614 6818 8730 1095
Holder: Gʻsniyev Sardorbek
            """
            await update.message.reply_text(premium_text)
        
        elif text == '⭐ Leaderboard':
            leaderboard_text = """
🏆 **LEADERBOARD - TOP 10**

1️⃣ Aziz - 450 points
2️⃣ Sara - 420 points
3️⃣ Ali - 390 points
4️⃣ Nozima - 360 points
5️⃣ Karim - 340 points
6️⃣ Fatima - 320 points
7️⃣ Shora - 300 points
8️⃣ Nadir - 280 points
9️⃣ Zarina - 260 points
🔟 Malik - 240 points

Siz hali leaderboard'da yo'qsiz.
Darslarni tugating va koʻproq balllar to'plang!
            """
            await update.message.reply_text(leaderboard_text)
        
        elif text == '❓ Yordam':
            await self.help_command(update, context)
        
        elif text == '/menu':
            await self.menu(update, context)
        
        elif text == '/help':
            await self.help_command(update, context)
        
        else:
            # Default response
            default_text = """
👋 Xabar qabul qilindi!

/menu - Menuga qaytish
/help - Yordam olish
            """
            await update.message.reply_text(default_text)
    
    async def error_handler(self, update, context):
        """Handle errors"""
        logger.error(f"❌ Xatolik: {context.error}")
        
        try:
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "❌ Xatolik yuz berdi!\n\n/menu - Menuga qaytish"
                )
        except Exception as e:
            logger.error(f"Error sending error message: {e}")
    
    def run(self):
        """Start the bot"""
        logger.info("="*60)
        logger.info("🚀 ENGLISH AI ACADEMY BOT ISHGA TUSHIRILMOQDA...")
        logger.info(f"🤖 Bot: @{BOT_USERNAME}")
        logger.info(f"👨 Admin: @{ADMIN_USERNAME}")
        logger.info("="*60)
        
        # Create application
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("menu", self.menu))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("courses", lambda u, c: self.handle_message(
            update=u, context=c
        ) if hasattr(u, 'message') else None))
        
        # Message handler (must be last)
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        app.add_error_handler(self.error_handler)
        
        logger.info("✅ Barcha handler'lar tayyorlandi")
        logger.info("📡 Bot ishga tushirildi (polling rejasida)")
        logger.info("⏸️  To'xtatish uchun: Ctrl+C\n")
        
        # Start polling
        app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    try:
        bot = SimpleBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("\n⏹️  Bot to'xtatildi (Ctrl+C)")
    except Exception as e:
        logger.error(f"💥 KRITIK XATOLIK: {e}")
        import traceback
        traceback.print_exc()
