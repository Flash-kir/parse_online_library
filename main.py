import os
import argparse

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from urllib.error import HTTPError
from urllib.parse import urljoin


def parse_book_page(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    title_block = soup.find('body').find('div', id='content').find('h1')
    title, name = title_block.text.split('::')
    image_path = soup.find('div', class_='bookimage').find('img')['src']
    comments = [x.find('span').text for x in soup.find('div', id='content').find_all('div', class_='texts')]
    genres = [x.text for x in soup.find('span', class_='d_book').find_all('a')]

    return {
        'filename': sanitize_filepath(f'{book_id}. {title.strip()} - {name.strip()}.txt'),
        'image_path': urljoin('https://tululu.org/', image_path),
        'comments': comments,
        'genres': genres
    }
    

def check_for_redirect(response):
    if response.history:
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
    parser = argparse.ArgumentParser(description="Программа скачивает книги с сайта https://tululu.org/")
    parser.add_argument('start_id', type=int, default=1, help='id книги, с которой начинается скачивание')
    parser.add_argument('end_id', type=int, default=10, help='id книги, которой закончится скачивание')
    args = parser.parse_args()
    for book_id in range(args.start_id, args.end_id + 1):
        try:
            book_data = parse_book_page(book_id)
            download_file(
                f'https://tululu.org/txt.php?id={book_id}', 
                book_data['filename']
            )
            download_image(book_data['image_path'])
        except:
            HTTPError


if __name__ == '__main__':
    main()