from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from src.keyboards.user import UserKeyboards
from src.messages.user import UserMessages
from src.database.users import User, create_or_update_user, get_user_or_none
from src.utils.check_subscription import get_not_subscribed_channels


async def handle_start_command(message: Message, state: FSMContext):
    await state.clear()

    user = message.from_user
    _, user = create_or_update_user(telegram_id=user.id, firstname=user.first_name, username=user.username)

    not_subscribed_channels = await get_not_subscribed_channels(bot=message.bot, user_id=user.telegram_id)
    if not_subscribed_channels:
        await message.answer(UserMessages.get_welcome(user_name=user.name))
        await message.answer(
            text=UserMessages.get_ask_for_subscribe(),
            reply_markup=UserKeyboards.get_check_subscription(not_subscribed_channels)
        )
        return

    await start(message.bot, user)


async def handle_check_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id

    not_subscribed_channels = await get_not_subscribed_channels(bot=callback.bot, user_id=user_id)
    if not_subscribed_channels:
        await callback.answer(text='Подпишитесь на все каналы!')
        new_markup = UserKeyboards.get_check_subscription(not_subscribed_channels)
        try:
            await callback.message.edit_reply_markup(reply_markup=new_markup)
        except Exception:
            pass
        return

    await callback.message.delete()
    await start(bot=callback.bot, user=get_user_or_none(user_id))


async def start(bot, user: User):
    if user.is_registration_passed:
        text = UserMessages.get_welcome_back()
        markup = UserKeyboards.get_main_menu()
    else:
        text = UserMessages.get_ask_for_registration()
        markup = UserKeyboards.get_choose_role()

    await bot.send_message(chat_id=user.telegram_id, text=text, reply_markup=markup)


def register_start_command_handler(router: Router):
    # Команда /start
    router.message.register(handle_start_command, CommandStart())

    router.callback_query.register(handle_check_subscription, F.data == 'check_subscription')
