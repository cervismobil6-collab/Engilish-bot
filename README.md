# 📚 English AI Academy Bot

A comprehensive AI-powered Telegram bot for learning English with personalized lessons, AI tutor support, premium features, and more.

## ✨ Features

### 📖 Main Menu
- **📚 Kurslar** - View and manage courses
- **🤖 AI Ustoz** - Ask AI tutor anything about English
- **📖 Lug'at** - Dictionary with translations, pronunciation, examples
- **📝 Testlar** - Practice tests with instant feedback
- **👤 Profil** - User profile and progress tracking
- **💳 Premium** - Premium subscription management

### 🎓 Courses
- **A1 Beginner** to **C1 Advanced** - 6 levels
- **120 comprehensive lessons** total
- Each lesson includes:
  - 📖 Theory and explanation
  - 📝 Practical exercises
  - 🎯 10 test questions
  - 📊 Performance feedback

### 🤖 AI Tutor
Ask anything about English:
- Grammar explanations
- Sentence corrections with detailed explanations
- Speaking practice
- New vocabulary lessons
- IELTS exam preparation

### 📖 Dictionary
Categories:
- 👨 Family
- 🏫 School
- 🍔 Food
- 🏥 Hospital
- ✈️ Travel
- 💼 Work
- ❤️ Daily Expressions

Each word includes:
- English translation
- Uzbek translation
- Pronunciation
- Example sentences

### 📝 Tests
- 10 questions per lesson
- Instant results
- Error analysis
- Detailed explanations

### 👤 Profile
- User information
- Level and progress tracking
- Completed lessons
- Premium status
- Join date

### 💳 Premium Plans
- **🥉 1 Month** - 29,999 som
- **🥈 3 Months** - 79,999 som
- **🥇 Lifetime** - 299,999 som

Payment methods:
- Uzcard
- Humo
- Click
- Payme

### 👑 Additional Features
- ⭐ Daily streak system
- 🏆 Leaderboard (Top 10)
- 🎁 Referral system
- 📅 Daily reminders
- 🎓 Certificates for completed courses
- 📊 Detailed analytics
- 🌙 Dark mode
- 🔔 Notifications

### 👨‍💻 Admin Panel
- 📊 Statistics
- 👤 User management
- 📚 Add/edit lessons
- 👑 Grant premium access
- 📢 Send broadcast messages
- 💰 Verify payments

## 🚀 Installation

### Prerequisites
- Python 3.10+
- MongoDB
- Redis (optional, for caching)
- OpenAI API key
- Telegram Bot Token

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/cervismobil6-collab/Engilish-bot.git
cd Engilish-bot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the bot**
```bash
python main.py
```

## 🔧 Configuration

All configuration is in `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_token_here
OPENAI_API_KEY=your_openai_key
DATABASE_URL=your_mongodb_url
# ... other settings
```

## 📚 Project Structure

```
english-ai-academy-bot/
├── main.py                 # Bot entry point
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
│
├── handlers/             # Message handlers
│   ├── start.py
│   ├── menu.py
│   ├── courses.py
│   ├── ai_tutor.py
│   ├── dictionary.py
│   ├── tests.py
│   ├── profile.py
│   ├── premium.py
│   └── admin.py
│
├── database/             # Database operations
│   ├── models.py
│   ├── connection.py
│   └── queries.py
│
├── ai/                   # AI integration
│   ├── openai_service.py
│   └── prompts.py
│
├── utils/                # Utilities
│   ├── logger.py
│   └── decorators.py
│
└── tests/                # Test files
    └── test_bot.py
```

## 🎯 Bot Commands

### User Commands
```
/start - Start the bot
/menu - Main menu
/courses - View courses
/ai_tutor - Talk with AI tutor
/dictionary - Open dictionary
/tests - Practice tests
/profile - View profile
/premium - Premium plans
/leaderboard - Top users
/help - Help
```

### Admin Commands
```
/admin - Admin panel
/stats - Bot statistics
/users - User management
/broadcast - Send message to all users
/add_lesson - Add new lesson
/add_premium - Grant premium
/verify_payment - Verify payments
```

## 🔐 Security

- API keys stored in `.env` (never commit)
- `.env` in `.gitignore`
- User data encrypted in database
- Payment verification implemented
- Admin-only commands protected

## 📊 Database Schema

### Users
```
{
  _id: ObjectId,
  telegram_id: Number,
  username: String,
  first_name: String,
  level: String (A1-C1),
  completed_lessons: [ObjectId],
  premium: {
    active: Boolean,
    expires_at: Date,
    plan: String (1month, 3month, lifetime)
  },
  streak: Number,
  coins: Number,
  created_at: Date,
  updated_at: Date
}
```

### Lessons
```
{
  _id: ObjectId,
  level: String,
  lesson_number: Number,
  title: String,
  content: String,
  examples: [String],
  exercises: [Object],
  tests: [Object]
}
```

### Payments
```
{
  _id: ObjectId,
  user_id: ObjectId,
  amount: Number,
  method: String,
  transaction_id: String,
  status: String (pending, completed, failed),
  created_at: Date
}
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 💬 Support

For support, contact admin: [@jasurdos](https://t.me/jasurdos)

## 📞 Contact

- Bot: [@engilishpromax_bot](https://t.me/engilishpromax_bot)
- Admin: [@jasurdos](https://t.me/jasurdos)

---

**Made with ❤️ for English learners**
