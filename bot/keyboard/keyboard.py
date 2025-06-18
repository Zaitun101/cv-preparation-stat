from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:
    @staticmethod
    def get_time_selection_keyboard():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='🕒 1ч', callback_data='time_1h'),
                    InlineKeyboardButton(text='🕒 2ч', callback_data='time_2h'),
                    InlineKeyboardButton(text='🕒 3ч', callback_data='time_3h'),
                ],
                [
                    InlineKeyboardButton(text='🕒 4ч', callback_data='time_4h'),
                    InlineKeyboardButton(text='🕒 6ч', callback_data='time_6h'),
                    InlineKeyboardButton(text='🕒 12ч', callback_data='time_12h'),
                ],
                [
                    InlineKeyboardButton(text='🕒 24ч', callback_data='time_24h'),
                    InlineKeyboardButton(text='🕒 48ч', callback_data='time_48h'),
                    InlineKeyboardButton(text='🕒 72ч', callback_data='time_72h'),
                ],
            ]
        )

    @staticmethod
    def get_detail_selection_keyboard():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='🐶 Статистика по фейлам Adopt',
                        callback_data='detail_adopt',
                    )
                ],
                [
                    InlineKeyboardButton(text='🎮 Игры', callback_data='detail_games'),
                    InlineKeyboardButton(
                        text='🖥️ Серверы', callback_data='detail_servers'
                    ),
                ],
                [InlineKeyboardButton(text='⬅ Назад', callback_data='back_to_time')],
            ]
        )
