"""
Updated main.py with payment handlers
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, 
    ContextTypes, ConversationHandler, CallbackQueryHandler
)
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from config import config
from handlers import start, menu, courses, ai_tutor, dictionary, tests, profile, premium, admin, payment
from database.connection import init_db


async def post_init(application: Application) -> None:
    """Initialize bot data after setup"""
    logger.info("Bot initialized successfully!")
    try:
        await init_db()
        logger.info("Database initialized!")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the bot"""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Xatolik yuz berdi. Qayta urinib ko'ring."
        )


def main() -> None:
    """Start the bot"""
    # Get bot token
    token = config.TELEGRAM_BOT_TOKEN
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    # Create application
    application = Application.builder().token(token).post_init(post_init).build()
    
    # Premium conversation handler
    premium_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(payment.handle_premium_selection, pattern="^premium_")],
        states={
            payment.AWAITING_SCREENSHOT: [
                MessageHandler(filters.PHOTO, payment.receive_payment_screenshot),
                CallbackQueryHandler(payment.cancel_payment, pattern="^cancel_payment$")
            ]
        },
        fallbacks=[CommandHandler("cancel", menu.show_menu)]
    )
    
    application.add_handler(premium_conv_handler)
    
    # Admin payment handlers
    application.add_handler(CommandHandler("approve", payment.approve_payment))
    application.add_handler(CommandHandler("reject", payment.reject_payment))
    
    # Add handlers
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
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu.handle_message))
    application.add_handler(MessageHandler(filters.VOICE, ai_tutor.handle_voice))
    
    # Callback query handlers
    application.add_handler(CallbackQueryHandler(courses.handle_course_selection, pattern="^course_"))
    application.add_handler(CallbackQueryHandler(dictionary.handle_dictionary_selection, pattern="^dict_"))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info(f"Starting bot: @{config.BOT_USERNAME}")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
