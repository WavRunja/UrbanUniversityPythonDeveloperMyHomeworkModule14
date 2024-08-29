# module_14_5.py

# Домашнее задание по теме "Написание примитивной ORM".

# Задача "Регистрация покупателей".

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

from crud_functions import initiate_db, get_all_products, add_products, add_user, is_included

# Инициализация базы данных
initiate_db()
add_products()

api = "Specify_your_API_token,_which_you_received_from_BotFather_in_Telegram"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    male = State()


# Изменения в Telegram-бот:
# Напишите новый класс состояний RegistrationState с следующими объектами класса State:
# username, email, age, balance(по умолчанию 1000).
# Создайте цепочку изменений состояний RegistrationState.
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


# Кнопки главного меню дополните кнопкой "Регистрация".
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("Рассчитать"), KeyboardButton("Информация"))
    keyboard.row(KeyboardButton("Купить"), KeyboardButton("Регистрация"))

    await message.answer(
        "Привет! Я бот, помогающий твоему здоровью.\nНажмите 'Рассчитать', чтобы начать расчет нормы калорий.",
        reply_markup=keyboard)


# Функции цепочки состояний RegistrationState:
# sing_up(message):
# Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
@dp.message_handler(lambda message: message.text.lower() == 'регистрация')
async def sing_up(message: types.Message):
    # Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    # После ожидать ввода возраста в атрибут RegistrationState.username при помощи метода set.
    await RegistrationState.username.set()


# set_username(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if is_included(username):
        # Если пользователь с таким message.text есть в таблице, то выводить
        # "Пользователь существует, введите другое имя"
        # и запрашивать новое состояние для RegistrationState.username.
        await message.answer("Пользователь существует, введите другое имя")
    else:
        await state.update_data(username=username)
        # Далее выводится сообщение "Введите свой email:"
        await message.answer("Введите свой email:")
        # и принимается новое состояние RegistrationState.email.
        await RegistrationState.email.set()


# set_email(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
@dp.message_handler(state=RegistrationState.email)
# Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
async def set_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    # Далее выводить сообщение "Введите свой возраст:":
    await message.answer("Введите свой возраст:")
    # После ожидать ввода возраста в атрибут RegistrationState.age.
    await RegistrationState.age.set()


# set_age(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
@dp.message_handler(state=RegistrationState.age)
# Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
async def set_age(message: types.Message, state: FSMContext):
    age = int(message.text)
    data = await state.get_data()
    # Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users
    # при помощи ранее написанной crud-функции add_user.
    add_user(data['username'], data['email'], age)
    await message.answer("Регистрация прошла успешно.")
    # В конце завершать приём состояний при помощи метода finish().
    await state.finish()


@dp.message_handler(lambda message: message.text.lower() == 'рассчитать')
async def main_menu(message: types.Message):
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(InlineKeyboardButton("Рассчитать норму калорий", callback_data='calories'),
                  InlineKeyboardButton("Формулы расчёта", callback_data='formulas'))

    await message.answer("Выберите опцию:", reply_markup=inline_kb)


@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    formula_message = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5\n"
        "Для женщин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161"
    )
    await call.message.answer(formula_message)


@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост (в см):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес (в кг):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    await message.answer("Укажите свой пол: М или Ж")
    await UserState.male.set()


@dp.message_handler(state=UserState.male)
async def set_male(message: types.Message, state: FSMContext):
    await state.update_data(male=message.text)
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    male = data['male']

    if male.lower() == 'м':
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
    elif male.lower() == 'ж':
        calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в сутки.")
    await state.finish()


@dp.message_handler(lambda message: message.text.lower() == 'купить')
async def get_buying_list(message: types.Message):
    products = get_all_products()

    for product in products:
        long_string = f"Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}"
        image_path = f"./image{product[0]}.png"
        await message.answer_photo(photo=InputFile(image_path), caption=long_string)

    inline_kb = InlineKeyboardMarkup()
    inline_kb.row(*(InlineKeyboardButton(product[1], callback_data='product_buying') for product in products))

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_kb)


@dp.callback_query_handler(lambda call: call.data == 'product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
