from datetime import datetime
from peewee import (
    Model, PostgresqlDatabase, SqliteDatabase, AutoField,
    SmallIntegerField, BigIntegerField, IntegerField,
    DateTimeField, CharField, TextField, BooleanField,
    ForeignKeyField, Field, ManyToManyField
)


db = SqliteDatabase(
    database='data.db'
    # DatabaseConfig.NAME,
    # user=DatabaseConfig.USER, password=DatabaseConfig.PASSWORD,
    # host=DatabaseConfig.HOST, port=DatabaseConfig.PORT
)


class EnumField(Field):
    def __init__(self, enum_class, *args, **kwargs):
        self.enum_class = enum_class
        super(EnumField, self).__init__(*args, **kwargs)

    def db_value(self, value):
        return value.value if value is not None else None

    def python_value(self, value):
        if value is not None:
            return self.enum_class(value)
        return None


class _BaseModel(Model):
    class Meta:
        database = db


class User(_BaseModel):
    """ Пользователь бота """
    class Meta:
        db_table = 'users'

    telegram_id = BigIntegerField(primary_key=True, unique=True, null=False)
    name = CharField(default='Пользователь')
    username = CharField(null=True, default=None)

    last_activity = DateTimeField(default=datetime.now)
    registration_timestamp = DateTimeField(default=datetime.now)
    is_registration_passed = BooleanField(default=False)
    is_bot_blocked = BooleanField(default=False)


class StudentData(_BaseModel):
    class Meta:
        db_table = 'students_data'

    user = ForeignKeyField(model=User, primary_key=True, on_delete='CASCADE')
    name = CharField()
    city = CharField()
    university = CharField()
    course = CharField()
    speciality = CharField()
    favourite_subjects = TextField()
    unloved_subjects = TextField()


class Category(_BaseModel):
    class Meta:
        db_table = 'categories'

    code_name = CharField(primary_key=True)
    title = CharField()


class Subcategory(_BaseModel):
    class Meta:
        db_table = 'subcategories'

    id = AutoField()
    category = ForeignKeyField(model=Category)
    title = CharField()


class SubcategoryContent(_BaseModel):
    class Meta:
        db_table = 'subcategories_content'

    subcategory = ForeignKeyField(model=Subcategory)
    chat_id = BigIntegerField()
    message_id = BigIntegerField()


class ChannelToSubscribe(_BaseModel):
    """" Канал для обязательной подписки """
    class Meta:
        db_table = 'channels_to_subscribe'

    channel_id = BigIntegerField()
    title = CharField()
    url = CharField()


class Admin(_BaseModel):
    """ Администратор бота """
    class Meta:
        db_table = 'admins'

    telegram_id = BigIntegerField(unique=True, null=False)
    name = CharField()


def register_models() -> None:
    for model in _BaseModel.__subclasses__():
        model.create_table()
