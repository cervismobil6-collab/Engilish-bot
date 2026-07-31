"""
Database queries
"""

from datetime import datetime
from database.connection import get_db
from database.models import User


async def get_or_create_user(user_data: dict) -> dict:
    """Get or create user"""
    db = get_db()
    
    result = await db.users.find_one({'telegram_id': user_data['telegram_id']})
    
    if not result:
        user = User(
            telegram_id=user_data['telegram_id'],
            username=user_data.get('username'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name')
        )
        await db.users.insert_one(user.to_dict())
        return user.to_dict()
    
    return result


async def get_user_stats(telegram_id: int) -> dict:
    """Get user statistics"""
    db = get_db()
    
    user = await db.users.find_one({'telegram_id': telegram_id})
    
    if not user:
        return {
            'level': 'A1',
            'completed_lessons': 0,
            'streak': 0,
            'coins': 0,
            'premium_status': 'Faol emas',
            'premium_expires': 'N/A',
            'rank': 'N/A'
        }
    
    return {
        'level': user.get('level', 'A1'),
        'completed_lessons': len(user.get('completed_lessons', [])),
        'streak': user.get('streak', 0),
        'coins': user.get('coins', 0),
        'premium_status': 'Faol' if user.get('premium') else 'Faol emas',
        'premium_expires': user.get('premium_expires', 'N/A'),
        'rank': 'N/A'
    }


async def update_user_premium(telegram_id: int, premium_plan: str) -> None:
    """Update user premium status"""
    db = get_db()
    
    # Calculate expiration date based on plan
    from dateutil.relativedelta import relativedelta
    now = datetime.utcnow()
    
    if premium_plan == '1month':
        expires = now + relativedelta(months=1)
    elif premium_plan == '3months':
        expires = now + relativedelta(months=3)
    else:  # lifetime
        expires = now + relativedelta(years=100)
    
    await db.users.update_one(
        {'telegram_id': telegram_id},
        {
            '$set': {
                'premium': True,
                'premium_expires': expires,
                'updated_at': datetime.utcnow()
            }
        }
    )
