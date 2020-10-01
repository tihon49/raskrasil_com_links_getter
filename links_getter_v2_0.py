import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint


counter = 0


def get_soup(url):
    '''придерживаемся принципа DRY'''
    session = requests.Session()
    request = session.get(url)
    soup = bs(request.text, 'lxml')
    return soup


def get_categories_links() -> list:
    '''получаем ссылки на все категории'''
    url = 'https://raskrasil.com/'
    categories_list = []
    soup = get_soup(url)

    navbar = soup.find('nav', class_='fusion-main-menu').find \
        ('li', class_='menu-item-4540').find('ul', class_='sub-menu').find_all('li')

    for category in navbar:
        link = category.find('a').get('href')
        categories_list.append(link)
        print(f'получена ссылка на категорию {link}')

    print('\n[!] Ссылки на все категории собраны!\n')
    return categories_list


def get_alboms_liks_from_categories(lst):
    '''
    получаем список категорий, собираем все альбомы из категорий,
    возвращем список ссылок на собранные альбомы
    '''

    print('[!] Начинаем собирать ссылки на альбомы по каждой категории...\n')
    alboms_links = []

    for category in lst:
        print(f'получаем ссылки на альбомы из категории {category}')
        url = 'https://raskrasil.com/category/' + category
        soup = get_soup(url)
        mainDiv = soup.find('div', id='posts-container')
        alboms = mainDiv.find_all('article')

        for albom in alboms:
            albom_link = albom.find('a').get('href')
            alboms_links.append(albom_link)

    print('\n[!] Все ссылки на все альбомы по всем категориям собраны!\n')
    return alboms_links


def get_img_links(url) -> list:
    '''
    получаем ссылку на альбом, возвращаем
    ссылки на все картинки из альбома
    '''

    global counter
    print(f'Переходим к получению ссылок на картинки из альбома: {url}')
    soup = get_soup(url)
    links_list = []
    mainDiv = soup.find('div', class_='post-content')
    columns = mainDiv.find_all('div', class_='fusion-layout-column')

    for i in columns:
        item = i.find_all('img')

        for img in item:
            if 'data:image/' not in str(img):
                img_href = img.get('src')
                links_list.append(img_href)
                counter += 1

    return links_list


def main():
    categories = get_categories_links()
    all_categories_links = get_alboms_liks_from_categories(categories)
    links = []

    for albom_link in all_categories_links:
        links.append(get_img_links(albom_link))

    pprint(links)
    print(f'\nВсего собрано {counter} ссылок на картинки.')


if __name__ == '__main__':
    main()
