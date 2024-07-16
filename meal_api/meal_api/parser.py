import pprint
import random
import time

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from tqdm import tqdm

base_url = 'https://www.russianfood.com'


def get_url(n):
    for page in range(1, n + 1):
        try:
            url = f'{base_url}/?page={page}'
            headers = Headers(browser='firefox', os='win').generate()
            response = requests.get(url, headers=headers)

            soup = BeautifulSoup(response.text, 'lxml')

            cards = soup.find_all('div', class_="annonce annonce_orange")
            time.sleep(random.uniform(1, 5))
            for card in cards:
                card_url = base_url + card.find('td', class_='toptext').find('a').get('href')
                time.sleep(random.uniform(1, 5))
                yield card_url
        except Exception:
            print('mistake')


def get_card(total=10):
    with tqdm(total=total, desc='Progress', ncols=100, unit='card') as pbar:
        for number, card_url in enumerate(get_url(total)):
            try:
                pbar.update()
                pbar.set_description(f"Обрабатывается {number + 1} карточка из {total}")
                headers = Headers(browser='firefox', os='win').generate()
                response = requests.get(card_url, headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')
                card = soup.find('table', class_="recipe_new")

                title = card.find('td', class_='padding_l padding_r').find('h1', class_='title').text
                products = card.find('table', class_='ingr').find_all('tr')
                products_list = [product.find_next('td', class_='padding_l padding_r').text.strip() for product in products]
                steps = card.find_all('div', class_='step_n')
                steps_descriptions = ["-" + step.find('p').text.strip() for step in steps]
                steps_images = ['https:' + step.find('a').get('href') for step in steps]
                steps_dict = {step: image for step, image in zip(steps_descriptions, steps_images)}

                title_info = card.find_all('span', class_='hl')
                if title_info is not None:
                    if len(title_info) > 0:
                        portions = title_info[0].find('b').text
                    else:
                        portions = None
                    if len(title_info) > 1:
                        cooking_time = title_info[1].get_text()
                    else:
                        cooking_time = None

                author_url = base_url + card.find('div', class_='sub_info').find('div', class_='el user_date').find('a').get('href')
                author = card.find('div', class_='sub_info').find('div', class_='el user_date').find('a').text
                time.sleep(random.uniform(1, 5))
                result = {
                    'title': title,
                    'portions': portions,
                    'cooking_time': cooking_time,
                    'products': products_list,
                    'cooking_steps': steps_dict,
                    'author': {
                        'nickname': {author},
                        'link': {author_url}
                    },
                    'link': card_url
                }
                pprint.pprint(result)
            except Exception as error:
                print('mistake')
                print(error, '||', card_url)


get_card()
