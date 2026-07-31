#!/usr/bin/env python3
"""
English AI Academy Bot - Main entry point
A comprehensive AI-powered Telegram bot for learning English
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
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
from handlers import start, menu, courses, ai_tutor, dictionary, tests, profile, premium, admin
from database.connection import init_db


async def post_init(application: Application) -> None:
    """Initialize bot data after setup"""
    logger.info("Bot initialized successfully!")
    await init_db()
    logger.info("Database initialized!")


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
    
    # Add handlers
    # Command handlers
    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("menu", menu.show_menu))
    application.add_handler(CommandHandler("courses", courses.show_courses))
    application.add_handler(CommandHandler("ai_tutor", ai_tutor.ai_tutor_start))
    application.add_handler(CommandHandler("dictionary", dictionary.show_dictionary))
    application.add_handler(CommandHandler("tests", tests.show_tests))
    application.add_handler(CommandHandler("profile", profile.show_profile))
    application.add_handler(CommandHandler("premium", premium.show_premium))
    application.add_handler(CommandHandler("help", start.help_command))
    
    # Admin commands
    application.add_handler(CommandHandler("admin", admin.admin_panel))
    application.add_handler(CommandHandler("stats", admin.show_stats))
    application.add_handler(CommandHandler("broadcast", admin.broadcast_message))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu.handle_message))
    application.add_handler(MessageHandler(filters.VOICE, ai_tutor.handle_voice))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info(f"Starting bot: @{config.BOT_USERNAME}")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
