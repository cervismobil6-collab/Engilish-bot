"""
Database models/schemas
"""

from typing import Optional, List
from datetime import datetime


class User:
    """User model"""
    def __init__(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        level: str = "A1",
        premium: bool = False,
        premium_expires: Optional[datetime] = None,
        streak: int = 0,
        coins: int = 0,
        completed_lessons: List[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.level = level
        self.premium = premium
        self.premium_expires = premium_expires
        self.streak = streak
        self.coins = coins
        self.completed_lessons = completed_lessons or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            'telegram_id': self.telegram_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'level': self.level,
            'premium': self.premium,
            'premium_expires': self.premium_expires,
            'streak': self.streak,
            'coins': self.coins,
            'completed_lessons': self.completed_lessons,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Lesson:
    """Lesson model"""
    def __init__(
        self,
        level: str,
        lesson_number: int,
        title: str,
        content: str,
        examples: List[str] = None,
        exercises: List[dict] = None,
        tests: List[dict] = None
    ):
        self.level = level
        self.lesson_number = lesson_number
        self.title = title
        self.content = content
        self.examples = examples or []
        self.exercises = exercises or []
        self.tests = tests or []
    
    def to_dict(self):
        return {
            'level': self.level,
            'lesson_number': self.lesson_number,
            'title': self.title,
            'content': self.content,
            'examples': self.examples,
            'exercises': self.exercises,
            'tests': self.tests
        }


class Payment:
    """Payment model"""
    def __init__(
        self,
        user_id: str,
        amount: int,
        method: str,
        transaction_id: str,
        status: str = "pending",
        created_at: Optional[datetime] = None
    ):
        self.user_id = user_id
        self.amount = amount
        self.method = method
        self.transaction_id = transaction_id
        self.status = status
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'amount': self.amount,
            'method': self.method,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'created_at': self.created_at
        }
