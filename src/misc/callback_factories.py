from aiogram.filters.callback_data import CallbackData


class WorkTypeCallback(CallbackData, prefix='work_type'):
    work_id: int


class SubcategoryCallback(CallbackData, prefix='subcategory'):
    code: int

