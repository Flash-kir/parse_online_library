import argparse
import os
import time

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from urllib.error import HTTPError
from urllib.parse import urljoin


def get_book_html(book_url: str):
    response = requests.get(book_url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    return response.text


def parse_book_page(book_html, book_url: str) -> dict:
    soup = BeautifulSoup(book_html, 'lxml')
    title_block = soup.find('body').find('div', id='content').find('h1')
    title, name = title_block.text.split('::')
    image_path = soup.find('div', class_='bookimage').find('img')['src']
    comments = [x.find('span').text for x in soup.find('div', id='content').find_all('div', class_='texts')]
    genres = [x.text for x in soup.find('span', class_='d_book').find_all('a')]

    return {
        'title': f'{title.strip()}',
        'author': f'{name.strip()}',
        'filename': sanitize_filepath(f'{title.strip()} - {name.strip()}.txt'),
        'image_path': urljoin(book_url, image_path),
        'comments': comments,
        'genres': genres
    }
    

def check_for_redirect(response):
    if response.history:
        raise HTTPError('Старинца не найдена')


def download_book_text_to_file(book_id, filename: str, dest_folder, folder='books/'):
    params = {
        'id': book_id
    }
    response = requests.get('https://tululu.org/txt.php', params=params, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    os.makedirs(os.path.join(dest_folder, folder), exist_ok=True)
    with open(os.path.join(dest_folder, folder, filename), 'wb') as file:
        file.write(response.content)
    return os.path.join(dest_folder, folder, filename)



def download_image(url, dest_folder, folder='images/'):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    filename = url.split('/')[-1]
    os.makedirs(os.path.join(dest_folder, folder), exist_ok=True)
    with open(os.path.join(dest_folder, folder, filename), 'wb') as file:
        file.write(response.content)
    return os.path.join(dest_folder, folder, filename)


def get_book_id_from_url(book_url: str):
    return book_url.split('/b')[-1].split('/')[0]


def download_book(book_url: str, dest_folder: str, skip_imgs: bool, skip_txt: bool):
    book_html = get_book_html(book_url)
    book_content = parse_book_page(book_html, book_url)
    image_src = ''
    book_path = ''
    if not skip_imgs:
        image_src = download_image(book_content['image_path'], dest_folder)
    if not skip_txt:
        book_path = download_book_text_to_file(
            get_book_id_from_url(book_url), 
            book_content['filename'],
            dest_folder
        )
    return {
        'title': book_content['title'],
        'author': book_content['author'],
        'image_src': image_src,
        'book_path': book_path,
        'comments': book_content['comments'],
        'genres': book_content['genres']
    }



def main(start_id: int, end_id: int, dest_folder: str, skip_imgs: bool, skip_txt: bool):
    for book_id in range(start_id, end_id + 1):
        try:
            download_book(
                urljoin('https://tululu.org/', f'b{book_id}/'),
                dest_folder, 
                skip_imgs, 
                skip_txt
            )
        except HTTPError:
            print('редирект')
        except AttributeError:
            print(f'не найдена страница книги {book_id}')
        except requests.exceptions.HTTPError:
            print('ссылка не верна')
        except requests.exceptions.ConnectionError:
            print('соединение потеряно')
            time.sleep(5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Программа скачивает книги с сайта https://tululu.org/")
    parser.add_argument('start_id', type=int, default=1, help='id книги, с которой начинается скачивание')
    parser.add_argument('end_id', type=int, default=10, help='id книги, которой закончится скачивание')
    parser.add_argument('-f', '--dest_folder', type=str, default='', help='путь к каталогу с результатами парсинга: картинкам, книгам, JSON')
    parser.add_argument('-i', '--skip_imgs', type=bool, default=False, help='не скачивать картинки')
    parser.add_argument('-t', '--skip_txt', type=bool, default=False, help='не скачивать книги')
    args = parser.parse_args()
    main(
        args.start_id, 
        args.end_id,
        args.dest_folder,
        args.skip_imgs,
        args.skip_txt,
    )
