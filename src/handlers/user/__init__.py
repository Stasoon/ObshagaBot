from aiogram import Router

from .menu import register_menu_handlers
from .start_command import register_start_command_handler
from .student_registration import register_student_registration_handlers
from .specialist_registration import register_specialist_registration_handlers


def register_user_handlers(router: Router):
    registration_functions = [
        register_start_command_handler,
        register_student_registration_handlers,
        register_specialist_registration_handlers,
        register_menu_handlers
    ]

    for func in registration_functions:
        func(router)
