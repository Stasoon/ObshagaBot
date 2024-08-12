from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMediaDocument
from aiogram.fsm.context import FSMContext

from config import REQUESTS_CHANNEL_ID
from src.database.users import get_user_or_none
from src.misc.enums import WORK_TYPES
from src.misc.states import SpecialistRegistrationStates
from src.keyboards.user import UserKeyboards
from src.misc.callback_factories import WorkTypeCallback


async def handle_i_am_specialist(message: Message, state: FSMContext):
    await message.answer(text='Введите ваше имя:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(SpecialistRegistrationStates.enter_name)


async def handle_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(text='Отправьте ваш контактный номер телефона:', reply_markup=UserKeyboards.get_phone())
    await state.set_state(SpecialistRegistrationStates.enter_phone)


async def handle_phone(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone_number=phone_number)

    await message.answer(
        text='Выберите виды работ, которые вы выполняете:',
        reply_markup=UserKeyboards.get_works_types()
    )
    await message.answer(text='Затем нажмите кнопку "Готово"', reply_markup=UserKeyboards.get_done())

    await state.set_state(SpecialistRegistrationStates.enter_works)


async def handle_work(callback: CallbackQuery, state: FSMContext, callback_data: WorkTypeCallback):
    data = await state.get_data()
    works = data.get('works') or []

    if callback_data.work_id in works:
        works.remove(callback_data.work_id)
    else:
        works.append(callback_data.work_id)

    await state.update_data(works=works)
    markup = UserKeyboards.get_works_types(marked_works=works)
    await callback.message.edit_reply_markup(reply_markup=markup)


async def handle_save_works(message: Message, state: FSMContext):
    works = (await state.get_data()).get('works')

    if not works:
        await message.answer('Выберите хотя бы один вид работ!')
        return

    await state.update_data(works=[WORK_TYPES.get(work_id) for work_id in works])

    await message.answer(
        text='Напишите комментарий, если хотите дополнить список. \n\nИли нажмите кнопку "Пропустить"',
        reply_markup=UserKeyboards.get_skip()
    )
    await state.set_state(SpecialistRegistrationStates.enter_works_comment)


async def handle_works_comment(message: Message, state: FSMContext):
    if not message.text.lower().startswith('пропустить'):
        await state.update_data(works_comment=message.text)

    await message.answer(
        text='Напишите дисциплины и специальности, по которым можете выполнять задания:',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(SpecialistRegistrationStates.enter_specialties)


async def handle_specialties(message: Message, state: FSMContext):
    await state.update_data(specialties=message.text)

    await message.answer(
        text='Напишите, с какими иностранными языками можете работать:',
        reply_markup=UserKeyboards.get_skip()
    )
    await state.set_state(SpecialistRegistrationStates.enter_languages)


async def handle_languages(message: Message, state: FSMContext):
    if not message.text.lower().startswith('пропустить'):
        await state.update_data(languages=message.text)

    await message.answer(
        text='Работаете ли с вузовским антиплагиатом?',
        reply_markup=UserKeyboards.get_anti_plagiarism()
    )
    await state.set_state(SpecialistRegistrationStates.enter_anti_plagiarism)


async def handle_anti_plagiarism(message: Message, state: FSMContext):
    if message.text.lower() not in ('да', 'нет', 'только с бесплатным'):
        await message.answer('Выберите ответ из предложенных!')
        return

    await state.update_data(anti_plagiarism=message.text)
    await message.answer(
        text='Рассматриваете для себя нашу деятельность, как основную работу или подработку?',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(SpecialistRegistrationStates.enter_main_or_part_time_job)


async def handle_main_or_part_time_job(message: Message, state: FSMContext):
    await state.update_data(main_or_part_time_job=message.text)

    await message.answer(text='Сколько часов в день и в неделю готовы уделять нашей деятельности?')
    await state.set_state(SpecialistRegistrationStates.enter_work_hours)


async def handle_work_hours(message: Message, state: FSMContext):
    await state.update_data(work_hours=message.text)

    await message.answer(
        text='Напишите дополнительную информация о себе, если хотите. \n\nИли нажмите "Пропустить"',
        reply_markup=UserKeyboards.get_skip()
    )
    await state.set_state(SpecialistRegistrationStates.enter_additional_info)


async def handle_additional_info(message: Message, state: FSMContext):
    if not message.text.lower().startswith('пропустить'):
        await state.update_data(additional_info=message.text)

    await message.answer(
        text='Отправьте примеры ваших готовых работ в формате Word-документов (5-10 штук):',
        reply_markup=UserKeyboards.get_done()
    )
    await state.set_state(SpecialistRegistrationStates.enter_work_examples)


async def handle_work_example(message: Message, state: FSMContext):
    data = await state.get_data()
    documents = data.get('documents') or []

    if len(documents) >= 9:
        await message.answer('Можно прикрепить лишь 10 документов. Нажмите кнопку "Готово"')
        return

    if message.document:
        await message.reply('Файл добавлен')
        documents.append(message.document.file_id)
        await state.update_data(documents=documents)

    elif message.text.lower().startswith('готово'):
        if not documents:
            await message.answer('Сначала прикрепите Word-документы с примерами ваших работ!')
            return

        user = get_user_or_none(telegram_id=message.from_user.id)
        user.is_registration_passed = True
        user.save()

        await message.answer(
            text='🎉 Ваша кандидатура будет рассмотрена, мы свяжемся с вами в ближайшие дни.',
            reply_markup=ReplyKeyboardRemove()
        )

        await state.clear()
        await send_request_to_admin(bot=message.bot, user=message.from_user, request_data=data)

    else:
        await message.answer('Прикрепите Word-документы с примерами ваших работ!')


async def send_request_to_admin(bot: Bot, user, request_data: dict):
    user_link = f"@{user.username}" if user.username else f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"

    text = (
        f"ID: {user.id} \n"
        f"Ссылка: {user_link} \n\n"
        
        f"Имя: {request_data.get('name')} \n"
        f"☎: {request_data.get('phone_number')} \n\n"
        
        f"Работы: {', '.join(w for w in request_data.get('works'))} \n"
        f"💬: {request_data.get('works_comment') or '-'} \n\n"
        
        f"Дисциплины и специальности: {request_data.get('specialties') or '-'} \n"
        f"Иностранные языки: {request_data.get('languages') or '-'} \n"
        f"Работа с анти-плагиатом: {request_data.get('anti_plagiarism') or '-'} \n\n"
        
        f"Временная или постоянная работа: {request_data.get('main_or_part_time_job') or '-'} \n"
        f"🕐: {request_data.get('work_hours') or '-'} \n"
        f"Доп. информация: {request_data.get('additional_info') or '-'} \n"
    )

    documents = request_data.get('documents')

    work_examples = [InputMediaDocument(media=doc) for doc in documents[:-1]]
    work_examples.append(InputMediaDocument(media=documents[-1], caption=text))
    await bot.send_media_group(chat_id=REQUESTS_CHANNEL_ID, media=work_examples)


def register_specialist_registration_handlers(router: Router):
    router.message.register(handle_i_am_specialist, F.text.lower().contains('я специалист.'))

    # Ввод имени
    router.message.register(handle_name, SpecialistRegistrationStates.enter_name)
    # Ввод телефона
    router.message.register(handle_phone, SpecialistRegistrationStates.enter_phone)

    # Выбор видов работ
    router.callback_query.register(handle_work, WorkTypeCallback.filter(), SpecialistRegistrationStates.enter_works)
    # Сохранить выбор работ
    router.message.register(handle_save_works, F.text.lower().contains('готово'), SpecialistRegistrationStates.enter_works)
    # Комментарий к видам работ
    router.message.register(handle_works_comment, SpecialistRegistrationStates.enter_works_comment)

    # Дисциплины и специальности
    router.message.register(handle_specialties, SpecialistRegistrationStates.enter_specialties)
    # Языки
    router.message.register(handle_languages, SpecialistRegistrationStates.enter_languages)
    # Работа с анти-плагиатом
    router.message.register(handle_anti_plagiarism, SpecialistRegistrationStates.enter_anti_plagiarism)

    # Основная работа или подработка
    router.message.register(handle_main_or_part_time_job, SpecialistRegistrationStates.enter_main_or_part_time_job)
    # Часы работы
    router.message.register(handle_work_hours, SpecialistRegistrationStates.enter_work_hours)
    # Доп информация
    router.message.register(handle_additional_info, SpecialistRegistrationStates.enter_additional_info)
    # Примеры работ
    router.message.register(handle_work_example, SpecialistRegistrationStates.enter_work_examples)
