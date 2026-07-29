# 🤖 English Learning Telegram Bot

Ingliz tilini professional darajada o'rgatuvchi Telegram bot: so'zlar, testlar, grammar,
speaking, IELTS, AI yordamchi, reyting, profil, daily streak, favorite va admin panel.

## 📁 Loyiha tuzilishi

```
english_bot/
├── main.py              # botni ishga tushiruvchi asosiy fayl
├── config.py            # TOKEN va sozlamalar (Environment Variables orqali)
├── database.py          # SQLite bilan ishlash (users, favorites, streak, points)
├── requirements.txt     # kerakli kutubxonalar
├── Procfile             # Railway/Render uchun ishga tushirish buyrug'i
├── runtime.txt           # Python versiyasi
├── data/
│   ├── words.json        # so'zlar bazasi (10000+ tagacha kengaytiriladi)
│   ├── tests.json         # test savollari (5000+ tagacha kengaytiriladi)
│   └── grammar.json       # grammatika mavzulari
└── handlers/
    ├── start.py            # /start va asosiy menyu
    ├── words.py            # 📚 So'zlar
    ├── tests.py            # 📝 Testlar
    ├── grammar.py          # 📖 Grammar
    ├── speaking.py         # 🗣 Speaking (ovozni AI orqali tekshirish)
    ├── ielts.py            # 🎯 IELTS Writing tekshiruvi
    ├── ai.py               # 🤖 AI yordamchi (Claude API)
    ├── rating.py           # 🏆 Reyting
    ├── profile.py          # 👤 Profil
    ├── favorite.py         # ❤️ Favorite
    └── admin.py            # 👨‍💼 Admin panel
```

## ⚙️ 1-qadam: Pydroid 3'da mahalliy sinash

1. Pydroid 3'ni oching, **Pip** bo'limidan quyidagilarni o'rnating:
   ```
   pyTelegramBotAPI requests SpeechRecognition pydub
   ```
2. Ushbu `english_bot` papkasini telefoningizga ko'chiring.
3. `config.py` faylida `BOT_TOKEN` o'rniga o'z tokeningizni yozing (faqat sinash uchun;
   productionda Environment Variable ishlating).
4. `main.py` faylini ishga tushiring.

> ⚠️ Speaking moduli `pydub` uchun `ffmpeg` talab qiladi. Pydroid 3'da ffmpeg bo'lmasligi
> mumkin — bu holda Speaking funksiyasi xato beradi, lekin qolgan barcha funksiyalar
> ishlayveradi. Serverga (Render/Railway) joylaganda ffmpeg avtomatik o'rnatiladi.

## 🔑 2-qadam: Bot tokenini olish

1. Telegram'da [@BotFather](https://t.me/BotFather) ga yozing.
2. `/newbot` buyrug'ini yuboring, nom va username bering.
3. Sizga beriladigan tokenni saqlab qo'ying.

## 🌐 3-qadam: Railway'ga 24/7 joylash (tavsiya etiladi)

1. [railway.app](https://railway.app) da ro'yxatdan o'ting (GitHub orqali).
2. Loyihani GitHub'ga yuklang (quyida yo'riqnoma).
3. Railway'da **New Project → Deploy from GitHub repo** tanlang.
4. **Variables** bo'limiga quyidagilarni qo'shing:
   - `BOT_TOKEN` — BotFather'dan olingan token
   - `ADMIN_IDS` — sizning Telegram ID'ingiz (masalan: `123456789`)
   - `ANTHROPIC_API_KEY` — AI funksiyalari uchun (ixtiyoriy)
5. Railway avtomatik `Procfile`ni o'qib, `worker: python main.py` buyrug'ini ishga tushiradi.
6. Deploy tugagach, bot 24/7 ishlaydi.

## 🌐 3-qadam (muqobil): Render'ga joylash

1. [render.com](https://render.com) da **New → Background Worker** tanlang.
2. GitHub repo'ni ulang.
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `python main.py`
5. **Environment** bo'limiga `BOT_TOKEN`, `ADMIN_IDS`, `ANTHROPIC_API_KEY` qo'shing.
6. Deploy qiling — Render bepul rejada worker'lar vaqti-vaqti bilan uxlab qolishi mumkin,
   shuning uchun to'liq 24/7 uchun pullik reja yoki Railway tavsiya etiladi.

## 📤 GitHub'ga yuklash (agar hali qilmagan bo'lsangiz)

```bash
cd english_bot
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/SIZNING_USERNAME/english_bot.git
git push -u origin main
```

## 📈 So'zlar va testlarni 10000+ / 5000+ tagacha kengaytirish

`data/words.json` va `data/tests.json` fayllari oddiy JSON ro'yxat — shu formatda
davom ettirib, xohlagancha so'z/test qo'shishingiz mumkin. Katta hajmda ma'lumot
qo'shmoqchi bo'lsangiz, Excel/CSV fayldan JSON'ga aylantirib olish ham mumkin —
shunga alohida yordam bera olaman.

## 👨‍💼 Admin panelga kirish

`config.py` (yoki Environment Variables) dagi `ADMIN_IDS` ro'yxatiga o'z Telegram
ID'ingizni qo'shing. ID'ni bilmasangiz [@userinfobot](https://t.me/userinfobot) ga yozing.
Keyin botga `/admin` buyrug'ini yuboring.

## 🤖 AI funksiyalarini yoqish

`ANTHROPIC_API_KEY` ni [console.anthropic.com](https://console.anthropic.com) dan olib,
Environment Variable sifatida qo'shsangiz, 🤖 AI, 🗣 Speaking va 🎯 IELTS
bo'limlaridagi AI baholash ishga tushadi.
