from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = '8125982558:AAGmyXr1-seEDL5AzYm-Au8tuy39-oRmTIw'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Введите "Calories" что бы начать рассчет вашей нормы каллорий')

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()

@dp.message_handler(text= 'Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост(см):')
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def set_sex(message, state):
    await state.update_data(weight = message.text)
    await message.answer('Введите пол "м" или "ж":')
    await UserState.sex.set()

@dp.message_handler(state= UserState.sex)
async def send_colories(message, state):
    await state.update_data(sex = message.text)
    data = await state.get_data()
    if data["sex"] == "м":
        colories_men = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
        await message.answer(f'Ваша норма колорий: {colories_men}')
    if data["sex"] == "ж":
        colories_women = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) - 161
        await message.answer(f'Ваша норма колорий: {colories_women}')
        await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)