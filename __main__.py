import asyncio
from settings import TG_BOT_TOKEN
from bot.tg_bot import TgBot


async def start():
    tg_bot = TgBot(TG_BOT_TOKEN)
    await tg_bot.dp.start_polling(tg_bot.bot)


if __name__ == '__main__':
    asyncio.run(start())
