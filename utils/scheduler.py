"""
Scheduler for daily tasks and reminders
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def start_scheduler():
    """Start APScheduler for background tasks"""
    
    # Daily reminder at 9:00 AM
    @scheduler.scheduled_job(
        CronTrigger(hour=9, minute=0),
        id='daily_reminder',
        name='Daily learning reminder'
    )
    async def daily_reminder():
        logger.info("📢 Kunlik reminder yuborilimoqda...")
        # TODO: Send daily reminder to active users
    
    # Weekly statistics at Sunday 10:00 PM
    @scheduler.scheduled_job(
        CronTrigger(day_of_week=6, hour=22, minute=0),
        id='weekly_stats',
        name='Weekly statistics'
    )
    async def weekly_stats():
        logger.info("📊 Haftalik statistika tayyorlanmoqda...")
        # TODO: Send weekly stats to users
    
    # Check premium expiry daily at 1:00 AM
    @scheduler.scheduled_job(
        CronTrigger(hour=1, minute=0),
        id='check_premium_expiry',
        name='Check premium expiry'
    )
    async def check_premium_expiry():
        logger.info("🔍 Premium muddati tekshirilmoqda...")
        # TODO: Check and notify users about expiring premium
    
    # Backup database daily at 3:00 AM
    @scheduler.scheduled_job(
        CronTrigger(hour=3, minute=0),
        id='database_backup',
        name='Database backup'
    )
    async def database_backup():
        logger.info("💾 Database backup olinmoqda...")
        # TODO: Backup database
    
    scheduler.start()
    logger.info("✅ Scheduler ishga tushdi")
    
    return scheduler


def stop_scheduler():
    """Stop scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("⛔ Scheduler to'xtatildi")
