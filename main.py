import requests
import pyfiglet
import time
import os
import random
from termcolor import colored


# Main class
class CNFS:
    def __init__(self, debug=True, warnings=True):
        self.debug = debug
        self.warnings = warnings


    @staticmethod
    def welcome():
        os.system('cls' if os.name == 'nt' else 'clear')
        ascii_logo = pyfiglet.figlet_format("CNFS v1.0")
        print(ascii_logo)
        time.sleep(1)

    def log(self, message, color):
        if self.debug is True:
            print(colored(message, color))

    def warning(self, message):
        if self.warnings is True:
            print(colored(message, 'yellow'))

    @staticmethod
    def is_online():
        try:
            requests.get('https://google.com')
        except requests.ConnectionError:
            try:
                requests.get('https://bing.com')
            except requests.ConnectionError:
                print(colored('Error: No internet connection', 'red'))
                exit()

    def cnfair_look(self):
        base_url = "https://cnfair.com/gateway/mall/ep/item/list"
        current_page = 1

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

        # DNT headers list
        dnt_headers = ['0', '1']

        # Keep-alive headers list
        keep_alive_headers = ['keep-alive', 'close']

        # Upgrade-Insecure-Requests headers list
        uir_headers = ['0', '1']

        while True:
            current_page = 1

            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept': '*/*',  # Accept all content types
                'Accept-Language': 'en-US,en;q=0.9, *;q=0.8',  # Accept English, then any language
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': random.choice(dnt_headers), 
                'Connection': random.choice(keep_alive_headers),
                'Upgrade-Insecure-Requests': random.choice(uir_headers),
                'Priority': 'u=1, i'
            }

            while True:
                params = {
                    'pageNum': current_page,
                    'pageSize': 48,
                    'epStatus': 1
                }

                full_url = base_url + '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
                response = requests.get(full_url, headers=headers)
                time.sleep(random.uniform(0.22, 0.97))  # Random delay to avoid rate limiting and simulate human behavior

                # If not 200 or 404
                if response.status_code not in (200, 404):
                    CNFS.warning('Error: Invalid response')
                    break
                elif response.status_code == 404:
                    CNFS.warning('Success: No more products found')
                    break

                # Parse JSON
                product_data = response.json()
                products = product_data.get('rows', [])
                
                # Create a list of the product's specifications (variable unpacking)
                for product in products:
                    title, item_id, goods_attr, seller, store_source_raw, price, exchange_code = (
                        product.get(key, '') for key in 
                        ('goodsName', 'itemNo', 'goodsAttr', 'storeName', 'storeSource', 'points', 'exchangeCode')
                    )

                    # Convert store source to reader-friendly format (dictionary mapping)
                    store_mapping = {
                        'wd': 'Weidian',
                        'taobao': 'Taobao',
                        'alibaba': 'Alibaba'
                    }
                    store_source = store_mapping.get(store_source_raw, store_source_raw)

                    # Convert attributes to string (assuming it might be a list or dictionary)
                    if isinstance(goods_attr, dict):
                        goods_attr = ' '.join(goods_attr.values())  # Adjust if needed
                    elif isinstance(goods_attr, list):
                        goods_attr = ' '.join(goods_attr) 

                    search_fields = [title, seller, goods_attr]

                    if any(self.query.lower() in field.lower() for field in search_fields):
                        print(colored('Title: ', 'green') + colored(str(title), 'white'))
                        print(colored('Item ID: ', 'green') + colored(str(item_id), 'white'))
                        print(colored('Goods Attr: ', 'green') + colored(str(goods_attr), 'white'))
                        print('---')
                        print(colored('Seller: ', 'green') + colored(str(seller), 'white') + colored(' | Source: ', 'green') + colored(str(store_source), 'white'))
                        print(colored('Price: ', 'green') + colored(str(price), 'white'))
                        print('---')
                        print(colored('Exchange Code: ', 'red') + colored(str(exchange_code), 'white'))
                        print(colored('URL: ', 'red') + colored(f'https://cnfair.com/detail/{item_id}', 'white'))
                        print()
                        print()

                        # Append to a file
                        with open(self.query + '.txt', 'a') as f:
                            f.write(f'Title: {title}\nItem ID: {item_id}\nGoods Attr: {goods_attr}\nSeller: {seller} | Source: {store_source}\nPrice: {price}\nExchange Code: {exchange_code}\nURL: https://cnfair.com/detail/{item_id}\n\n')

                if not products:
                    break

                current_page += 1

    def search(self):
        print()
        query = input('\033[1mWhat phrase do you want to search for?\033[0m ' + colored('>> ', 'green'))
        self.query = query
        print()
        CNFS.cnfair_look(self)


if __name__ == '__main__':
    cnfs = CNFS()
    cnfs.welcome()
    cnfs.is_online()
    cnfs.search()