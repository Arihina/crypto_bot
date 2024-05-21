from pprint import pprint

import bs4
import fake_useragent
import grequests

ref = "https://www.binance.com/ru/markets/overview/"
header = {"user-agent": fake_useragent.UserAgent().random}

response = grequests.get(ref, headers=header)
response = grequests.map([response])[0]

if response.status_code == 200:
    response = response.text
else:
    print("Ошибка при выполнении запроса:", response.status_code)


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

pprint(coins)
