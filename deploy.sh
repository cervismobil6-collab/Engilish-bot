#!/bin/bash
# Production deployment script for 24/7 running bot

echo "🚀 English AI Academy Bot - Production Deployment"
echo "================================================"

# Check Python version
echo "🔍 Python versiyasi tekshirilmoqda..."
python3 --version

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment yaratilimoqda..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Virtual environment faollashtirilmoqda..."
source venv/bin/activate

# Install/Update dependencies
echo "📥 Zavisimliklarni o'rnatish..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env fayli topilmadi!"
    echo "📝 .env.example dan .env yaratilmoqda..."
    cp .env.example .env
    echo "✏️  Iltimos, .env faylni o'z API kalitleri bilan tayyorlang"
    exit 1
fi

echo ""
echo "✅ Bot ishga tushirish uchun tayyor!"
echo ""
echo "📱 Bot ishga tushirish:"
echo "   python3 server.py"
echo ""
echo "🐳 Docker-da ishga tushirish (ixtiyoriy):"
echo "   docker build -t english-bot ."
echo "   docker run -d --restart always english-bot"
echo ""
