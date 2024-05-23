import asyncio

from telebot import types
from telebot.async_telebot import AsyncTeleBot

import data
from parser import periodic_task, first_fill


async def run_bot_and_parser():
    first_fill()
    from parser import coins
    parser_data = coins
    k = list(parser_data.keys())
    bot = AsyncTeleBot(data.token)

    async def polling():
        await bot.polling(none_stop=True)

    @bot.message_handler(commands=['start'])
    async def handle_start(message):
        await bot.send_message(message.chat.id,
                               f"Привет, интересуешься криптовалютой?\nЯ тоже, поэтому давай посмотрим, что тут у нас есть!\nВоспользуйся командой /help, чтобы узнать, какие у меня есть функции!")

    @bot.message_handler(commands=['help'])
    async def handle_start(message):
        await bot.send_message(message.chat.id,
                               f"/start - запуск работы бота\n/help - справка о командах бота\n/crypto - просмотр курса криптовалют")

    @bot.message_handler(commands=['crypto'])
    async def send_countries(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for coin in k:
            markup.add(types.KeyboardButton(coin))

        await bot.send_message(message.chat.id, "Список криптовалют:", reply_markup=markup)

    @bot.message_handler(content_types='text')
    async def message_reply(message):
        from parser import coins as last_coins
        if message.text in last_coins:
            price, link = last_coins[message.text]
            await bot.send_message(message.chat.id, f'{message.text} — {price}\n{link}')

    tasks = [polling(), periodic_task()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(run_bot_and_parser())
