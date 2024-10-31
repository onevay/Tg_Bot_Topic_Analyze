from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

topic_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🚀 Запустить выделитель топиков', callback_data='topic_start')]
    ]
)

ancet_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📝 Пройти анкету', callback_data='anceta')],
    [InlineKeyboardButton(text='🚀 Запустить выделитель топиков', callback_data='topic_start')]
])

check_data = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Все верно", callback_data='correct')],
        [InlineKeyboardButton(text="❌ Заполнить сначала", callback_data='incorrect')]
    ]
)

air_foul = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🙅‍♂️ Не хочу рассказывать', callback_data='air_foul')]
    ]
)

gen_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👩🏻 Женщина')],
        [KeyboardButton(text='👨🏻 Мужчина')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='🤔 Выберите ваш пол')

rezult_choice = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='✅Диаграмма 1'), KeyboardButton(text='✅Диаграмма 2')],
    [KeyboardButton(text='🚀Запрос в ChatGPT'), KeyboardButton(text='📝Полный список')],
    [KeyboardButton(text='❌Выход')]
], resize_keyboard=True, input_field_placeholder='Выберите действие')