import os
from urllib.error import HTTPError

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath


def get_book_title(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_block = soup.find('body').find('div', id='content').find('h1')
    title, name = title_block.text.split('::')
    return sanitize_filepath(f'{id}. {title.strip()} - {name.strip()}.txt')

def check_for_redirect(response):
    if response.status_code // 100 == 3:
        raise HTTPError("Не найдена книга")


def download_file_by_id(url, filename, folder='books/'):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    os.makedirs(f'{folder}', exist_ok=True)
    with open(f'{folder}/{filename}', 'wb') as file:
        file.write(response.content)


def main():
    for id in range(11):
        try:
            download_file_by_id(
                f'https://tululu.org/txt.php?id={id}', 
                get_book_title(id)
            )
            
        except:
            HTTPError


if __name__ == '__main__':
    main()