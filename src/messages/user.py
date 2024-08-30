from aiogram import html


class UserMessages:

    @staticmethod
    def get_welcome(user_name: str) -> str:
        return (
            f"<b>Привет, сообщество «Общага» на связи</b> 🙌 \n\n"
            
            f"Этот бот будет полезен каждому студенту! \n\n"
            
            "Мы собрали полезные материалы для учебы: «гайд по поднятию оригинальности», "
            "«шаблон оформления курсовой» и многое другое! \n\n"
            
            "Также в нашем боте найдешь: нейросети для учебы, гайды по "
            "устройству на работу и заработку для студентов! \n\n"
            
            "Запускай бота, заполняй анкету и пользуйся всеми материалами БЕСПЛАТНО🤝"
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

    @staticmethod
    def get_section_in_dev() -> str:
        return 'Этот раздел находится в разработке!'
