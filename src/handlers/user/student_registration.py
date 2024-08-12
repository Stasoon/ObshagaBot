from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.database import users
from src.database.models import StudentData
from src.misc.states import StudentRegistrationStates
from src.keyboards.user import UserKeyboards


async def handle_student(message: Message, state: FSMContext):
    await message.answer(text='Введите ваше имя:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(StudentRegistrationStates.enter_name)


async def handle_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(text='Введите ваш город:')
    await state.set_state(StudentRegistrationStates.enter_city)


async def handle_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

    await message.answer(text='В каком университете вы обучаетесь?')
    await state.set_state(StudentRegistrationStates.enter_university)


async def handle_university(message: Message, state: FSMContext):
    await state.update_data(university=message.text)

    await message.answer(text='На каком курсе вы учитесь?')
    await state.set_state(StudentRegistrationStates.enter_course)


async def handle_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)

    await message.answer(text='Ввведите вашу специальность:')
    await state.set_state(StudentRegistrationStates.enter_speciality)


async def handle_speciality(message: Message, state: FSMContext):
    await state.update_data(speciality=message.text)

    await message.answer(text='Перечислите ваши любимые предметы:')
    await state.set_state(StudentRegistrationStates.enter_favourite_subjects)


async def handle_favourite_subjects(message: Message, state: FSMContext):
    await state.update_data(favourite_subjects=message.text)

    await message.answer(text='Перечислите ваши НЕлюбимые предметы:')
    await state.set_state(StudentRegistrationStates.enter_unloved_subjects)


async def handle_unloved_subjects(message: Message, state: FSMContext):
    await state.update_data(unloved_subjects=message.text)

    await message.answer(
        text='Спасибо за ваши ответы! \n\nТеперь вам доступны материалы бота:',
        reply_markup=UserKeyboards.get_main_menu()
    )

    data = await state.get_data()
    await state.clear()

    user = users.get_user_or_none(telegram_id=message.from_user.id)
    user.is_registration_passed = True
    user.save()

    StudentData.create(
        user=user, name=data.get('name'),
        city=data.get('city'), university=data.get('university'),
        course=data.get('course'), speciality=data.get('speciality'),
        favourite_subjects=data.get('favourite_subjects'),
        unloved_subjects=data.get('unloved_subjects')
    )


def register_student_registration_handlers(router: Router):
    router.message.register(handle_student, F.text.lower().contains('я студент.'))

    router.message.register(handle_name, StudentRegistrationStates.enter_name)
    router.message.register(handle_city, StudentRegistrationStates.enter_city)
    router.message.register(handle_university, StudentRegistrationStates.enter_university)
    router.message.register(handle_course, StudentRegistrationStates.enter_course)
    router.message.register(handle_speciality, StudentRegistrationStates.enter_speciality)
    router.message.register(handle_favourite_subjects, StudentRegistrationStates.enter_favourite_subjects)
    router.message.register(handle_unloved_subjects, StudentRegistrationStates.enter_unloved_subjects)
