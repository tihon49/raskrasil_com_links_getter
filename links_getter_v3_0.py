import requests
from bs4 import BeautifulSoup as bs
# from pprint import pprint
from threading import Thread

file = open('links.log', 'w', encoding='utf-8')
counter = 0


def threaded(func):
    """
    Decorator that multithreads the target function
    with the given parameters. Returns the thread
    created for the function
    """

    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args)
        thread.start()
        return thread

    return wrapper


def get_soup(url):
    '''придерживаемся принципа DRY'''

    session = requests.Session()
    request = session.get(url)
    if request.status_code == 200:
        soup = bs(request.text, 'lxml')
        return soup
    return False


def get_categories_links() -> list:
    '''получаем ссылки на все категории'''

    url = 'https://raskrasil.com/'
    categories_list = []
    soup = get_soup(url)

    if soup:
        navbar = soup.find('nav', class_='fusion-main-menu').find \
            ('li', class_='menu-item-4540').find('ul', class_='sub-menu').find_all('li')

        for category in navbar:
            link = category.find('a').get('href')
            categories_list.append(link)
            print(f'получена ссылка на категорию {link}')

        print('\n[!] Ссылки на все категории собраны!')
        print(f'Всего категорий: {len(categories_list)}\n')
        return categories_list


def get_alboms_links_from_categories(lst) -> list:
    '''
    получаем список категорий
    собираем все альбомы из категорий
    возвращем список ссылок на собранные альбомы
    '''

    print('[!] Начинаем собирать ссылки на альбомы по каждой категории...\n')
    albums_links = []

    for category in lst:
        print(f'получаем ссылки на альбомы из категории {category}')
        url = 'https://raskrasil.com/category/' + category
        soup = get_soup(url)

        if soup:
            albums = soup.find('div', id='posts-container').find_all('article')

            for album in albums:
                album_link = album.find('a').get('href')
                albums_links.append(album_link)

    print(f'\n[!] Все ссылки на все все альбомы по всем категориям собраны!\n[+] Всего альбомов: {len(albums_links)}\n')
    return albums_links


# многопоточность иногда тупит. Можно включать/выключать
# @threaded
def get_img_links(url) -> list:
    '''
    получаем ссылку на альбом
    возвращаем ссылки на все картинки из альбома
    '''

    global counter
    soup = get_soup(url)
    links_list = []

    if soup:
        columns = soup.find('div', class_='post-content').find_all('div', class_='fusion-layout-column')

        for column in columns:
            images = column.find_all('img')

            for img in images:
                img_href = img.get('src')
                if 'data:image/' not in str(img_href):
                    links_list.append(img_href)
                    file.write(img_href + '\n')
                    counter += 1

    print(f'Получены ссылки на картинки из альбома: {url}\n[+] Всего картинок: {len(links_list)}\n')
    return links_list


def main():
    print('[!] Нчинаем собирать категории с сайта raskrasil.com\n')
    categories = get_categories_links()
    albums = get_alboms_links_from_categories(categories)

    for album_link in albums:
        get_img_links(album_link)

    global file
    file.close()

    print(f'\n[+] Всего собрано {counter} ссылок на картинки.')


if __name__ == '__main__':
    main()
