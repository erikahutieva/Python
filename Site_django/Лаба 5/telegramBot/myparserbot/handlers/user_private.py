from aiogram import types, Router
from aiogram.filters import CommandStart
from myparserbot.parser import get_prices, resault_to_str

user_private_Router = Router()

@user_private_Router.message(CommandStart())
async def start(message: types.Message) -> None:
    await message.answer("Ты нажал на команду 'start'")


@user_private_Router.message()
async def parse(message: types.Message) -> None:
    # await message.answer(message.text)
    URL = r"https://www.cbr.ru/currency_base/daily/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    prices = get_prices(URL, headers)
    for currency in prices:
        if currency[0] == message.text.upper():
            await message.answer(f"{currency[0]} - {currency[1]}₽")
            break
    else:
        await message.answer(resault_to_str(prices))