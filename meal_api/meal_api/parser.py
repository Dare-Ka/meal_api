import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

headers = Headers(browser='firefox', os='win').generate()

base_url = 'https://www.russianfood.com'


def get_url():
    for page in range(1, 2):
        try:
            url = f'{base_url}/?page={page}'

            response = requests.get(url, headers=headers)

            soup = BeautifulSoup(response.text, 'lxml')

            cards = soup.find_all('div', class_="annonce annonce_orange")

            for card in cards:
                card_url = base_url + card.find('td', class_='toptext').find('a').get('href')
                yield card_url
        except Exception as err:
            print('mistake')
            print(err)


for card_url in get_url():
    try:
        response = requests.get(card_url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        card = soup.find('table', class_="recipe_new")

        title = card.find('td', class_='padding_l padding_r').find('h1', class_='title').text
        products = card.find('table', class_='ingr').find_all('tr')
        products_list = [product.find_next('td', class_='padding_l padding_r').text.strip() + '\n' for product in products]
        steps = card.find_all('div', class_='step_n')
        steps_descriptions = ["-" + step.find('p').text.strip() for step in steps]
        steps_images = ['https:' + step.find('a').get('href') for step in steps]
        steps_dict = {step: image for step, image in zip(steps_descriptions, steps_images)}

        _ = '\n'

        portions = card.find('div', class_='sub_info').find('div', class_='el').find('span', class_='hl').find('b').text
        cooking_time = card.find('div', class_='sub_info').find_next('div', class_='el').find('span', class_='hl').find('b').text #TODO: Доработать время!
        author_url = base_url + card.find('div', class_='sub_info').find('div', class_='el user_date').find('a').get('href')
        author = card.find('div', class_='sub_info').find('div', class_='el user_date').find('a').text

        print(f'Название: {title}\n'
              f'Порции: {portions}\n'
              f'Время приготовления: {cooking_time}\n'
              f'Продукты:\n{" ".join(product for product in products_list)}'
              f'Шаги приготовления:\n{_.join(step + image for step, image in steps_dict.items())}\n'
              f'Автор: {author}({author_url})\n'
              f'Ссылка: {card_url}\n\n')
    except Exception as error:
        print('mistake')
        print(error)
