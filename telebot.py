import telebot
import time
import re
import os
import sys
from telebot import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 🔑 Bot Credentials (GitHub Secrets से लेंगे)
TOKEN = os.getenv('BOT_TOKEN')
TARGET_CHANNEL = os.getenv('TARGET_CHANNEL')

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# 🚫 Unwanted Patterns
UNWANTED_PATTERNS = [r"@\w+", r"www.", r"http://", r"https://", r"[{}]", r"\s{2,}"]

# 📌 Caption Format Function with Inline Button
def format_caption(file_name, file_size):
    cleaned_name = file_name.strip()
    for pattern in UNWANTED_PATTERNS:
        cleaned_name = re.sub(pattern, "", cleaned_name, flags=re.IGNORECASE).strip()
    cleaned_name = re.sub(r'[^a-zA-Z0-9 @._-]', '', cleaned_name)
    
    # Create the inline button
    inline_button = types.InlineKeyboardButton(
        text=" 🔥 ᴍᴏᴠɪᴇ ꜱᴇᴀʀᴄʜ ɢʀᴏᴜᴘ 🔥 ",
        url="https://t.me/FilmyEmpire_group"
    )
    inline_markup = types.InlineKeyboardMarkup(row_width=1)
    inline_markup.add(inline_button)
    
    # Create the caption text
    caption_text = f"<b><a href='https://t.me/FilmyEmpire'>{cleaned_name}</a></b>\n\n" \
                   f"<pre> �𝙵𝚒𝚕𝚎 𝚂𝚒𝚣𝚎 ♻️ ➥ {file_size} </pre>\n" \
                   f"<blockquote>𝙿𝚘𝚠𝚎𝚛𝚎𝚍 𝙱𝚢 ➥ <b><a href='https://t.me/FilmyEmpire'>@𝐅𝐈𝐋𝐌𝐘𝐄𝐌𝐏𝐈𝐑𝐄</a></b></blockquote>"

    return caption_text, inline_markup

# 📥 Handle Media Files
@bot.message_handler(content_types=["document", "video"])
def handle_media(message):
    file_id, file_name, file_type, file_size = None, None, None, None
    if message.document:
        file_id, file_name, file_type = message.document.file_id, message.document.file_name, "document"
        file_size = message.document.file_size / (1024 * 1024)
    elif message.video:
        file_id, file_name, file_type = message.video.file_id, message.video.file_name, "video"
        file_size = message.video.file_size / (1024 * 1024)

    if not file_id or not file_name:
        return

    file_size = f"{file_size / 1024:.2f} GB" if file_size >= 1024 else f"{file_size:.2f} MB"
    caption, inline_markup = format_caption(file_name, file_size)

    success, error_message = False, None
    retry_count = 3
    while retry_count > 0:
        try:
            if file_type == "document":
                bot.send_document(TARGET_CHANNEL, file_id, caption=caption, parse_mode="HTML", reply_markup=inline_markup)
            elif file_type == "video":
                bot.send_video(TARGET_CHANNEL, file_id, caption=caption, parse_mode="HTML", reply_markup=inline_markup)
            success = True
            print(f"✅ File Sent: {file_name}")
            break
        except telebot.apihelper.ApiException as e:
            retry_count -= 1
            error_message = f"❌ {file_name} | {TARGET_CHANNEL}: {e}"
            time.sleep(5)

    if not success:
        print(error_message)

# 🔄 Auto Restart Function
def restart_bot():
    print("🔁 Restarting bot in 5 seconds...")
    time.sleep(5)
    os.execv(sys.executable, ['python3'] + sys.argv)

# 🚀 Start Polling
def start_polling():
    while True:
        try:
            print("🤖 Bot is running...")
            bot.polling(none_stop=True, timeout=60, long_polling_timeout=5)
        except telebot.apihelper.ApiException as e:
            print(f"⚠️ Telegram API Error: {e}")
            time.sleep(10)
        except Exception as e:
            print(f"🔴 Unknown Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    start_polling()