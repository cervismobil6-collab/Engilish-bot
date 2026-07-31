"""
Premium handler
"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from config import config


async def show_premium(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show premium plans"""
    text = f"""
👑 **PREMIUM REJALAR**

🥉 **1 MONTH** (1 Oy)
   Narxi: {config.PREMIUM_PRICE_1MONTH:,} so'm
   ✅ Barcha darslar
   ✅ AI Ustoz cheksiz
   ✅ Testlar cheksiz
   ✅ Sertifikat olish

🥈 **3 MONTHS** (3 Oy)
   Narxi: {config.PREMIUM_PRICE_3MONTH:,} so'm
   ✅ Barcha darslar
   ✅ AI Ustoz cheksiz
   ✅ Testlar cheksiz
   ✅ Sertifikat olish
   ✅ Priority support

🥇 **LIFETIME** (Umr boyi)
   Narxi: {config.PREMIUM_PRICE_LIFETIME:,} so'm
   ✅ Barcha darslar
   ✅ AI Ustoz cheksiz
   ✅ Testlar cheksiz
   ✅ Sertifikat olish
   ✅ Premium support
   ✅ Barcha yangilanishlar

Rejani tanlang va to'lovni boshlang:
    """
    
    keyboard = [
        [InlineKeyboardButton(
            f"🥉 1 Oy - {config.PREMIUM_PRICE_1MONTH:,} so'm",
            callback_data="premium_1month"
        )],
        [InlineKeyboardButton(
            f"🥈 3 Oy - {config.PREMIUM_PRICE_3MONTH:,} so'm",
            callback_data="premium_3months"
        )],
        [InlineKeyboardButton(
            f"🥇 Umr boyi - {config.PREMIUM_PRICE_LIFETIME:,} so'm",
            callback_data="premium_lifetime"
        )],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
