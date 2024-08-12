from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from src.database import users
from src.database.models import StudentData, Category, Subcategory, SubcategoryContent
from src.misc.callback_factories import SubcategoryCallback
from src.keyboards.user import UserKeyboards


async def handle_category_button(message: Message):
    category: Category = Category.get(Category.title == message.text)
    await message.answer(
        text=category.description if category.description else category.title,
        reply_markup=UserKeyboards.get_category(category=category)
    )


async def handle_subcategory(callback: CallbackQuery, callback_data: SubcategoryCallback):
    content = SubcategoryContent.get_or_none(SubcategoryContent.subcategory == callback_data.code)

    if not content:
        await callback.answer(text='Этот раздел находится в разработке!', show_alert=True)
        return

    await callback.answer()
    await callback.bot.copy_message(
        chat_id=callback.from_user.id,
        from_chat_id=content.chat_id,
        message_id=content.message_id
    )


def register_menu_handlers(router: Router):

    router.message.register(
        handle_category_button,
        F.text.in_([category.title for category in Category.select(Category.title)])
    )

    router.callback_query.register(handle_subcategory, SubcategoryCallback.filter())
