"""
Decorators for handlers
"""

import logging
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config import config

logger = logging.getLogger(__name__)


def admin_only(func):
    """Decorator to restrict command to admin only"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        
        # Check if user is admin
        if user.username != config.ADMIN_USERNAME:
            logger.warning(f"Unauthorized admin attempt by {user.username} ({user.id})")
            await update.message.reply_text(
                "❌ Siz admin emassiz! Ushbu buyruq faqat adminga ruxsat berilgan."
            )
            return
        
        return await func(update, context, *args, **kwargs)
    
    return wrapper


def premium_only(func):
    """Decorator to restrict command to premium users only"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        from database.queries import get_user_stats
        
        user_id = update.effective_user.id
        stats = await get_user_stats(user_id)
        
        if stats.get('premium_status') != 'Faol':
            await update.message.reply_text(
                "💳 Bu xususiyat faqat Premium foydalanuvchilar uchun. Premium rejasini tanlang: /premium"
            )
            return
        
        return await func(update, context, *args, **kwargs)
    
    return wrapper


def log_command(func):
    """Decorator to log command usage"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        logger.info(f"User {user.username} ({user.id}) called command: {func.__name__}")
        return await func(update, context, *args, **kwargs)
    
    return wrapper
