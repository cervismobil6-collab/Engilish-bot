import os

# Muhim: Tokenni hech qachon kodga yozmang!
# Render/Railway'da "Environment Variables" bo'limiga qo'shing.

BOT_TOKEN = os.getenv("BOT_TOKEN", "SIZNING_BOT_TOKENINGIZ_BU_YERGA")

# Admin panelga kirish huquqi bo'lgan Telegram ID'lar (vergul bilan ajratib bir nechta bo'lishi mumkin)
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]

# AI funksiyalari uchun (Speaking tekshiruvi, IELTS Writing, AI suhbat)
# https://console.anthropic.com dan olinadi
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

DB_PATH = os.getenv("DB_PATH", "bot_database.db")

# Kuniga necha marta so'z/test o'tilsa streak hisoblanadi
DAILY_GOAL = 5
