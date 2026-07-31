# English AI Academy Bot

## 24/7 Running Deployment Guide

### 🚀 Quick Start (Lokal - Development)

```bash
# 1. Clone repository
git clone https://github.com/cervismobil6-collab/Engilish-bot.git
cd Engilish-bot

# 2. Setup
bash deploy.sh

# 3. Configure .env
cp .env.example .env
# Edit .env with your API keys

# 4. Run bot with auto-restart
python3 run_24_7.py
```

### 🐳 Docker Deployment (Production - Recommended)

```bash
# 1. Build image
docker build -t english-bot .

# 2. Run with docker-compose (includes MongoDB & Redis)
docker-compose up -d

# 3. Check logs
docker logs -f english-ai-bot

# 4. Stop bot
docker-compose down
```

### ☁️ Cloud Deployment (VPS/Server)

#### Option 1: Systemd Service (Ubuntu/Debian)

```bash
# 1. Create service file
sudo nano /etc/systemd/system/english-bot.service
```

```ini
[Unit]
Description=English AI Academy Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Engilish-bot
ExecStart=/usr/bin/python3 /home/ubuntu/Engilish-bot/run_24_7.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 2. Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable english-bot
sudo systemctl start english-bot

# 3. Check status
sudo systemctl status english-bot

# 4. View logs
sudo journalctl -u english-bot -f
```

#### Option 2: Tmux (Session)

```bash
# 1. Install tmux
sudo apt-get install tmux

# 2. Create session
tmux new-session -d -s english-bot

# 3. Run bot
tmux send-keys -t english-bot "cd ~/Engilish-bot && python3 run_24_7.py" Enter

# 4. Attach to session
tmux attach -t english-bot

# 5. Detach (Ctrl+B then D)
```

### 🔍 Monitoring

```bash
# Check bot process
ps aux | grep python3

# Monitor logs
tail -f bot.log
tail -f bot_manager.log

# Check resource usage
htop

# Database status
mongo --eval "db.adminCommand('ping')"
redis-cli ping
```

### 📊 Bot Features (24/7)

✅ **Always Running:**
- Message handling
- Commands processing
- Payment verification
- AI responses
- Database queries

✅ **Scheduled Tasks:**
- Daily reminders (9:00 AM)
- Weekly statistics (Sunday 10 PM)
- Premium expiry check (1:00 AM)
- Database backup (3:00 AM)

✅ **Auto-Recovery:**
- Automatic restart on crash
- Connection retry
- Error logging
- Graceful shutdown

### 🛡️ Security Tips

```bash
# 1. Secure .env file
chmod 600 .env

# 2. Use strong database password
# 3. Enable firewall
sudo ufw enable
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443

# 4. Regular backups
crontab -e
# Add: 0 3 * * * /path/to/backup.sh

# 5. Monitor logs
grep ERROR bot.log | tail -20
```

### 🐛 Troubleshooting

```bash
# Bot not responding
1. Check logs: tail -f bot.log
2. Verify token: echo $TELEGRAM_BOT_TOKEN
3. Check database: mongo
4. Restart bot: systemctl restart english-bot

# High memory usage
1. Check process: ps aux | grep python
2. Monitor: htop
3. Restart if needed

# Database connection error
1. Check MongoDB: sudo systemctl status mongod
2. Verify connection string in .env
3. Check firewall rules
```

### 📞 Support

- Admin: @jasurdos
- Bot: @engilishpromax_bot
- GitHub: https://github.com/cervismobil6-collab/Engilish-bot

---

**Bot is running 24/7! 🚀**
