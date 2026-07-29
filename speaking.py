from telebot import types
from database import add_points, update_streak
from handlers.ai import ask_claude

WAITING_FOR_VOICE = set()  # speaking rejimida turgan foydalanuvchilar


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "🗣 Speaking")
    def speaking_intro(message):
        update_streak(message.from_user.id)
        WAITING_FOR_VOICE.add(message.from_user.id)
        bot.send_message(
            message.chat.id,
            "🗣 <b>Speaking mashqi</b>\n\n"
            "Menga ingliz tilida 🎙 ovozli xabar yuboring — talaffuz va grammatikangizni "
            "tekshirib, tavsiya beraman.",
            parse_mode="HTML",
        )

    @bot.message_handler(content_types=["voice"], func=lambda m: m.from_user.id in WAITING_FOR_VOICE)
    def handle_voice(message):
        bot.send_message(message.chat.id, "⏳ Tahlil qilinmoqda...")

        try:
            import speech_recognition as sr
            from pydub import AudioSegment
            import io

            file_info = bot.get_file(message.voice.file_id)
            downloaded = bot.download_file(file_info.file_path)

            ogg_audio = AudioSegment.from_file(io.BytesIO(downloaded), format="ogg")
            wav_io = io.BytesIO()
            ogg_audio.export(wav_io, format="wav")
            wav_io.seek(0)

            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_io) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="en-US")

            bot.send_message(message.chat.id, f"📝 Eshitilgan matn:\n<i>{text}</i>", parse_mode="HTML")

            feedback = ask_claude(
                f"Talaba ingliz tilida gapirdi, transkripsiya: \"{text}\". "
                "O'zbek tilida qisqa (3-4 gap) grammatik va talaffuz bo'yicha tavsiya ber, "
                "ijobiy va rag'batlantiruvchi ohangda yoz."
            )
            bot.send_message(message.chat.id, f"🤖 AI tavsiyasi:\n{feedback}")
            add_points(message.from_user.id, 3)

        except Exception as e:
            bot.send_message(
                message.chat.id,
                "❌ Ovozni tahlil qilishda xatolik yuz berdi. Qaytadan urinib ko'ring.\n"
                f"(Texnik: {e})"
            )
