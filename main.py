import requests
import pyfiglet
import time
import socket
import json
import os
import random
from bs4 import BeautifulSoup
from termcolor import colored
from selenium import webdriver

DEBUG = True
WARNINGS = True

# Main class
class Main:
    def welcome(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        ascii_logo = pyfiglet.figlet_format("CNFS v1.0")
        print(ascii_logo)
        time.sleep(1)

    def log(message, color):
        if DEBUG is True:
            print(colored(message, color))

    def warning(message):
        if WARNINGS is True:
            print(colored(message, 'yellow'))

    def is_online(self):
        try:
            requests.get('https://google.com')
            Main.log("Success: Internet connection is available", 'green')
        except requests.ConnectionError:
            print(colored("Error: No internet connection", 'red'))

    def cnfair_look(query):
        base_url = "https://cnfair.com/gateway/mall/ep/item/list"
        current_page = 1
        total_products = 0

        # User agents list
        user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        ]

        # Bypass security checks
        headers = {'User-Agent': random.choice(user_agents),}

        while True:
            current_page = 1

            while True:
                params = {
                    'pageNum': current_page,
                    'pageSize': 48,
                    'epStatus': 1
                }

                full_url = base_url + '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
                response = requests.get(full_url, headers=headers)

                # If not 200 or 404
                if response.status_code != 200 and response.status_code != 404:
                    Main.warning('Error: Invalid response')
                    break
                elif response.status_code == 404:
                    Main.warning('Success: No more products found')
                    break

                # Parse JSON
                product_data = response.json()
                products = product_data.get('rows', [])
                
                for product in products:
                    title = product.get('goodsName', '')
                    item_id = product.get('itemNo', '')
                    goods_attr = product.get('goodsAttr', '')
                    seller = product.get('storeName', '')
                    store_source = product.get('storeSource', '')
                    price = product.get('points', '')
                    exchange_code = product.get('exchangeCode', '')

                    # Convert attributes to string (assuming it might be a list or dictionary)
                    if isinstance(goods_attr, dict):
                        goods_attr = ' '.join(goods_attr.values())  # Adjust if needed
                    elif isinstance(goods_attr, list):
                        goods_attr = ' '.join(goods_attr) 

                    search_fields = [title, seller, goods_attr]

                    if any(query.lower() in field.lower() for field in search_fields):
                        print(colored('Title: ', 'green') + colored(str(title), 'white'))
                        print(colored('Item ID: ', 'green') + colored(str(item_id), 'white'))
                        print(colored('Goods Attr: ', 'green') + colored(str(goods_attr), 'white'))
                        print('---')
                        print(colored('Seller: ', 'green') + colored(str(seller), 'white') + colored(' | Source: ', 'green') + colored(str(store_source), 'white'))
                        print(colored('Price: ', 'green') + colored(str(price), 'white'))
                        print('---')
                        print(colored('Exchange Code: ', 'red') + colored(str(exchange_code), 'white'))
                        print()
                        print()

                if not products:
                    break

                current_page += 1

    def search(self):
        print()
        query = input('\033[1mWhat phrase do you want to search for?\033[0m ' + colored('>> ', 'green'))
        print()
        Main.cnfair_look(query)


if __name__ == '__main__':
    main = Main()
    main.welcome()
    main.is_online()
    main.search()