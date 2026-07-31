#!/usr/bin/env python3
"""
English AI Academy Bot - Production Server
24/7 running with webhook support
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, ContextTypes
from telegram.error import TelegramError
from dotenv import load_dotenv
import asyncio
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging with file output
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from config import config
from handlers import start, menu, courses, ai_tutor, dictionary, tests, profile, admin, payment
from database.connection import init_db
from utils.scheduler import start_scheduler


class EnglishBotServer:
    """24/7 Bot Server Class"""
    
    def __init__(self):
        self.app = None
        self.is_running = False
    
    async def post_init(self, application: Application) -> None:
        """Initialize bot after setup"""
        logger.info("="*50)
        logger.info(f"🤖 Bot ishga tushirildi: @{config.BOT_USERNAME}")
        logger.info(f"⏰ Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"🌍 Muhit: {config.ENVIRONMENT}")
        logger.info("="*50)
        
        # Initialize database
        try:
            await init_db()
            logger.info("✅ Database tayyorlandi")
        except Exception as e:
            logger.error(f"❌ Database xatosi: {e}")
        
        self.is_running = True
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Global error handler"""
        logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)
        
        try:
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "❌ Xatolik yuz berdi. Qayta urinib ko'ring.\n/menu"
                )
        except TelegramError as e:
            logger.error(f"Failed to send error message: {e}")
    
    async def setup_handlers(self, application: Application) -> None:
        """Setup all handlers"""
        from telegram.ext import (
            CommandHandler, MessageHandler, filters,
            ConversationHandler, CallbackQueryHandler
        )
        
        # Premium conversation handler
        premium_conv = ConversationHandler(
            entry_points=[CallbackQueryHandler(payment.handle_premium_selection, pattern="^premium_")],
            states={
                payment.AWAITING_SCREENSHOT: [
                    MessageHandler(filters.PHOTO, payment.receive_payment_screenshot),
                    CallbackQueryHandler(payment.cancel_payment, pattern="^cancel_payment$")
                ]
            },
            fallbacks=[CommandHandler("cancel", menu.show_menu)]
        )
        
        application.add_handler(premium_conv)
        
        # Admin payment handlers
        application.add_handler(CommandHandler("approve", payment.approve_payment))
        application.add_handler(CommandHandler("reject", payment.reject_payment))
        
        # Command handlers
        application.add_handler(CommandHandler("start", start.start))
        application.add_handler(CommandHandler("menu", menu.show_menu))
        application.add_handler(CommandHandler("courses", courses.show_courses))
        application.add_handler(CommandHandler("ai_tutor", ai_tutor.ai_tutor_start))
        application.add_handler(CommandHandler("dictionary", dictionary.show_dictionary))
        application.add_handler(CommandHandler("tests", tests.show_tests))
        application.add_handler(CommandHandler("profile", profile.show_profile))
        application.add_handler(CommandHandler("premium", payment.show_premium))
        application.add_handler(CommandHandler("help", start.help_command))
        
        # Admin commands
        application.add_handler(CommandHandler("admin", admin.admin_panel))
        application.add_handler(CommandHandler("stats", admin.show_stats))
        application.add_handler(CommandHandler("broadcast", admin.broadcast_message))
        application.add_handler(CommandHandler("status", self.bot_status))
        
        # Message handlers
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu.handle_message))
        application.add_handler(MessageHandler(filters.VOICE, ai_tutor.handle_voice))
        
        # Callback handlers
        application.add_handler(CallbackQueryHandler(courses.handle_course_selection, pattern="^course_"))
        application.add_handler(CallbackQueryHandler(dictionary.handle_dictionary_selection, pattern="^dict_"))
        
        # Error handler
        application.add_error_handler(self.error_handler)
        
        logger.info("✅ Barcha handler'lar tayyorlandi")
    
    async def bot_status(self, update, context) -> None:
        """Check bot status"""
        uptime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status_text = f"""
✅ **BOT HOLATI**

🤖 Bot: Ishlamoqda ✅
⏰ Vaqt: {uptime}
🌍 Muhit: {config.ENVIRONMENT}
📊 Status: 24/7 ISHLAMOQDA
🔗 Webhook: {'Faol' if config.WEBHOOK_URL else 'O\'chirilgan'}
        """
        await update.message.reply_text(status_text)
    
    async def start_polling(self) -> None:
        """Start bot with polling"""
        logger.info("📡 Polling rezhimida ishga tushdirilyapti...")
        
        self.app = Application.builder() \
            .token(config.TELEGRAM_BOT_TOKEN) \
            .post_init(self.post_init) \
            .build()
        
        await self.setup_handlers(self.app)
        
        # Start scheduler for daily tasks
        # scheduler = start_scheduler()
        
        logger.info("🚀 Bot polling-da ishga tushirildi!")
        
        # Run with error handling
        try:
            await self.app.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
        except TelegramError as e:
            logger.error(f"Telegram xatosi: {e}")
            await asyncio.sleep(5)
            await self.start_polling()
        except Exception as e:
            logger.error(f"Xatolik: {e}")
            await asyncio.sleep(5)
            await self.start_polling()
    
    async def start_webhook(self) -> None:
        """Start bot with webhook (production)"""
        if not config.WEBHOOK_URL or not config.WEBHOOK_PORT:
            logger.error("❌ Webhook uchun URL va PORT kerak")
            await self.start_polling()
            return
        
        logger.info(f"🌐 Webhook rezhimida ishga tushdirilyapti...")
        logger.info(f"   URL: {config.WEBHOOK_URL}")
        logger.info(f"   Port: {config.WEBHOOK_PORT}")
        
        self.app = Application.builder() \
            .token(config.TELEGRAM_BOT_TOKEN) \
            .post_init(self.post_init) \
            .build()
        
        await self.setup_handlers(self.app)
        
        try:
            async with self.app:
                await self.app.bot.set_webhook(url=config.WEBHOOK_URL)
                logger.info("✅ Webhook o'rnatildi")
                
                # Run webhook server
                await self.app.start()
                logger.info("🚀 Webhook server ishga tushdi!")
                
                # Keep running
                while True:
                    await asyncio.sleep(1)
        
        except Exception as e:
            logger.error(f"Webhook xatosi: {e}")
            logger.info("🔄 Polling-ga o'tish...")
            await self.start_polling()


def main() -> None:
    """Main entry point"""
    token = config.TELEGRAM_BOT_TOKEN
    
    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN topilmadi!")
        return
    
    logger.info("🔥 English AI Academy Bot ISHGA TUSHIRILIMOQDA...")
    logger.info(f"🤖 Bot username: @{config.BOT_USERNAME}")
    logger.info(f"👤 Admin: @{config.ADMIN_USERNAME}")
    
    server = EnglishBotServer()
    
    # Choose mode: webhook (production) or polling (development)
    if config.ENVIRONMENT == "production" and config.WEBHOOK_URL:
        asyncio.run(server.start_webhook())
    else:
        asyncio.run(server.start_polling())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⛔ Bot to'xtatildi")
    except Exception as e:
        logger.critical(f"❌ KRITIK XATOLIK: {e}")
