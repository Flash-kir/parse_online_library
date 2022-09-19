import os

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json

from main import check_for_redirect, download_book

BASE_URL = 'https://tululu.org/'
FANTASTIC_CATEGORY_URL = urljoin(BASE_URL, 'l55/')

def get_category_page(page_num: int) -> str:
    url = urljoin(FANTASTIC_CATEGORY_URL, f'{page_num}/')
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    return response.text


def parse_category_page(page_html: str) -> list:
    soup = BeautifulSoup(page_html, 'lxml')
    selector = 'body div[id="content"] .bookimage a[href]'
    books_urls = soup.select(selector)
    books_jsons = []
    for book_link in books_urls:
        book_url = urljoin(BASE_URL, book_link['href'])
        print(book_url)
        book_json = download_book(book_url)
        if book_json:
            if book_json['book_path']:
                books_jsons.append(book_json)
    return books_jsons


def main(max: int):
    for page_num in range(1, max + 1):
        page_html = get_category_page(page_num)
        books = parse_category_page(page_html)
        with open('books.json', 'w', encoding='utf-8') as file:
            json.dump(books, file, ensure_ascii=False)

        


if __name__ == '__main__':
    # argparse
    main(1)
