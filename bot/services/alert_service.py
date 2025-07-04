import asyncio
from datetime import datetime, timedelta, timezone

from aiogram import Bot
from bot.services.statistics_service import StatisticsService
from bot.utils.utils import split_message_text
from settings import CHAT_IDS


class AlertService:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.statistics = StatisticsService()

    async def check_alerts(self):
        events = self.statistics.mongo.get_events(20)
        if not events:
            return

        general_alert = self.statistics.get_alert_general_statistics(events)
        bot_result = general_alert[0]
        success_count = general_alert[1]
        success_percent = general_alert[2]
        fail_count = general_alert[3]
        fail_percent = general_alert[4]
        game_alerts = self.statistics.get_game_statistics(events)
        server_alerts = self.statistics.get_server_statistics(events)

        alerts = []

        if bot_result >= 20:
            if fail_percent >= 25:
                alerts.append(
                    f'✅ {success_count} — {success_percent}% | ❌ {fail_count} — {fail_percent}%'
                )

        for lines in (game_alerts, server_alerts):
            section = '\n'.join(lines)
            blocks = section.split('\n\n')
            for block in blocks:
                if block.strip().startswith('🚨'):
                    alerts.append(block.strip())

        print(f'alerts == {alerts}')

        if not alerts:
            return

        alert_text = '⚠️ Алерт по статистике за последние 2 часа:\n\n' + '\n\n'.join(
            alerts
        )
        for chat_id in CHAT_IDS:
            for chunk in split_message_text(alert_text):
                await self.bot.send_message(chat_id, chunk)

    async def start(self):
        while True:
            now = datetime.now(timezone.utc)
            print(f'time == {now}')
            await self.check_alerts()
            print(f'next_run == {now + timedelta(seconds=+7200)}')
            await asyncio.sleep(7200)
