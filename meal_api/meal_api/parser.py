import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

headers = Headers(browser='firefox', os='win').generate()
list_card_url = []
for page in range(1, 2):
    try:
        url = f'https://www.russianfood.com/?page={page}'

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')

        cards = soup.find_all('div', class_="annonce annonce_orange")

        for card in cards:
            card_url = 'https://www.russianfood.com' + card.find('td', class_='toptext').find('a').get('href')
            list_card_url.append(card_url)
    except Exception:
        print('mistake')
for card_url in list_card_url:
    try:
        response = requests.get(card_url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        card = soup.find('table', class_="recipe_new")

        title = card.find('td', class_='padding_l padding_r').find('h1', class_='title').text
        time_of_day = card.find('div', class_='el user_date').find('a').text.strip()
        products = card.find('table', class_='ingr').find_all('tr')
        products_list = [product.find_next('td', class_='padding_l padding_r').text.strip() + '\n' for product in products]
        steps = card.find_all('div', class_='step_n')
        steps_descriptions = [step.find('p').text.strip() for step in steps]
        steps_images = ['https:' + step.find('a').get('href') for step in steps]
        steps_dict = {step: image for step, image in zip(steps_descriptions, steps_images)}
        _ = '\n'
        print(f'Название: {title}\n'
              f'Время суток: {time_of_day}\n'
              f'Продукты:\n{" ".join(product for product in products_list)}'
              f'Шаги приготовления:\n{_.join(step + image for step, image in steps_dict.items())}\n'
              f'Ссылка: {card_url}\n\n')
    except Exception:
        print('mistake')
