

work_types_titles = (
    'докторские диссертации', 'кандидатские диссертации', 'аспирантские ВКР',
    'магистерские диссертации', 'дипломные работы', 'курсовые', 'отчеты по практике',
    'научные статьи', 'рефераты', 'эссе', 'презентации/речь к выступлениям',
    'контрольные (не онлайн)', 'онлайн помощь на контрольных, экзаменах, зачетах и тестах'
)

WORK_TYPES: dict[int, str] = {n: title for n, title in enumerate(work_types_titles)}
