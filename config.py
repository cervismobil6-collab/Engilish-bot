"""
Configuration file for English AI Academy Bot
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "engilishpromax_bot")
    BOT_NAME = os.getenv("BOT_NAME", "English AI Academy")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 2000))
    
    # Admin
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "jasurdos")
    ADMIN_ID = os.getenv("ADMIN_ID")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "english_ai_academy")
    
    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Payment
    PAYME_MERCHANT_ID = os.getenv("PAYME_MERCHANT_ID")
    PAYME_API_KEY = os.getenv("PAYME_API_KEY")
    CLICK_MERCHANT_ID = os.getenv("CLICK_MERCHANT_ID")
    CLICK_API_KEY = os.getenv("CLICK_API_KEY")
    
    # Premium Prices (in som)
    PREMIUM_PRICE_1MONTH = int(os.getenv("PREMIUM_PRICE_1MONTH", 29999))
    PREMIUM_PRICE_3MONTH = int(os.getenv("PREMIUM_PRICE_3MONTH", 79999))
    PREMIUM_PRICE_LIFETIME = int(os.getenv("PREMIUM_PRICE_LIFETIME", 299999))
    
    # Webhook
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", 8443))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "bot.log")
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENVIRONMENT = "development"


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENVIRONMENT = "production"


# Select configuration based on environment
config = ProductionConfig() if os.getenv("ENVIRONMENT", "production") == "production" else DevelopmentConfig()