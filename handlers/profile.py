"""
Profile handler
"""

from telegram import Update
from telegram.ext import ContextTypes
from database.queries import get_user_stats


async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show user profile"""
    user_id = update.effective_user.id
    
    # Get user stats from database
    stats = await get_user_stats(user_id)
    
    text = f"""
👤 **PROFIL**

📝 **Ma'lumotlar:**
• Ism: {update.effective_user.first_name}
• Username: @{update.effective_user.username or 'N/A'}

📊 **Statistika:**
• Daraja: {stats.get('level', 'A1')}
• Tugatilgan darslar: {stats.get('completed_lessons', 0)}/120
• Streyk: {stats.get('streak', 0)} kun
• Coin'lar: {stats.get('coins', 0)} 🪙

👑 **Premium:**
• Status: {stats.get('premium_status', 'Faol emas')}
• Tugadigan sana: {stats.get('premium_expires', 'N/A')}

🏆 **Reyting:** #{stats.get('rank', 'N/A')}

Qo'shimcha ma'lumot uchun /help buyrug'ini bosing.
    """
    
    await update.message.reply_text(text)
