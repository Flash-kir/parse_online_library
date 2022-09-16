import os
from urllib.error import HTTPError

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from urllib.parse import urlparse


def get_book_data(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    title_block = soup.find('body').find('div', id='content').find('h1')
    title, name = title_block.text.split('::')

    image_path = soup.find('div', class_='bookimage').find('img')['src']

    return {
        'filename': sanitize_filepath(f'{id}. {title.strip()} - {name.strip()}.txt'),
        'image_path': f'https://tululu.org/{image_path}'
    }
    

def check_for_redirect(response):
    if response.status_code // 100 == 3:
        raise HTTPError("Не найдена книга")


def download_file(url, filename, folder='books/'):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    os.makedirs(f'{folder}', exist_ok=True)
    with open(f'{folder}/{filename}', 'wb') as file:
        file.write(response.content)


def download_image(url, folder='images/'):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    filename = url.split('/')[-1]
    os.makedirs(f'{folder}', exist_ok=True)
    with open(f'{folder}/{filename}', 'wb') as file:
        file.write(response.content)


def main():
    for id in range(1, 10):
        try:
            book_data = get_book_data(id)
            download_file(
                f'https://tululu.org/txt.php?id={id}', 
                book_data['filename']
            )
            download_image(book_data['image_path'])
        except:
            HTTPError


if __name__ == '__main__':
    main()