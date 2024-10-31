import re

def remove_russian_mat(words):
    russian_mat = [
        'блин', 'черт', 'сучка', 'мать', 'пизда', 'хуй', 'ебать', 'бля', 'гандон', 'впизду', "уебан", "ебать", "блять", "нихуя", "ебать", "заебать", "нахуй", "заебись", "сука", "пизда", "похуй"  ]

    mat_pattern = re.compile(r'\b(' + '|'.join(russian_mat) + r')\b', re.IGNORECASE)
    filtered_words = [word for word in words if not mat_pattern.search(word)]

    return filtered_words