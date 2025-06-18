from aiogram.types import CallbackQuery
from bot.keyboard.keyboard import Keyboard
from bot.utils.utils import split_message_text, prompt_select_time


def register(tg_bot):
    @tg_bot.dp.callback_query(lambda c: c.data.startswith('time_'))
    async def handle_time_selection(callback: CallbackQuery):
        time_key = callback.data.split('_')[1]
        hours = tg_bot.time_options.get(time_key, 1)
        await tg_bot.reporter.show_report_for_hours(tg_bot, callback, hours)

    @tg_bot.dp.callback_query(
        lambda c: c.data in ['detail_games', 'detail_servers', 'back_to_time']
    )
    async def handle_detail_selection(callback: CallbackQuery):
        user_id = callback.from_user.id
        context = tg_bot.user_context.get(user_id)

        if callback.data == 'back_to_time':
            await callback.message.edit_text('🕒 Выберите временной диапазон:')
            await callback.message.edit_reply_markup(
                reply_markup=Keyboard.get_time_selection_keyboard()
            )
            return

        if not context or 'events' not in context:
            await prompt_select_time(callback, Keyboard.get_time_selection_keyboard())
            return

        events = context['events']

        if callback.data == 'detail_games':
            lines = tg_bot.reporter.get_game_statistics(events)
        elif callback.data == 'detail_servers':
            lines = tg_bot.reporter.get_server_statistics(events)
        else:
            await callback.message.answer('❌ Неизвестная команда')
            return

        for chunk in split_message_text('\n'.join(lines)):
            await callback.message.answer(chunk)

        detail_keyboard = Keyboard.get_detail_selection_keyboard()
        await callback.message.answer('✅ Done !', reply_markup=detail_keyboard)

    @tg_bot.dp.callback_query(lambda c: c.data == 'detail_adopt')
    async def handle_adopt_statistics(callback: CallbackQuery):
        user_id = callback.from_user.id
        context = tg_bot.user_context.get(user_id)

        if not context or 'events' not in context:
            await prompt_select_time(callback, Keyboard.get_time_selection_keyboard())
            return

        events = context['events']
        lines = tg_bot.reporter.get_adopt_statistics(events)

        if not lines:
            await callback.message.answer('❌ Ничего не найдено по этому фильтру')
        else:
            for chunk in split_message_text('\n'.join(lines)):
                await callback.message.answer(chunk)

        detail_keyboard = Keyboard.get_detail_selection_keyboard()
        await callback.message.answer('✅ Done !', reply_markup=detail_keyboard)
