from aiogram import Bot, Dispatcher
from bot.services.report_service import ReportService
from bot.handlers import commands, callbacks, messages


class TgBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.reporter = ReportService()
        self.user_context = {}

        self.time_options = {
            '1h': 1,
            '2h': 2,
            '3h': 3,
            '4h': 4,
            '6h': 6,
            '12h': 12,
            '24h': 24,
            '48h': 48,
            '72h': 72,
        }

        commands.register(self)
        callbacks.register(self)
        messages.register(self)
