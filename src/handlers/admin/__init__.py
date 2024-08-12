from aiogram import Router

from .admin_menu import register_admin_menu_handlers
from .edit_content import register_admin_edit_content_handlers
from .statistic import register_admin_statistic_handlers
from .mailing import register_mailing_handlers
from .subscriptions import register_necessary_subscriptions_handlers


def register_admin_handlers(router: Router):
    register_admin_menu_handlers(router)
    register_admin_statistic_handlers(router)
    register_mailing_handlers(router)
    register_admin_edit_content_handlers(router)
    register_necessary_subscriptions_handlers(router)
