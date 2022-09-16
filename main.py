import os
import argparse
from urllib.error import HTTPError

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from urllib.parse import urlparse


def parse_book_page(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    title_block = soup.find('body').find('div', id='content').find('h1')
    title, name = title_block.text.split('::')

    image_path = soup.find('div', class_='bookimage').find('img')['src']

    comments_blocks = soup.find('div', id='content').find_all('div', class_='texts')
    comments = []
    for comment_block in comments_blocks:
        comments.append(comment_block.find('span').text)

    genres_blocks = soup.find('span', class_='d_book').find_all('a')
    genres = []
    for genres_block in genres_blocks:
        genres.append(genres_block.text)


    print(sanitize_filepath(f'{id}. {title.strip()} - {name.strip()}.txt'))
    print(genres)
    return {
        'filename': sanitize_filepath(f'{id}. {title.strip()} - {name.strip()}.txt'),
        'image_path': f'https://tululu.org/{image_path}',
        'comments': comments,
        'genres': genres
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
    parser = argparse.ArgumentParser()
    parser.add_argument('start_id', type=int, default=1, help='id книги, с которой начинается скачивание')
    parser.add_argument('end_id', type=int, default=10, help='id книги, которой закончится скачивание')
    args = parser.parse_args()
    for id in range(args.start_id, args.end_id):
        try:
            book_data = parse_book_page(id)
            download_file(
                f'https://tululu.org/txt.php?id={id}', 
                book_data['filename']
            )
            download_image(book_data['image_path'])
        except:
            HTTPError


if __name__ == '__main__':
    main()