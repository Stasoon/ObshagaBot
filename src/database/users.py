from datetime import datetime, timedelta
from typing import Generator

from peewee import DoesNotExist

from .models import User
# from .reflinks import increase_users_count


# region SQL Create

def create_or_update_user(
        telegram_id: int, firstname: str, username: str = None, reflink: str = None
) -> tuple[bool, User]:
    user = get_user_by_telegram_id_or_none(telegram_id)

    if user:
        user.name = firstname
        user.username = username
        user.is_bot_blocked = False
        user.save()
        return False, user
    else:
        user = User.create(
            name=firstname, telegram_id=telegram_id, username=username, referral_link=reflink
        )
        # increase_users_count(reflink=reflink)
        return True, user


# endregion


# region SQL Select

def get_user_or_none(telegram_id: int) -> User | None:
    return User.get_or_none(User.telegram_id == telegram_id)


def get_users_total_count() -> int:
    return User.select().count()


def get_online_users_count(minutes_threshold=15) -> int:
    threshold_time = datetime.now() - timedelta(minutes=minutes_threshold)
    return User.select().where(User.last_activity >= threshold_time).count()


def get_users_registered_within_hours_count(hours: int) -> int:
    start_time = datetime.now() - timedelta(hours=hours)
    users_count = User.select().where(User.registration_timestamp >= start_time).count()

    return users_count


def get_user_lang_code(telegram_id: int) -> str | None:
    user = get_user_by_telegram_id_or_none(telegram_id)
    lang_code = user.lang_code if user else None
    return lang_code


def get_user_ids() -> Generator[int, any, any]:
    yield from (user.telegram_id for user in User.select())


def get_all_users() -> Generator[User, any, any]:
    """ Возвращает генератор с пользователями """
    yield from (user for user in User.select())


def get_user_by_telegram_id_or_none(telegram_id: int) -> User | None:
    try:
        user = User.get(User.telegram_id == telegram_id)
        return user
    except DoesNotExist:
        return None


# endregion


def update_last_activity(user_id: int, new_activity_timestamp: datetime):
    user = User.get_or_none(User.telegram_id == user_id)
    if user:
        user.last_activity = new_activity_timestamp
        user.save()

