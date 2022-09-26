import argparse
import os
import time

import requests
from tqdm import tqdm
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json

from parse_tululu_book import check_for_redirect, parse_book, download_image, download_book_text_to_file

FANTASTIC_CATEGORY_URL = urljoin('https://tululu.org/', 'l55/')


def get_category_page(category_url: str) -> str:
    response = requests.get(category_url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    return response.text


def get_book_id_from_url(book_url: str):
    return book_url.split('/b')[-1].split('/')[0]

def parse_category_page(page_html: str, category_url: str) -> list:
    soup = BeautifulSoup(page_html, 'lxml')
    selector = 'body div[id="content"] .bookimage a[href]'
    books_links = soup.select(selector)
    books_urls = []
    for book_link in books_links:
        books_urls.append(urljoin(category_url, book_link['href']))
    return books_urls


def parse_args():
    parser = argparse.ArgumentParser(description="Программа скачивает книги с сайта https://tululu.org/")
    parser.add_argument('-s', '--start_page', type=int, default=1, help='номер страницы в разделе фантастики, с которой начинается скачивание')
    parser.add_argument('-e', '--end_page', type=int, default=701, help='номер страницы в разделе фантастики, которой закончится скачивание')
    parser.add_argument('-f', '--dest_folder', default='', help='путь к каталогу с результатами парсинга: картинкам, книгам, JSON')
    parser.add_argument('-i', '--skip_imgs', type=bool, default=False, help='не скачивать картинки')
    parser.add_argument('-t', '--skip_txt', type=bool, default=False, help='не скачивать книги')
    parser.add_argument('-j', '--json_path', default='./', help='указать свой путь к *.json файлу с результатами')
    return parser.parse_args()


def fetch_books(start_page: int, end_page: int, dest_folder: str, skip_imgs: bool, skip_txt: bool, json_path: str):
    books = []
    for page_num in range(start_page, end_page):
        try:
            category_page_url = urljoin(FANTASTIC_CATEGORY_URL, f'{page_num}/')
            page_html = get_category_page(category_page_url)
            print(f'Page {page_num} downloading')
            page_books_urls = parse_category_page(page_html, category_page_url)
        except requests.exceptions.HTTPError:
            print('ссылка на страницу каталога не верна')
        except requests.exceptions.ConnectionError:
            print('соединение потеряно')
            time.sleep(5)
        for book_url in tqdm(page_books_urls):
            try:
                book_content = parse_book(book_url)
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
                if book_content:
                    books.append({
                        'title': book_content['title'],
                        'author': book_content['author'],
                        'image_src': image_src,
                        'book_path': book_path,
                        'comments': book_content['comments'],
                        'genres': book_content['genres']
                    })
            except requests.exceptions.HTTPError:
                print('ссылка на книгу не верна')
            except requests.exceptions.ConnectionError:
                print('соединение потеряно')
                time.sleep(5)
    result_json_path = ''
    if json_path:
        result_json_path = json_path
    elif dest_folder:
        result_json_path = dest_folder
    os.makedirs(result_json_path, exist_ok=True)
    json_filename = os.path.join(result_json_path, f'books({start_page}-{end_page - 1}_pages).json')
    with open(json_filename, 'w', encoding='utf-8') as file:
        json.dump(books, file, ensure_ascii=False)


def main():
    args = parse_args()
    fetch_books(
        args.start_page,
        args.end_page,
        args.dest_folder,
        args.skip_imgs,
        args.skip_txt,
        args.json_path
    )

if __name__ == '__main__':
    main()
