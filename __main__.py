import asyncio
from settings import TG_BOT_TOKEN
from bot.tg_bot import TgBot
from bot.services.alert_service import AlertService


async def start():
    tg_bot = TgBot(TG_BOT_TOKEN)
    alert_service = AlertService(tg_bot.bot)

    asyncio.create_task(alert_service.start())
    await tg_bot.dp.start_polling(tg_bot.bot)


if __name__ == '__main__':
    asyncio.run(start())
