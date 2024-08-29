# module_14_4.py

# Домашнее задание по теме "План написания админ панели"

# Задача "Продуктовая база".

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

from crud_functions import initiate_db, get_all_products, add_products

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


# Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Рассчитать"), KeyboardButton("Информация"))
    keyboard.add(KeyboardButton("Купить"))

    await message.answer(
        "Привет! Я бот, помогающий твоему здоровью.\nНажмите 'Рассчитать', чтобы начать расчет нормы калорий.",
        reply_markup=keyboard
    )


# Кнопка "Рассчитать"
@dp.message_handler(lambda message: message.text.lower() == 'рассчитать')
async def main_menu(message: types.Message):
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(InlineKeyboardButton("Рассчитать норму калорий", callback_data='calories'),
                  InlineKeyboardButton("Формулы расчёта", callback_data='formulas'))

    await message.answer("Выберите опцию:", reply_markup=inline_kb)


# Кнопка "Формулы расчёта"
@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    formula_message = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5\n"
        "Для женщин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161"
    )
    await call.message.answer(formula_message)


# Кнопка "Рассчитать норму калорий"
@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()


# Ввод возраста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост (в см):")
    await UserState.growth.set()


# Ввод роста
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес (в кг):")
    await UserState.weight.set()


# Ввод веса
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    await message.answer("Укажите свой пол: М или Ж")
    await UserState.male.set()


# Ввод пола и расчет калорий
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


# Кнопка "Купить"
@dp.message_handler(lambda message: message.text.lower() == 'купить')
async def get_buying_list(message: types.Message):
    # Изменения в Telegram-бот:
    # В самом начале запускайте ранее написанную функцию get_all_products.
    # Измените функцию get_buying_list в модуле с Telegram-ботом,
    # используя вместо обычной нумерации продуктов функцию get_all_products.
    # Полученные записи используйте в выводимой надписи:
    # "Название: <title> | Описание: <description> | Цена: <price>"
    products = get_all_products()

    for product in products:
        long_string = f"Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}"
        image_path = f"./image{product[0]}.png"
        await message.answer_photo(photo=InputFile(image_path), caption=long_string)

    inline_kb = InlineKeyboardMarkup()
    inline_kb.row(*(InlineKeyboardButton(product[1], callback_data='product_buying') for product in products))

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_kb)


# Кнопка покупки продукта
@dp.callback_query_handler(lambda call: call.data == 'product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")


# Для неизвестных сообщений
@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
