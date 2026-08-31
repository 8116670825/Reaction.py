import asyncio
import logging
import random
import os
from typing import List, Union
from telegram import Bot, ReactionTypeEmoji, Update
from telegram.ext import ApplicationBuilder, ContextTypes
from flask import Flask, request

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    level=logging.WARNING,
)
logger = logging.getLogger("TimedAutoReactionBot")

app = Flask(__name__)

MASTER_BOT_TOKENS = [
    "8999002604:AAHQkjDH4E3AvbuorTSvRizaPHErLdj40cU",
    "8825165148:AAFLH2V0hDOsF2k5y53IKzCeycot7_MxYIA",
    "8473485047:AAE3-jus14leB8MdA332FCyBACEmEAE_O6g",
    "8659316894:AAFDd7rylEyeBxZXZDOVOA1d4MYJWSs-UuI",
    "8922121008:AAFX-9htuq38Y7PT4l0x4iyE_fBhr_b5qxU",
    "8906091528:AAE-WHsGRBZwW5mJjIM-T1qM4TyQ18pKAS8",
    "8843097551:AAF7kEu65d25ti2q13WRT9LP9rdpj0dsQFw",
    "8837449945:AAEr6moakG9CWXOUVggQx_N12yba_xQpHkU",
    "8633675773:AAFZLJxvr6wPyYQIODvrrnUC-ujwjprzE70",
    "8940372239:AAEnVaDwUBzRPJiHjXAFr4q0JyC4BnlWf9M",
    "8424700473:AAE_ssUvYbSZozT92PxnSxFqxEkzqIjmdNY",
    "8952443379:AAE1oJghDCJFDmmsut_cpea8iEPQwOsNjYM",
    "8737706065:AAGuUqc5z-NFvnRJsm_kB6NVmWunnZ14X9E",
    "8829734925:AAG1mzPW6RjI5vT5EADHocrqrO1qQnO4Dck",
    "8800528845:AAHmyyMYQFVNN-mZXNh_lqEWI1ERXhSXrpo",
    "8761698916:AAFfzO23UVGEwocLBZhn4T9pGzV-7liHzz8",
    "8782038492:AAE1lVStUJDe_VoYXWORS4K36lsbAXA9C2k",
    "8977006749:AAHghztgL1qQCbVJ7M9Phk5UXJqrsNWQoRw",
    "8968367741:AAF7zGlo9tLuE24cm4SgVgwJHm5Rqg5YV1Q",
    "8912664879:AAHvLsdmkgo6E4zeK-OT3PyfpA6bxvwjWxE",
    "8931245797:AAGe3G5yCuOJ_cRLURgtQ0Pn-x-wihcJG6M",
    "8839540355:AAG0bPt75mZeX-gSveu7k-dam1PfMdi2fmc",
    "8902690674:AAFAqYDASbZnDBAvoNf7dim12mDytFOIuCM",
    "8629441200:AAFkxBJNIaeiVqDjXiLdl9CihYgpSW0mHn4",
    "8634235544:AAFIv59qGL8JqXt1U0w5HoCwDPghY8qFw9Y",
    "8821954483:AAFqPDysUiD83OhUYE6vrQdUTfcKtRJWE6Q",
    "8974488228:AAFlFqYOdTRLgOmIbafVjbP5P3ic5WQUcMw",
    "7799842664:AAFtHUR9IuSXBgEN1xLe0qpy-jIBI1AUJ9A",
    "8931713588:AAE2mSWpT8EA8y96E2GhzWe4L_O-zb2-kXo"
]

PRIVATE_CHANNEL_ID = -1002982567511

async def _safe_react(token: str, message_id: int, emoji: str) -> bool:
    try:
        async with Bot(token=token) as bot:
            await bot.set_message_reaction(
                chat_id=PRIVATE_CHANNEL_ID,
                message_id=message_id,
                reaction=[ReactionTypeEmoji(emoji)],
                is_big=False
            )
            return True
    except Exception:
        return False

async def trigger_all_reactions(message_id: int):
    tokens = list(MASTER_BOT_TOKENS)
    random.shuffle(tokens)
    
    # हार्ट रिएक्शन की संख्या 13 से 15 के बीच तय की गई है
    target_heart_count = random.randint(13, 15)
    total_reactions = target_heart_count + 2  # कुल रिएक्शन थोड़े ज़्यादा ताकि मिक्स इमोजी भी आ सकें
    
    other_emojis = ["👍", "🔥", "😍", "👏", "🎉", "🤩", "🏆", "🍾", "👻", "👀"]

    print(f"--> Auto Triggered! Message ID: {message_id}. Sending ~{target_heart_count} hearts within time limit...")

    active_count = 0
    heart_sent = 0
    
    for token in tokens:
        if active_count >= total_reactions:
            break

        # पहले 13 से 15 तक सिर्फ हार्ट (❤️) भेजेगा, उसके बाद मिक्स्ड इमोजी
        if heart_sent < target_heart_count:
            emoji = "❤️"
            heart_sent += 1
        else:
            emoji = random.choice(other_emojis)
        
        success = await _safe_react(token, message_id, emoji)
        if success:
            active_count += 1

        # हर रिएक्शन के बीच 10 से 15 सेकंड का अंतराल
        delay = random.uniform(10.0, 15.0)
        await asyncio.sleep(delay)

@app.route('/')
def home():
    return "Timed Auto-Reaction Bot (13-15 Hearts) is Running 24/7!"

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if data:
        post = data.get("channel_post") or data.get("edited_channel_post")
        if post:
            chat = post.get("chat", {})
            if chat.get("id") == PRIVATE_CHANNEL_ID or chat.get("id") == str(PRIVATE_CHANNEL_ID):
                msg_id = post.get("message_id")
                if msg_id:
                    asyncio.run_coroutine_threadsafe(trigger_all_reactions(msg_id), loop)
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

async def main():
    global loop
    loop = asyncio.get_running_loop()
    
    main_bot_token = MASTER_BOT_TOKENS[0]
    application = ApplicationBuilder().token(main_bot_token).build()
    
    RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
    if RENDER_URL:
        webhook_url = f"{RENDER_URL}/webhook"
        await application.bot.set_webhook(url=webhook_url)

    import threading
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    print("Bot is up and listening with 13-15 heart constraints...")
    
    await application.initialize()
    await application.start()
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
    
