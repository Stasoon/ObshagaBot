from aiogram.fsm.state import StatesGroup, State


class SpecialistRegistrationStates(StatesGroup):
    enter_name = State()
    enter_phone = State()

    enter_works = State()
    enter_works_comment = State()

    enter_specialties = State()
    enter_languages = State()
    enter_anti_plagiarism = State()

    enter_main_or_part_time_job = State()
    enter_work_hours = State()
    enter_additional_info = State()
    enter_work_examples = State()


class StudentRegistrationStates(StatesGroup):
    enter_name = State()
    enter_city = State()
    enter_university = State()
    enter_course = State()
    enter_speciality = State()
    enter_favourite_subjects = State()
    enter_unloved_subjects = State()


class EditContentStates(StatesGroup):
    enter_new_content = State()
