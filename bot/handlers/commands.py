from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboard.keyboard import Keyboard


def register(tg_bot):
    @tg_bot.dp.message(Command('start'))
    async def cmd_start(message: Message):
        welcome_text = (
            '🤖 Привет !\n'
            'Я бот для анализа статистики прогрева\n\n'
            'Я могу показать:\n'
            '    • Статистику работы ботов\n'
            '    • Статистику по фейлам Adopt с данными для отправки боту @sp_logs_adopt_tmp_bot\n'
            '    • Углубленную статистику по играм, серверам и ботам\n\n'
            'Выберите временной диапазон:'
        )
        await message.answer(
            welcome_text, reply_markup=Keyboard.get_time_selection_keyboard()
        )

        help_hint = 'ℹ Чтобы узнать, как задавать время вручную, напишите /help'
        await message.answer(help_hint)

    @tg_bot.dp.message(Command('help'))
    async def cmd_help(message: Message):
        help_text = (
            'Вы можете задать временной диапазон двумя способами:\n\n'
            '1. Через кнопки: выбирайте из предложенных вариантов\n\n'
            '2. Написать текстом в чат:\n'
            '     • Например: `5 часов`,  `8 hours`,  `20h`\n'
            '     • Бот сам распознает число и покажет статистику за эти часы'
        )
        await message.answer(
            help_text,
            reply_markup=Keyboard.get_time_selection_keyboard(),
            parse_mode='Markdown',
        )
