from typing import Iterable

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardBuilder

from src.database.models import Category, Subcategory, ChannelToSubscribe
from src.misc.callback_factories import WorkTypeCallback, SubcategoryCallback
from src.misc.enums import WORK_TYPES


class UserKeyboards:

    @staticmethod
    def get_choose_role() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text='👨‍🏫 Я специалист. Хочу в команду')
        builder.button(text='👨‍🎓 Я студент. Хочу полезные материалы')
        builder.adjust(1)
        return builder.as_markup(resize_keyboard=True, is_persistent=True)

    @staticmethod
    def get_check_subscription(channels_to_sub: Iterable[ChannelToSubscribe]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for channel in channels_to_sub:
            builder.button(text=channel.title, url=channel.url)
        builder.button(text='Проверить подписку ✅', callback_data='check_subscription')

        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def get_phone() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text='📞 Отправить мой номер', request_contact=True)
        return builder.as_markup(resize_keyboard=True, is_persistent=True)

    @staticmethod
    def get_done() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text='Готово')
        return builder.as_markup(resize_keyboard=True, is_persistent=True)

    @staticmethod
    def get_skip() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text='Пропустить ➡️')
        return builder.as_markup(resize_keyboard=True, is_persistent=True)

    @staticmethod
    def get_works_types(marked_works: list[int] = None) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        if not marked_works:
            marked_works = []

        for work_id, work_title in WORK_TYPES.items():
            text = f"{work_title} ✅" if work_id in marked_works else work_title
            builder.button(text=text, callback_data=WorkTypeCallback(work_id=work_id))

        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def get_anti_plagiarism() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()

        builder.button(text='Да')
        builder.button(text='Нет')
        builder.button(text='Только с бесплатным')

        builder.adjust(2)
        return builder.as_markup(resize_keyboard=True, is_persistent=True)

    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()

        for category in Category.select():
            builder.button(text=category.title)

        builder.adjust(1)
        return builder.as_markup(resize_keyboard=True, is_persistent=True)

    @staticmethod
    def get_category(subcategories: list[Subcategory]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for n, s in enumerate(subcategories, start=1):
            builder.button(text=f"{s.title}", callback_data=SubcategoryCallback(code=s.id))

        builder.adjust(1)
        return builder.as_markup()

