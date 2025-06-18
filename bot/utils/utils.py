from aiogram.types import CallbackQuery


def split_message_text(text: str, max_len: int = 4096) -> list[str]:
    """Разделение текста на 4096 символа (формат одного сообщения в тг)"""
    return [text[i : i + max_len] for i in range(0, len(text), max_len)]


def get_user_and_message(obj):
    """Получение user_id и message из Message или CallbackQuery"""
    if isinstance(obj, CallbackQuery):
        return obj.from_user.id, obj.message
    return obj.from_user.id, obj


def parse_hours_from_text(text: str) -> int | None:
    """Извлечения числа часов из строки"""
    digits = ''.join(filter(str.isdigit, text))
    if digits:
        try:
            return int(digits)
        except ValueError:
            return None
    return None


async def prompt_select_time(callback, keyboard):
    """Промпт для выбора времени, если оно не было выбрано"""
    await callback.message.answer('❌ Сначала выберите период')
    await callback.message.edit_text('🕒 Выберите временной диапазон:')
    await callback.message.edit_reply_markup(reply_markup=keyboard)
