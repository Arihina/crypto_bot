import asyncio

from telebot import types
from telebot.async_telebot import AsyncTeleBot

import data
from parser import periodic_task, first_fill


async def run():
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
                               f"Привет, интересуешься криптовалютой?\nЯ тоже, поэтому давай посмотрим, "
                               f"что тут у нас есть!\nВоспользуйся командой /help, чтобы узнать, "
                               f"какие у меня есть функции!")

    @bot.message_handler(commands=['help'])
    async def handle_start(message):
        await bot.send_message(message.chat.id,
                               f"/start - запуск работы бота\n/help - справка о"
                               f" командах бота\n/crypto - просмотр курса криптовалют\n"
                               f"/subscribe + название доступной валюты - подписка на ежедневную рассылку")

    @bot.message_handler(commands=['crypto'])
    async def send_countries(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for coin in k:
            markup.add(types.KeyboardButton(coin))

        await bot.send_message(message.chat.id, "Список криптовалют:", reply_markup=markup)

    @bot.message_handler(commands=['subscribe'])
    async def newsletter_subscribe(message):
        try:
            coin = message.text.split(' ', 1)[1]
            if coin in k:
                with open("users.txt", "a") as file:
                    file.writelines(f"{message.chat.id} {coin}\n")
                await bot.send_message(message.chat.id,
                                       f"Вы подписаны на ежедневную рассылку по криптовалюте "
                                       f"{coin}")
        except:
            await bot.send_message(message.chat.id,
                                   f"Указанной криптовалюты нет в нашем списке")

    @bot.message_handler(content_types='text')
    async def message_reply(message):
        from parser import coins as last_coins
        if message.text in last_coins:
            price, link = last_coins[message.text]
            await bot.send_message(message.chat.id, f'{message.text} — {price}\n{link}')

    tasks = [polling(), periodic_task()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(run())
