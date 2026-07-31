"""
Premium subscription and payment verification system
"""

import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from config import config
from database.queries import update_user_premium, get_user_stats

logger = logging.getLogger(__name__)

# Conversation states
AWAITING_SCREENSHOT = 1

# Updated premium prices
PREMIUM_PLANS = {
    '1month': {
        'name': '1 OY',
        'price': 29999,
        'emoji': '🥉',
        'duration_days': 30
    },
    '3months': {
        'name': '3 OY',
        'price': 79999,
        'emoji': '🥈',
        'duration_days': 90
    },
    'lifetime': {
        'name': 'UMRBOYI',
        'price': 299000,  # Updated to 299,000 som
        'emoji': '🥇',
        'duration_days': 36500  # 100 years
    }
}

PAYMENT_CARD = "5614 6818 8730 1095"
CARD_HOLDER = "Gʻsniyev Sardorbek"
ADMIN_USERNAME = config.ADMIN_USERNAME
ADMIN_CHAT_ID = config.ADMIN_ID


async def show_premium(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show premium plans with new pricing"""
    text = f"""
👑 **PREMIUM REJALAR**

🥉 **1 MONTH** (1 Oy)
   Narxi: {PREMIUM_PLANS['1month']['price']:,} so'm
   ✅ Barcha darslar
   ✅ AI Ustoz cheksiz
   ✅ Testlar cheksiz
   ✅ Sertifikat olish

🥈 **3 MONTHS** (3 Oy)
   Narxi: {PREMIUM_PLANS['3months']['price']:,} so'm
   ✅ Barcha darslar
   ✅ AI Ustoz cheksiz
   ✅ Testlar cheksiz
   ✅ Sertifikat olish
   ✅ Priority support

🥇 **LIFETIME** (Umrboyi)
   Narxi: {PREMIUM_PLANS['lifetime']['price']:,} so'm
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
            f"🥉 1 Oy - {PREMIUM_PLANS['1month']['price']:,} so'm",
            callback_data="premium_1month"
        )],
        [InlineKeyboardButton(
            f"🥈 3 Oy - {PREMIUM_PLANS['3months']['price']:,} so'm",
            callback_data="premium_3months"
        )],
        [InlineKeyboardButton(
            f"🥇 Umrboyi - {PREMIUM_PLANS['lifetime']['price']:,} so'm",
            callback_data="premium_lifetime"
        )],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)


async def handle_premium_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle premium plan selection"""
    query = update.callback_query
    await query.answer()
    
    # Extract plan from callback_data
    plan = query.data.replace('premium_', '')
    
    if plan not in PREMIUM_PLANS:
        await query.edit_message_text("❌ Noto'g'ri rejani tanlash. Qayta urinib ko'ring.")
        return ConversationHandler.END
    
    # Store selected plan in context
    context.user_data['selected_plan'] = plan
    context.user_data['user_id'] = update.effective_user.id
    context.user_data['username'] = update.effective_user.username
    context.user_data['first_name'] = update.effective_user.first_name
    
    plan_info = PREMIUM_PLANS[plan]
    
    payment_text = f"""
💳 **TO'LOV MA'LUMOTLARI**

📌 Rejangiz: {plan_info['emoji']} {plan_info['name']}
💰 Narxi: {plan_info['price']:,} so'm

🏦 **Kartaga to'lov:**
Karta raqami: `{PAYMENT_CARD}`
Holders: {CARD_HOLDER}

📝 **To'lov bosqichlari:**
1️⃣ Kartaga {plan_info['price']:,} so'm to'lang
2️⃣ To'lov chekining screenshot'ini yuboring
3️⃣ Admin tasdiqlagandan keyin premium faollashiladi

📸 Iltimos, to'lov chekining screenshot'ini yuboring:
    """
    
    keyboard = [
        [InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_payment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(payment_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    return AWAITING_SCREENSHOT


async def receive_payment_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receive payment screenshot from user"""
    if not update.message.photo:
        await update.message.reply_text(
            "❌ Iltimos, rasm yuboring (screenshot). Boshqa fayl turlari qabul qilinmaydi."
        )
        return AWAITING_SCREENSHOT
    
    # Get the highest quality photo
    photo_file = update.message.photo[-1]
    photo_id = photo_file.file_id
    
    user_info = {
        'user_id': context.user_data['user_id'],
        'username': context.user_data['username'],
        'first_name': context.user_data['first_name'],
        'plan': context.user_data['selected_plan'],
        'plan_name': PREMIUM_PLANS[context.user_data['selected_plan']]['name'],
        'price': PREMIUM_PLANS[context.user_data['selected_plan']]['price'],
        'photo_id': photo_id
    }
    
    # Confirm to user
    plan_info = PREMIUM_PLANS[context.user_data['selected_plan']]
    confirmation_text = f"""
✅ **TO'LOV TASDIQLANDI**

👤 Foydalanuvchi: {user_info['first_name']} (@{user_info['username']})
📌 Rejangiz: {plan_info['emoji']} {plan_info['name']}
💰 Summa: {user_info['price']:,} so'm

⏳ Admin tasdiqlanishi kutilmoqda...
Tasdiqlangandan keyin sizning akkountingiz faollashiladi.

Adminning javobini kuting!
    """
    
    await update.message.reply_text(confirmation_text)
    
    # Send to admin for verification
    await send_payment_to_admin(context.bot, user_info, photo_id)
    
    logger.info(f"Payment screenshot received from user {user_info['user_id']}")
    
    return ConversationHandler.END


async def send_payment_to_admin(bot, user_info: dict, photo_id: str) -> None:
    """Send payment details and screenshot to admin for verification"""
    admin_message = f"""
🔔 **YANGI TO'LOV TASDIQLANISH KUTILMOQDA**

👤 **Foydalanuvchi ma'lumoti:**
   Ism: {user_info['first_name']}
   Username: @{user_info['username']}
   ID: {user_info['user_id']}

📌 **To'lov ma'lumoti:**
   Rejangiz: {PREMIUM_PLANS[user_info['plan']]['emoji']} {user_info['plan_name']}
   Summa: {user_info['price']:,} so'm
   Karta: {PAYMENT_CARD}
   Holder: {CARD_HOLDER}

📸 **Chek screenshot'i quyida:**

✅ Tasdiqlash uchun: /approve_{user_info['user_id']}
❌ Rad etish uchun: /reject_{user_info['user_id']}
    """
    
    try:
        if config.ADMIN_ID:
            # Send message to admin
            await bot.send_message(
                chat_id=config.ADMIN_ID,
                text=admin_message
            )
            
            # Send screenshot to admin
            await bot.send_photo(
                chat_id=config.ADMIN_ID,
                photo=photo_id,
                caption=f"To'lov cheki: {user_info['first_name']} - {user_info['price']:,} so'm"
            )
        else:
            logger.warning(f"Admin ID not configured. Cannot send payment verification request.")
    except Exception as e:
        logger.error(f"Failed to send payment to admin: {e}")


async def approve_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin approves payment and activates premium"""
    # Check if user is admin
    if update.effective_user.username != config.ADMIN_USERNAME:
        await update.message.reply_text(
            "❌ Siz admin emassiz! Ushbu buyruq faqat adminga ruxsat berilgan."
        )
        return
    
    try:
        # Extract user_id from command
        user_id = int(context.args[0].replace('approve_', '')) if context.args else None
        
        if not user_id:
            # Try to get from callback if exists
            if hasattr(update, 'callback_query') and update.callback_query:
                user_id = int(update.callback_query.data.split('_')[1])
        
        if not user_id:
            await update.message.reply_text(
                "❌ Foydalanuvchi ID topilmadi. Formati: /approve_123456789"
            )
            return
        
        # Find the plan from recent payments (for demo purposes, default to lifetime)
        plan = 'lifetime'  # In production, fetch from database
        
        # Update user premium status
        await update_user_premium(user_id, plan)
        
        # Send success message to admin
        await update.message.reply_text(
            f"✅ Foydalanuvchi {user_id} uchun {PREMIUM_PLANS[plan]['emoji']} {PREMIUM_PLANS[plan]['name']} rejasi faollashtirildi."
        )
        
        # Notify user (if bot has access)
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"""✅ **PREMIUM FAOLLASHTIRILDI!**

🎉 Tabriklaymiz! Sizning premium obunangiz {PREMIUM_PLANS[plan]['emoji']} {PREMIUM_PLANS[plan]['name']} rejasida faollashtirildi.

👑 Siz quyidagilarga ruxsat oldingiz:
✅ Barcha 120 darsga kirish
✅ AI Ustoz cheksiz
✅ Testlar cheksiz
✅ Sertifikat olish
✅ Priority support

🎓 O'rganishni boshlang: /menu
            """
            )
        except Exception as e:
            logger.warning(f"Could not notify user {user_id}: {e}")
        
        logger.info(f"Payment approved for user {user_id}")
    
    except Exception as e:
        logger.error(f"Error in approve_payment: {e}")
        await update.message.reply_text(f"❌ Xatolik yuz berdi: {e}")


async def reject_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin rejects payment"""
    # Check if user is admin
    if update.effective_user.username != config.ADMIN_USERNAME:
        await update.message.reply_text(
            "❌ Siz admin emassiz!"
        )
        return
    
    try:
        user_id = int(context.args[0].replace('reject_', '')) if context.args else None
        
        if not user_id:
            await update.message.reply_text(
                "❌ Formati: /reject_123456789"
            )
            return
        
        await update.message.reply_text(
            f"❌ Foydalanuvchi {user_id} ning to'lovi rad etildi."
        )
        
        # Notify user
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="""❌ **TO'LOV RAD ETILDI**

Administrator sizning to'lovingizni rad etdi. 
Sabablar:
• To'lov cheki aniq emas
• Noto'g'ri summa
• Kartada vositalar yo'q

📞 Admin bilan bog'laning: @jasurdos
            """
            )
        except Exception as e:
            logger.warning(f"Could not notify user {user_id}: {e}")
        
        logger.info(f"Payment rejected for user {user_id}")
    
    except Exception as e:
        logger.error(f"Error in reject_payment: {e}")
        await update.message.reply_text(f"❌ Xatolik: {e}")


async def cancel_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """User cancels payment process"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "❌ To'lov jarayoni bekor qilindi.\n\n/menu - Menuga qaytish"
    )
    
    return ConversationHandler.END
