from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from src.database import users
from src.database.models import StudentData, Category, Subcategory, SubcategoryContent
from src.messages.user import UserMessages
from src.misc.callback_factories import SubcategoryCallback
from src.keyboards.user import UserKeyboards


async def handle_category_button(message: Message):
    category: Category = Category.get(Category.title == message.text)

    subcategories = Subcategory.select().where(Subcategory.category == category)
    subcategories_count = len(subcategories)

    if subcategories_count == 0:
        text = UserMessages.get_section_in_dev()
        markup = None
    elif subcategories_count == 1:
        content = SubcategoryContent.get(subcategory=subcategories[0])
        await message.bot.copy_message(
            chat_id=message.from_user.id,
            from_chat_id=content.chat_id,
            message_id=content.message_id,
            caption=subcategories[0].title
        )
        return
    else:
        text = category.title
        markup = UserKeyboards.get_category(subcategories=subcategories)

    await message.answer(text=text, reply_markup=markup)


async def handle_subcategory(callback: CallbackQuery, callback_data: SubcategoryCallback):
    content = SubcategoryContent.get_or_none(SubcategoryContent.subcategory == callback_data.code)

    if not content:
        await callback.answer(text=UserMessages.get_section_in_dev(), show_alert=True)
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
