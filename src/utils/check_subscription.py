from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import AiogramError
from loguru import logger

from src.database.channels_to_subscribe import get_channels


async def check_status_in_channel_is_member(bot: Bot, channel_id: int, user_id: int) -> bool:
    try:
        user = await bot.get_chat_member(channel_id, user_id)
    except AiogramError as e:
        logger.exception(e)
        return True

    if user.status != ChatMemberStatus.LEFT:
        return True
    return False


async def get_not_subscribed_channels(bot, user_id):
    not_subbed_channels = [
        channel for channel in get_channels()
        if not await check_status_in_channel_is_member(bot, channel.channel_id, user_id)
    ]
    return not_subbed_channels

