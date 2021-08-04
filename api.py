#!/usr/bin/python3

import configparser
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from tabulate import tabulate

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')
API_KEY=str(config.get('API_KEY', 'KEY'),)


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
	'symbol':'BTC,ETH,XRP,LTC,XMR,MIOTA,ETC,ADA'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': API_KEY,
}
 
session = Session()
session.headers.update(headers)


url_usd = 'https://www.cbr-xml-daily.ru/daily_json.js'
session_usd = Session()
response_usd = session.get(url_usd)
json_data_usd = json.loads(response_usd.text)
dollar = float(json_data_usd["Valute"]["USD"]["Value"])

carrency_dict = {
  'BTC': 0.10147135,
  'ETH': 1.17869503,
  'LTC': 0.37962,
  'XMR': 0.597168065,
  'XRP': 135,
  'ETC': 5.035,
  'ADA': 0.999,
  'MIOTA': 30.968
}

total_rub = 0
total_usd = 0
table_list = []

try:
  response = session.get(url, params=parameters)
  json_data = json.loads(response.text)
   
 
  for currency_code in carrency_dict:
    price = json_data['data'][currency_code]['quote']['USD']['price']
    amount = carrency_dict[currency_code]
    price_usd_amount = price * amount
    price_rub_amount = price_usd_amount * dollar
    total_rub = price_rub_amount + total_rub
    total_usd = price_usd_amount + total_usd

    table_tuple = (currency_code, price, amount, price_usd_amount, price_rub_amount)
    table_list = table_list + [table_tuple]

  columns = ['Код', 'Цена', 'Количество', 'Сумма USD', 'Сумма RUB']
  print(tabulate(table_list, tablefmt="grid", headers=columns, floatfmt=("",".2f", "",".2f",".2f")))

  print('Курс доллара: '+str(dollar))
  print('Всего в долларах: '+str(round(total_usd, 2)))
  print('Всего в рублях: '+str(round(total_rub, 2)))

   
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
  