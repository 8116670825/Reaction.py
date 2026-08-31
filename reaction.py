import asyncio
import logging
import random
import os
from typing import List, Union
from telegram import Bot, ReactionTypeEmoji
from telegram.error import TelegramError, NetworkError, TimedOut
from aiohttp import web

# बेहतरीन लॉगिंग सेटअप ताकि हर दिक्कत साफ़ दिखे
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("UltraProMaxEngine")

# Render फ्री टियर के पोर्ट एरर को रोकने के लिए अल्ट्रा-स्टेबल डमी वेब सर्वर
async def handle(request):
    return web.Response(text="Ultra Pro Max Telegram Reaction Engine is Online & Healthy!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"🚀 Render Port-Binding Server successfully active on port {port}")

class UltraProMaxReactionEngine:
    def __init__(self, bot_tokens: List[str], channel_id: Union[int, str]):
        self.bot_tokens = bot_tokens
        self.channel_id = channel_id
        self.emoji_pool = [
            "❤️", "❤️", "❤️", "❤️", "❤️", "❤️", "❤️", "❤️", "❤️", "❤️",
            "👍", "🔥", "❤️", "❤️", "👏", "🎉", "❤️", "😍", "🤩", "❤️"
        ]

    async def _bulletproof_react(self, token: str, message_id: int, emoji: str, max_retries: int = 3) -> bool:
        """नेटवर्क इश्यू, टाइमआउट या फ्लड एरर से निपटने के लिए एडवांस्ड रिकवरी मेकैनिज्म"""
        for attempt in range(1, max_retries + 1):
            try:
                # हर बार नया बॉट सेशन ताकि पुराना कनेक्शन जाम न हो
                async with Bot(token=token) as bot:
                    await bot.set_message_reaction(
                        chat_id=self.channel_id,
                        message_id=message_id,
                        reaction=[ReactionTypeEmoji(emoji)],
                        is_big=False
                    )
                    return True
            
            except (NetworkError, TimedOut) as net_err:
                # अगर नेटवर्क या टाइमआउट की समस्या हो तो थोड़ा रुककर दोबारा कोशिश करें
                logger.warning(f"⚠️ Network glitch on attempt {attempt}: {net_err}. Retrying...")
                if attempt == max_retries:
                    return False
                await asyncio.sleep(random.uniform(3.0 * attempt, 5.0 * attempt))
                
            except TelegramError as tg_err:
                err_msg = str(tg_err).lower()
                # अगर टेलीग्राम फ्लड या लिमिट एरर दे दे
                if "flood" in err_msg or "too_many" in err_msg:
                    sleep_time = random.uniform(10.0, 15.0)
                    logger.warning(f"🛡️ Flood control triggered. Sleeping for {sleep_time:.1f}s...")
                    await asyncio.sleep(sleep_time)
                    if attempt < max_retries:
                        continue
                # किसी अन्य बॉट या परमिशन एरर पर चुपचाप स्किप करें ताकि प्रोसेस न रुके
                return False
                
            except Exception as e:
                logger.error(f"❌ Unexpected error: {e}")
                return False
        return False

    async def execute_campaign(self, message_id: int) -> None:
        if not self.bot_tokens:
            logger.error("❌ No bot tokens provided!")
            return

        tokens = list(self.bot_tokens)
        random.shuffle(tokens)
        total_bots = len(tokens)
        
        logger.info(f"🎯 Starting Ultra Pro Max Campaign with {total_bots} bots for message ID: {message_id}")
        
        fast_phase_limit = min(20, total_bots)

        for index, token in enumerate(tokens):
            emoji = random.choice(self.emoji_pool)
            success = await self._bulletproof_react(token, message_id, emoji)
            
            if success:
                logger.info(f"✅ Bot [{index+1}/{total_bots}] successfully reacted with {emoji}")

            if index == total_bots - 1:
                break

            # आपके तय किए गए समय के अनुसार सटीक डिले मैनेजमेंट
            if index < fast_phase_limit:
                delay = random.uniform(5.0, 6.5)  # पहले 2 मिनट में तेज़ रफ़्तार
            else:
                delay = random.uniform(12.0, 18.0) # बाकी समय के लिए धीमी रफ़्तार

            await asyncio.sleep(delay)
        
        logger.info("🎉 Reaction campaign successfully completed across all active bot nodes.")

async def main():
    # Render को चालू रखने के लिए सबसे पहले वेब सर्वर शुरू करें
    asyncio.create_task(start_web_server())

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
    TARGET_MESSAGE_ID = 26251

    engine = UltraProMaxReactionEngine(
        bot_tokens=MASTER_BOT_TOKENS,
        channel_id=PRIVATE_CHANNEL_ID
    )
    
    # मुख्य रिएक्शन कैंपेन चलाएं
    await engine.execute_campaign(message_id=TARGET_MESSAGE_ID)
    
    # काम खत्म होने के बाद भी सर्वर को जिंदा रखें ताकि Render फ्री टियर में ऐप बंद न करे
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
        
