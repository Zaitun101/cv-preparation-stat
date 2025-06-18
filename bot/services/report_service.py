from datetime import datetime, timedelta

from bot.services.statistics_service import StatisticsService
from bot.keyboard.keyboard import Keyboard
from bot.utils.utils import get_user_and_message, split_message_text


class ReportService:
    def __init__(self):
        self.statistics = StatisticsService()

    def get_general_statistics(self, events):
        return self.statistics.get_general_statistics(events)

    def get_game_statistics(self, events):
        return self.statistics.get_game_statistics(events)

    def get_server_statistics(self, events):
        return self.statistics.get_server_statistics(events)

    def get_adopt_statistics(self, events):
        return self.statistics.get_adopt_statistics(events)

    async def show_report_for_hours(self, tg_bot, message_or_callback, hours: int):
        user_id, message = get_user_and_message(message_or_callback)

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        await message.answer(
            f'⏳ Собираю статистику за период:\nс {start_time.strftime("%Y-%m-%d %H:%M UTC")} '
            f'до {end_time.strftime("%Y-%m-%d %H:%M UTC")}'
        )

        events = self.statistics.mongo.get_events(hours)

        tg_bot.user_context[user_id] = {'events': events, 'hours': hours}

        lines = self.get_general_statistics(events)
        for chunk in split_message_text('\n'.join(lines)):
            await message.answer(chunk)

        detail_keyboard = Keyboard.get_detail_selection_keyboard()
        await message.answer('✅ Done !', reply_markup=detail_keyboard)
