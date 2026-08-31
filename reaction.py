import asyncio
import logging
import random
import os
from typing import List, Union
from telegram import Bot, ReactionTypeEmoji
from flask import Flask

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    level=logging.WARNING,
)
logger = logging.getLogger("AutoDetectEngine")

app = Flask(__name__)

@app.route('/')
def home():
    return "Auto-Detect Reaction Bot Server is Live!"

@app.route('/ping')
def ping():
    return "Pong! Active.", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

class ChannelAutoDetector:
    def __init__(self, bot_tokens: List[str], channel_id: Union[int, str]):
        self.bot_tokens = bot_tokens
        self.channel_id = channel_id
        self.last_processed_id = 0

    async def _safe_react(self, token: str, message_id: int, emoji: str) -> bool:
        try:
            async with Bot(token=token) as bot:
                await bot.set_message_reaction(
                    chat_id=self.channel_id,
                    message_id=message_id,
                    reaction=[ReactionTypeEmoji(emoji)],
                    is_big=False
                )
                return True
        except Exception:
            return False

    async def trigger_reactions(self, message_id: int):
        tokens = list(self.bot_tokens)
        random.shuffle(tokens)
        
        heart_count = random.randint(15, 20)
        other_emojis = ["👍", "🔥", "😍", "👏", "🎉", "🤩", "🏆", "🍾", "👻", "👀", "🎃", "😎"]

        print(f"New message detected! ID: {message_id}. Sending reactions...")

        for index, token in enumerate(tokens):
            if index < heart_count:
                emoji = "❤️"
            else:
                emoji = random.choice(other_emojis)

            await self._safe_react(token, message_id, emoji)

            if index == len(tokens) - 1:
                break

            delay = random.uniform(15.0, 25.0)
            await asyncio.sleep(delay)

    async def start_auto_scanning(self):
        scanner_token = self.bot_tokens[0]
        print("Auto-detection scanner is running in background...")

        async with Bot(token=scanner_token) as bot:
            while True:
                try:
                    # चैनल के हालिया मैसेज को ट्रैक करने के लिए फॉरवर्ड या चैट इतिहास की जाँच
                    # चूंकि टेलीग्राम बॉट API चैनलों के सीधे अपडेट्स नहीं देता, 
                    # हम यहाँ एक स्मार्ट फॉरवर्ड चेकर विधि का उपयोग कर रहे हैं।
                    updates = await bot.get_updates(limit=5, timeout=10)
                    for update in updates:
                        if update.channel_post:
                            msg_id = update.channel_post.message_id
                            if msg_id > self.last_processed_id:
                                self.last_processed_id = msg_id
                                asyncio.create_task(self.trigger_reactions(msg_id))
                    
                except Exception as e:
                    # यदि कोई नेटवर्क या एपीआई लिमिट एरर हो तो थोड़ा रुककर फिर कोशिश करेगा
                    pass
                
                await asyncio.sleep(3)

async def main():
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

    detector = ChannelAutoDetector(
        bot_tokens=MASTER_BOT_TOKENS,
        channel_id=PRIVATE_CHANNEL_ID
    )
    
    await detector.start_auto_scanning()

if __name__ == "__main__":
    import threading
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    asyncio.run(main())
    
