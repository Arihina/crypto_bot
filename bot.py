import asyncio

from telebot import types
from telebot.async_telebot import AsyncTeleBot

import config
from parser import periodic_task, first_fill
from sender import get_receiver


async def run():
    first_fill()
    from parser import coins
    parser_data = coins
    k = list(parser_data.keys())
    bot = AsyncTeleBot(config.token)

    async def polling():
        await bot.polling(none_stop=True)

    async def sender():
        while True:
            async for receiver in get_receiver():
                from parser import coins
                price, link = coins[receiver[1]]
                await bot.send_message(receiver[0], f'Mailing: {receiver[1]} — {price}\n{link}')
            await asyncio.sleep(28800)

    @bot.message_handler(commands=['start'])
    async def handle_start(message):
        await bot.send_message(message.chat.id,
                               f"Hi, are you interested in cryptocurrency?\nMe too, so let's see, "
                               f"what we have here.\nUse the command /help, to find out "
                               f"what functions I have")

    @bot.message_handler(commands=['help'])
    async def handle_start(message):
        await bot.send_message(message.chat.id,
                               f"/start - starting the bot\n/help - information about"
                               f" bot commands\n/crypto - viewing the cryptocurrency exchange rate\n"
                               f"/subscribe + name of the available currency - subscribe to the daily newsletter "
                               f"(3 times a day)")

    @bot.message_handler(commands=['crypto'])
    async def send_countries(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for coin in k:
            markup.add(types.KeyboardButton(coin))

        await bot.send_message(message.chat.id, "List of cryptocurrencies:", reply_markup=markup)

    @bot.message_handler(commands=['subscribe'])
    async def newsletter_subscribe(message):
        try:
            coin = message.text.split(' ', 1)[1]
            if coin in k:
                with open("users.txt", "a") as file:
                    file.writelines(f"{message.chat.id} {coin}\n")
                await bot.send_message(message.chat.id,
                                       f"You have subscribed to the daily cryptocurrency newsletter "
                                       f"{coin}")
        except:
            await bot.send_message(message.chat.id,
                                   f"The specified cryptocurrency is not on our list")

    @bot.message_handler(content_types='text')
    async def message_reply(message):
        from parser import coins as last_coins
        if message.text in last_coins:
            price, link = last_coins[message.text]
            await bot.send_message(message.chat.id, f'{message.text} — {price}\n{link}')

    tasks = [polling(), periodic_task(), sender()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(run())
