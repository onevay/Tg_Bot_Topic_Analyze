from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, FSInputFile
from aiogram import filters
from aiogram.enums import ParseMode
import app.db as db
import topic_funcs.gensi as gn
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import re
import topic_funcs.vizualize as viz
import topic_funcs.probably as prob
import topic_funcs.textb as req
from decouple import config


db_url = config('DB_URL')
host = config('HOST')
port = config('PORT')
user = config('USER')
password = config('PASSWORD')
database = config('DB_NAME')
import app.keyboard as kb

router = Router()
test_dict = {}

def age_check(n: str):
    if n.isdigit():
        return True
    else:
        return False

def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None

class UserData(StatesGroup):
    name: str = State()
    age: int | None = State()
    aim: str = State()
    gender: str | None = State()

class TopicAnalize(StatesGroup):
    start_analize: str = State()
    choice_rezult = State()

@router.message(filters.CommandStart())
async def start_bot(message: Message):
    await message.answer(text='Привет!😁')
    await message.answer(text='Ты, наверное, знаешь цели нашего бота🙂,\n'
                         'но команда /help все равно может тебе помочь')
    await message.answer(text='Перед использованием функционала обязательно нужно пройти анкетирование🙂\n'
                         'Мы не передаем данные, они останутся между нами (для статистики)', reply_markup=kb.ancet_start)

@router.message(filters.Command('help'))
async def help(message: Message):
    await message.answer(
        text=f'📚 *Доступные команды:*  \n\n'
             f'🔹 /start - *начать пользоваться ботом*  \n'
             f'🔹 /help - *все объяснит*  \n'
             f'🔹 /ancet_fill - *заполнить анкету*  \n'
             f'🔹 /start_topic - *анализ текста*',
        parse_mode=ParseMode.MARKDOWN_V2
    )

@router.message(filters.Command('start_topic'))
async def start_topic(message: Message):
    await message.answer(text=f'🚀*Запуск анализа темы\!*', parse_mode=ParseMode.MARKDOWN_V2, reply_markup=kb.topic_start)

@router.message(filters.Command('ancet_fill'))
async def ancet_fill(message: Message):
    await message.answer(
        text=f'📝 *Вы можете заполнить анкету:*  \n'
             f'☝️*С нуля*  \n'
             f'✌️*Обновить данные в ней*',
        reply_markup=kb.ancet_start,
        parse_mode=ParseMode.MARKDOWN_V2
    )

@router.callback_query(F.data == 'anceta')
async def cl_ancet_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f'📝 *Давай приступим\!\n*'
                                  f'🤔 *Как тебя зовут?*', parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(UserData.name)
    await callback.answer()

@router.message(F.text, UserData.name)
async def get_name(message: Message, state: FSMContext):
    await message.answer(text=f'Так, {message.text}, а сколько тебе лет?😶')
    await state.update_data(name=message.text)

    await state.set_state(UserData.age)

@router.message(UserData.name)
async def get_name_e(message: Message):
    await message.answer(
        text=f'❌ *Ошибка\!*  \n'
             f'🤷‍♂️ *Ты явно ткнул не туда\.*  \n'
             f'🔄 *Попробуй сделать все правильно и введи свое имя\!*',
        parse_mode=ParseMode.MARKDOWN_V2)

@router.message(F.text, UserData.age)
async def get_age(message: Message, state: FSMContext):
    if age_check(message.text):
        await state.update_data(age=extract_number(message.text))
        procent = db.age_procent(message.text)
        await message.answer(
            text=f'🎉 *Посчитали и поняли\!*  \n'
                 f'📊 *Ваш возраст совпадает с {procent}% наших пользователей\.*',
            parse_mode=ParseMode.MARKDOWN_V2
        )
        await message.answer(
            text=f'🤔 *С возрастом определились, неплохо бы еще и гендер узнать\.*',
            reply_markup=kb.gen_button,
            parse_mode=ParseMode.MARKDOWN_V2
        )
        await state.set_state(UserData.gender)
    else:
        await message.answer(
            text=f'❌ *Не похоже на правду\!*  \n'
                 f'😕 *Может, ты неправильно вводишь? Попробуй еще раз\.*',
            parse_mode=ParseMode.MARKDOWN_V2
        )

@router.message(UserData.age)
async def get_age_e(message: Message):
    await message.answer(text='Что это ты отправляешь? Нужен возраст')

@router.message(F.text.in_(['👩🏻 Женщина', '👨🏻 Мужчина']), UserData.gender)
async def get_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text[2:].lower())
    procent = db.gender_procent(message.text[2:])
    await message.answer(
        text=f'🎉 *Класс\!*  \n'
             f'🤝 *Твой пол совпадает с полом {procent}% наших пользователей\.*',
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await message.answer(
        text=f'💬 *Расскажи, почему решил пользоваться нашим сервисом?*',
        reply_markup=kb.air_foul,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(UserData.aim)

@router.message(UserData.gender)
async def get_gender_e(message: Message):
    await message.answer(
        text=f'❌ *Не знаю такого гендера\!*  \n'
             f'👉 Пожалуйста, выбери из предложенного списка\.',
        parse_mode=ParseMode.MARKDOWN_V2)

@router.message(F.text, UserData.aim)
async def get_air(message: Message, state: FSMContext):
    await state.update_data(aim=message.text)
    db.insert(message.chat.id, await state.get_data())
    test_dict = db.print_data(message.chat.id)
    await message.answer(
        text=f'📋 *Проверьте, всё ли верно:*  \n\n'
             f'👱🎤 *Имя:* {test_dict[0]}  \n'
             f'🕒 *Возраст:* {test_dict[1]}  \n'
             f'🚻 *Пол:* {test_dict[2]}  \n'
             f'💬 *Почему решили пользоваться:* {test_dict[3]}',
        reply_markup=kb.check_data,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.clear()

@router.message(UserData.aim)
async def get_air_e(message: Message):
    await message.answer(
        text=f'❌ *Разве это цель?*  \n'
             f'📝 Пожалуйста, введи корректные данные\!',
        reply_markup=kb.air_foul,
        parse_mode=ParseMode.MARKDOWN_V2
    )

@router.callback_query(F.data == 'air_foul', UserData.aim)
async def air_foul(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=f'😔 *Жаль, что не расскажешь\.\.\.*  \n'
    )
    await state.update_data(aim=callback.message.text)
    db.insert(callback.message.chat.id, await state.get_data())
    test_dict = db.print_data(callback.message.chat.id)

    await callback.message.answer(
        text='📋 *Проверьте, всё ли верно:*  \n\n'
             f'👱‍🎤 *Имя:* {test_dict[0]}  \n'
             f'🕒 *Возраст:* {test_dict[1]}  \n'
             f'🚻 *Пол:* {test_dict[2]}  \n',
        reply_markup=kb.check_data,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await callback.answer()
    await state.clear()

@router.callback_query(F.data == 'correct')
async def correct(callback: CallbackQuery):
    await callback.message.answer(
        text=f'🎉 *Класс\!*  \n'
             f'🚀 *Самое время воспользоваться функционалом\!*',
        reply_markup=kb.topic_start,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await callback.answer()

@router.callback_query(F.data == 'incorrect')
async def incorrect(callback: CallbackQuery, state: FSMContext):
    db.delete_user(callback.message.chat.id)
    await callback.message.answer(
        text=f'🔄 *Шило на мыло\.\.\. То есть, введи своё имя:*',
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(UserData.name)
    await callback.answer()

@router.callback_query(F.data == 'topic_start')
async def topic_start(callback: CallbackQuery, state: FSMContext):
    if not db.check_primary(callback.message.chat.id):
        await callback.message.answer(
        text=f'📄 *Отправь мне файл для анализа\.*  \n'
             f'⚠️ *Файл, кстати, должен быть в CSV формате\.*',
        parse_mode=ParseMode.MARKDOWN_V2
    )
        await state.set_state(TopicAnalize.start_analize)

    else:
        await callback.message.answer(
            text=f'❗️ *Не вижу анкету от тебя,*  \n'
                 f'📝 *нужно это исправить\!*',
            reply_markup=kb.ancet_start,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    await callback.answer()

@router.message(F.document, TopicAnalize.start_analize)
async def analyze(message: Message, state: FSMContext):
    global res, lda_model, them_count, mydict, corpus, st
    if '.csv' in message.document.file_name:
        await message.answer(text=f'✅ *Принял, обрабатываю\.\.\.*', parse_mode=ParseMode.MARKDOWN_V2)
        await message.bot.download(message.document.file_id, destination='../csv.csv')

        with open('../TG_BOT/tgbot/csv.csv') as f:
            st1 = f.read()

        res, lda_model, them_count, mydict, corpus, st = gn.start(st1)

        await message.answer(text=f'🔍 *Анализ завершен:*  \n{res}', reply_markup=kb.rezult_choice, parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(TopicAnalize.choice_rezult)
    else:
        await message.answer(text=f'❌ *Видимо, файл не того формата\.*  \n'
                                  f'📄 *Попробуй снова с CSV файлом\!*', parse_mode=ParseMode.MARKDOWN_V2)

@router.message(TopicAnalize.start_analize)
async def analyze_e(message: Message):
    await message.reply(text=f'❗️ *Ты неправильно пользуешься ботом\.\.\. Одумайся\!*', parse_mode=ParseMode.MARKDOWN_V2)

@router.message(F.text.startswith('✅Диаг'), TopicAnalize.choice_rezult)
async def show_res(message: Message):
    if message.text[-1] == '1':
        if them_count <= 6:
            viz.plot_topic_distribution(lda_model, 3)
        else:
            viz.plot_topic_distribution(lda_model, 4)
        await message.answer_photo(photo=FSInputFile('../res1.png'),
                                   caption=f'📊 *Здесь представлены самые значимые слова каждой смысловой группы\.*', parse_mode=ParseMode.MARKDOWN_V2)
    else:
        prob.probably_topics(lda_model, mydict, them_count)
        await message.answer_photo(photo=FSInputFile('../res2.png'),
                                   caption=f'📈 *Значимость каждой подтемы в общем массиве ответов\.*', parse_mode=ParseMode.MARKDOWN_V2)

@router.message(F.text.startswith('📝Пол'), TopicAnalize.choice_rezult)
async def full_list(message: Message):
    await message.answer(text=f'📄 Полный список твоих ответы:  \n{st}')

@router.message(F.text.startswith('❌Вых'), TopicAnalize.choice_rezult)
async def exit_analysis(message: Message, state: FSMContext):
    await message.answer(text=f'🚪 *Вы вышли из режима анализа\.*', reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN_V2)
    await message.answer(text=f'😊 *Но не огорчайтесь, вы всегда можете вернуться к использованию\!*',
                         reply_markup=kb.topic_start, parse_mode=ParseMode.MARKDOWN_V2)
    await state.clear()

@router.message(F.text.startswith('🚀Зап'), TopicAnalize.choice_rezult)
async def gpt_request(message: Message):
    await message.answer(text=f'🚀 Запрос отправлен, ожидайте результата')
    await message.answer(text=req.get_answer(st))

@router.message(TopicAnalize.choice_rezult)
async def state_e(message: Message):
    await message.answer(text=f'❓ *Для продолжения необходимо выбрать действие или выйти из данного режима*', parse_mode=ParseMode.MARKDOWN_V2)

@router.message(F.text, F.document, F.emoji, F.photo)
async def any_text(message: Message):
    await message.answer(
        text=f'❌ *Такое я не обрабатываю\!*  \n'
             f'📜 *Используй /help, чтобы просмотреть доступные команды\.*',
        parse_mode=ParseMode.MARKDOWN_V2
    )