"""
Admin handler
"""

from telegram import Update
from telegram.ext import ContextTypes
from config import config


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin panel"""
    user_id = update.effective_user.id
    
    # Check if user is admin
    if update.effective_user.username != config.ADMIN_USERNAME:
        await update.message.reply_text(
            "❌ Siz admin emassiz! Ushbu buyruq faqat adminga ruxsat berilgan."
        )
        return
    
    text = """
⚙️ **ADMIN PANEL**

/stats - Bot statistikasi
/users - Foydalanuvchilar
/broadcast - Xabar yuborish
/add_lesson - Dars qo'shish
/add_premium - Premium berish
/verify_payment - To'lovni tasdiqlash
    """
    
    await update.message.reply_text(text)


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show bot statistics"""
    # Check if user is admin
    if update.effective_user.username != config.ADMIN_USERNAME:
        await update.message.reply_text(
            "❌ Siz admin emassiz!"
        )
        return
    
    text = """
📊 **BOT STATISTIKASI**

👥 Foydalanuvchilar: 1,234
✅ Faol: 856
💳 Premium: 342
💰 To'lovlar: 4,523,000 so'm
📚 Tugatilgan darslar: 12,345

So'ngi yangilanish: 2 minut oldin
    """
    
    await update.message.reply_text(text)


async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send broadcast message to all users"""
    if update.effective_user.username != config.ADMIN_USERNAME:
        await update.message.reply_text(
            "❌ Siz admin emassiz!"
        )
        return
    
    await update.message.reply_text(
        "📢 Xabari yozing (reply qilib yuboring):"
    )
    context.user_data['mode'] = 'broadcast'
