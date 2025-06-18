from aiogram.types import Message
from bot.utils.utils import parse_hours_from_text


def register(tg_bot):
    @tg_bot.dp.message()
    async def handle_custom_time_input(message: Message):
        text = message.text.strip().lower()
        hours = parse_hours_from_text(text)

        if not hours:
            await message.answer(
                '❌ Не удалось распознать количество часов, напишите число'
            )
            return

        await tg_bot.reporter.show_report_for_hours(tg_bot, message, hours)
