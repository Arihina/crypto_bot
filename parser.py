import asyncio
from pprint import pprint

import bs4
import fake_useragent
import requests

coins = None


async def fetch_data(ref, header):
    response = requests.get(ref, headers=header)
    response = response.text

    soup = bs4.BeautifulSoup(response, 'lxml')

    divs = soup.find_all('div', {"direction": "ltr"})

    coins = {}

    for div in divs:
        link_block = div.find_next('a', {"data-bn-type": "link"})
        name_block = link_block.find_next('div', {"class": "body3 line-clamp-1 truncate text-t-third css-vurnku"})
        price_block = div.find_next('div', {"class": "body2 items-center css-18yakpx"})

        link = link_block.get('href')
        name = name_block.text
        price = price_block.text

        coins[name] = (price, "https://www.binance.com" + link)

    return coins


def first_fill():
    global coins
    ref = "https://www.binance.com/ru/markets/overview/"
    header = {"user-agent": fake_useragent.UserAgent().random}
    response = requests.get(ref, headers=header)
    response = response.text

    soup = bs4.BeautifulSoup(response, 'lxml')

    divs = soup.find_all('div', {"direction": "ltr"})

    coins = {}

    for div in divs:
        link_block = div.find_next('a', {"data-bn-type": "link"})
        name_block = link_block.find_next('div', {"class": "body3 line-clamp-1 truncate text-t-third css-vurnku"})
        price_block = div.find_next('div', {"class": "body2 items-center css-18yakpx"})

        link = link_block.get('href')
        name = name_block.text
        price = price_block.text

        coins[name] = (price, "https://www.binance.com" + link)


async def parse():
    ref = "https://www.binance.com/ru/markets/overview/"
    header = {"user-agent": fake_useragent.UserAgent().random}
    global coins
    coins = await fetch_data(ref, header)
    if coins:
        pprint(coins)


async def periodic_task():
    while True:
        await parse()
        await asyncio.sleep(15)
