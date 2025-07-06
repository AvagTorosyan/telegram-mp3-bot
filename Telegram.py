import telebot
from telebot import types
import os
import re
import tempfile
import subprocess
import uuid

bot = telebot.TeleBot("7589813852:AAE_QEjog9Vv3b45vsrTnzKjfXjW00cDaXs")

@bot.message_handler(commands=['start', 'hello', 'hi'])
def send_welcome(message):
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()

    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add(types.KeyboardButton('📋 Menu'))
    menu.add(types.KeyboardButton('💬 Contact'))
    menu.add(types.KeyboardButton('📢 Our Channel'))

    image_path = r"C:\Users\User\OneDrive\Սեղան\Telegram_Bot\Finger.jpg"
    if os.path.exists(image_path):
        with open(image_path, 'rb') as file:
            bot.send_photo(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, "⚠️ Image not found.")

    bot.send_message(
        message.chat.id,
        f"👋 Hello, {full_name}! I'm your friendly Telegram bot.\n"
        "🎧 Send me a YouTube link or an MP4 file, and I’ll convert it to MP3 for you!",
        reply_markup=menu
    )

@bot.message_handler(func=lambda msg: msg.text and ("youtube.com" in msg.text.lower() or "youtu.be" in msg.text.lower()))
def download_youtube_audio(message):
    try:
        url = message.text.strip()
        bot.send_message(message.chat.id, "⏳ Downloading and converting video to MP3...\n⏳This might take around 20 minutes — feel free to grab a coffee ☕, bro! ")

        temp_dir = tempfile.gettempdir()
        uid = uuid.uuid4().hex
        mp3_path = os.path.join(temp_dir, f"{uid}.mp3")

        command = [
            "yt-dlp",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "--output", mp3_path,
            url
        ]
        subprocess.run(command, check=True)

        if os.path.exists(mp3_path):
            with open(mp3_path, 'rb') as f:
                bot.send_audio(message.chat.id, f)
            os.remove(mp3_path)
        else:
            bot.send_message(message.chat.id, "❌ Error: File not created.")
    except Exception as e:
        print(f"[ERROR] {e}")
        bot.send_message(message.chat.id, "❌ Error: Could not process this link. Please try another one.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(
        message.chat.id,
        "📌 *Welcome!*\n"
        "This bot converts YouTube links to audio (MP3).\n"
        "Just send a YouTube link or upload an MP4 file, and I’ll convert it for you! 🎵\n\n"
        "🟢 *Simple. Fast. Free.*",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda msg: msg.text == '📋 Menu')
def site(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Open YouTube", url="https://www.youtube.com/")
    btn2 = types.InlineKeyboardButton(text="Convert MP4 (URL) ➝ MP3", callback_data='convert')
    btn3 = types.InlineKeyboardButton(text="Back", callback_data='delete')

    markup.row(btn1)
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "🌐 Choose your option ...", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    if call.data == "delete":
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
    elif call.data == "convert":
        bot.send_message(call.message.chat.id, "🛠 Please send me a YouTube link (MP4) to convert to MP3.")

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, "📸 Aww, great picture!")

@bot.message_handler(func=lambda message: True)
def info(message):
    text = message.text.lower()

    if text in ("hello", "hi"):
        first_name = message.from_user.first_name or "there"
        bot.send_message(message.chat.id, f"👋 Hello, {first_name}!")

    elif text == "i am mira":
        bot.send_message(message.chat.id, "I love you Mira ❤️")

    elif text == "id":
        bot.reply_to(message, f'🆔 Your Telegram ID: {message.from_user.id}')

    elif text == "contact" or text == "💬 contact":
        bot.send_message(message.chat.id, "📬 You can contact me via Gmail — feel free to write!\n🧾 avag.torosyan4@gmail.com")

    elif text == "our channel" or text == "📢 our channel":
        bot.send_message(message.chat.id, "📢 *Our Telegram Channel*\nStay tuned for updates and contact us anytime:\n🔗 https://t.me/convertorMp4", parse_mode='Markdown')

    else:
        bot.send_message(message.chat.id, "🤖 Sorry, I didn’t understand that. Try /help")

bot.polling(none_stop=True)
