import asyncio
import logging
import random
from typing import List, Union
from telegram import Bot, ReactionTypeEmoji

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    level=logging.WARNING,
)
logger = logging.getLogger("UltraProMaxReactionEngine")

class TelegramReactionEngine:
    def __init__(self, bot_tokens: List[str], channel_id: Union[int, str]):
        self.bot_tokens = bot_tokens
        self.channel_id = channel_id
        self.emoji_pool = [
            "❤️", "❤️", "❤️", "❤️", "❤️", "❤️", "❤️", "❤️", "❤️", "❤️",
            "👍", "🔥", "❤️", "❤️", "👏", "🎉", "❤️", "😍", "🤩", "❤️"
        ]

    async def _safe_react(self, token: str, message_id: int, emoji: str, attempt: int = 1) -> bool:
        try:
            async with Bot(token=token) as bot:
                await bot.set_message_reaction(
                    chat_id=self.channel_id,
                    message_id=message_id,
                    reaction=[ReactionTypeEmoji(emoji)],
                    is_big=False
                )
                return True
        except Exception as e:
            # अगर कोई फ्लड या लिमिट एरर आए तो थोड़ा रुककर दोबारा कोशिश करें
            if "flood" in str(e).lower() or "too_many" in str(e).lower():
                if attempt < 3:
                    await asyncio.sleep(random.uniform(2.0, 4.0))
                    return await self._safe_react(token, message_id, emoji, attempt + 1)
            return False

    async def execute_reaction_campaign(self, message_id: int) -> None:
        if not self.bot_tokens:
            return

        tokens = list(self.bot_tokens)
        random.shuffle(tokens)
        total_bots = len(tokens)
        
        # पहले 2 मिनट (120 सेकंड) में 20 रिएक्शन पूरे करने के लिए गति सेट की गई है
        fast_phase_limit = min(20, total_bots)

        for index, token in enumerate(tokens):
            emoji = random.choice(self.emoji_pool)
            await self._safe_react(token, message_id, emoji)

            if index == total_bots - 1:
                break

            # टाइमिंग: पहले 20 के लिए तेज़, बाद के लिए धीमा (कुल 4 मिनट का प्रोसेस)
            if index < fast_phase_limit:
                delay = random.uniform(5.0, 6.5)
            else:
                delay = random.uniform(12.0, 18.0)

            await asyncio.sleep(delay)

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
    TARGET_MESSAGE_ID = 26251

    engine = TelegramReactionEngine(
        bot_tokens=MASTER_BOT_TOKENS,
        channel_id=PRIVATE_CHANNEL_ID
    )
    
    await engine.execute_reaction_campaign(message_id=TARGET_MESSAGE_ID)

if __name__ == "__main__":
    asyncio.run(main())
        
