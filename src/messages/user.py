from aiogram import html


class UserMessages:

    @staticmethod
    def get_welcome(user_name: str) -> str:
        return (
            f'Привет, {html.quote(user_name)}! \n\n'
        )

    @staticmethod
    def get_welcome_back() -> str:
        return 'С возвращением!'

    @staticmethod
    def get_ask_for_registration() -> str:
        return 'Давайте познакомимся!'

    @staticmethod
    def get_ask_for_subscribe() -> str:
        return 'Подпишитесь на каналы, чтобы получить доступ к боту:'
