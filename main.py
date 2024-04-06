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

        while True:
            current_page = 1

            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Lang': 'en',
                'Currency': 'CNY', 
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'DNT': '1',
                'Host': 'cnfair.com',
                'Referer': 'https://cnfair.com/home',
                'Sec-Ch-Ua': '"Chromium";v="123", "Not:A-Brand";v="8"',
                'Sec-Ch-Ua-Mobile': '?1',
                'Sec-Ch-Ua-Platform': 'Android',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Connection': 'keep-alive',
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
                    title, item_id, goods_attr, seller, seller_id ,store_source_raw, price, exchange_code = (
                        product.get(key, '') for key in 
                        ('goodsName', 'itemNo', 'goodsAttr', 'storeName', 'storeId', 'storeSource', 'points', 'exchangeCode')
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
                        print(colored('Seller: ', 'green') + colored(str(seller) + f' ({seller_id})', 'white') + colored(' | Source: ', 'green') + colored(str(store_source), 'white'))
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