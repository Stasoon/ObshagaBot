from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.database.models import SubcategoryContent
from src.keyboards.admin import AdminKeyboards
from src.misc.callback_factories import SubcategoryCallback
from src.misc.states import EditContentStates


async def handle_edit_content_button(message: Message, state: FSMContext):
    await message.answer(
        text="Нажмите на вкладку, которую хотите изменить:",
        reply_markup=AdminKeyboards.get_edit_content()
    )
    await state.set_state(EditContentStates.enter_new_content)


async def handle_subcategory_callback(callback: CallbackQuery, state: FSMContext, callback_data: SubcategoryCallback):
    await callback.answer()

    await state.update_data(subcategory_code=callback_data.code)
    await callback.message.answer(
        text='Отправьте сообщение с новым содержанием:',
        reply_markup=AdminKeyboards.get_cancel()
    )


async def handle_new_content(message: Message, state: FSMContext):
    subcategory_code = (await state.get_data()).get('subcategory_code')
    if not subcategory_code:
        await message.answer(text='Отменено', reply_markup=AdminKeyboards.get_admin_menu())
        await state.clear()
        return

    if subcategory_content := SubcategoryContent.get_or_none(subcategory=subcategory_code):
        subcategory_content.message_id = message.message_id
        subcategory_content.chat_id = message.chat.id
        subcategory_content.save()
    else:
        SubcategoryContent.create(subcategory=subcategory_code, message_id=message.message_id, chat_id=message.chat.id)

    await message.answer(text='Готово!', reply_markup=AdminKeyboards.get_admin_menu())
    await state.clear()


async def handle_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Отменено', reply_markup=AdminKeyboards.get_admin_menu())


def register_admin_edit_content_handlers(router: Router):
    router.message.register(handle_edit_content_button, F.text == '✍️ Изменить наполнение')

    router.callback_query.register(
        handle_subcategory_callback, SubcategoryCallback.filter(), EditContentStates.enter_new_content
    )

    router.message.register(handle_cancel, F.text == '❌ Отменить', EditContentStates.enter_new_content)

    router.message.register(handle_new_content, EditContentStates.enter_new_content)
