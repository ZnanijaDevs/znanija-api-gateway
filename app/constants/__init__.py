# pylint: disable=line-too-long
BRAINLY_SUBJECTS = [{"id":"59","name":"Уход за собой"},{"id":"29","name":"Математика"},{"id":"17","name":"Литература"},{"id":"30","name":"Алгебра"},{"id":"16","name":"Русский язык"},{"id":"31","name":"Геометрия"},{"id":"33","name":"Английский язык"},{"id":"10","name":"Химия"},{"id":"9","name":"Физика"},{"id":"3","name":"Биология"},{"id":"42","name":"Другие предметы"},{"id":"13","name":"История"},{"id":"15","name":"Обществознание"},{"id":"46","name":"Окружающий мир"},{"id":"8","name":"География"},{"id":"37","name":"Українська мова"},{"id":"32","name":"Информатика"},{"id":"41","name":"Українська література"},{"id":"44","name":"Қазақ тiлi"},{"id":"22","name":"Экономика"},{"id":"48","name":"Музыка"},{"id":"25","name":"Право"},{"id":"49","name":"Технология"},{"id":"43","name":"Беларуская мова"},{"id":"47","name":"Французский язык"},{"id":"45","name":"Немецкий язык"},{"id":"50","name":"Черчение"},{"id":"51","name":"МХК"},{"id":"52","name":"ОБЖ"},{"id":"53","name":"Психология"},{"id":"54","name":"Оʻzbek tili"},{"id":"55","name":"Кыргыз тили"},{"id":"56","name":"Астрономия"},{"id":"57","name":"Физкультура и спорт"},{"id":"58","name":"ЕГЭ / ОГЭ"}]
SUBJECT_IDS = [3,8,9,10,13,15,16,17,22,25,29,30,31,32,33,37,41,42,43,44,45,46,47,48,51,52,53,54,55,56,57]

DISALLOWED_RANKS_FOR_ACTIVE_USERS = ['новичок', 'середнячок', 'хорошист']
MIN_ANSWERS_COUNT_FOR_ACTIVE_USER = 75
SUBJECTS_IDS_FOR_ACTIVE_USERS = [3,8,9,10,13,15,16,17,25,29,30,31,32,33,37,41,42,44,45,46,48,52,53,54]

RANKING_TYPES = ['WEEKLY', 'MONTHLY', 'THREE_MONTH']
DEFAULT_USER_AVATAR = 'https://znanija.com/img/avatars/100-ON.png'
DELETED_USER_DATA = {
    "id": 0,
    "nick": "Аккаунт удалён",
    "rank": "",
    "avatar": "https://znanija.com/img/avatars/100-ON.png",
    "created": "1970-01-01T00:00:00+04:00",
    "gender": "MALE",
    "special_ranks": [],
    "is_deleted": True
}
DELETED_ACCOUNT_NICK = 'Аккаунт удален'

SPAMOUTS_RANKS_REGEX = r"spamout|антиспамер|старший спамаут"
SPAMOUTS_AND_MODS_RANKS_REGEX = r"spamout|антиспамер|старший спамаут|модератор"
EXCLUDE_MODERATORS_FROM_MODS_LIST = [3149887, 964920, 171544, 1348713, 7686708, 14388546, 4589768, 9406673]
