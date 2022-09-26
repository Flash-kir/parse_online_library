import os
import json

import more_itertools

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def fetch_images(folder='./books/images'):
    images_folder = os.path.join(folder)
    os.makedirs(os.path.join(images_folder), exist_ok=True)
    day_images = []
    for filename in os.listdir(images_folder):
        day_images.append(os.path.join(images_folder, f'{filename}'))
    return day_images


def main():
    with open(os.path.join('./', 'books.json'), 'r') as books:
        books_list = json.load(books)

    books = open(os.path.join('./', 'books.json'), 'r')
    books_list = json.load(books)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    books_lists_devided_by_20 = list(more_itertools.chunked(books_list, 20))
    page_number = 0
    for books_lists in books_lists_devided_by_20:
        page_number += 1
        template = env.get_template('template.html')
        rendered_page = template.render(books=books_lists)
        os.makedirs(os.path.join('./pages'), exist_ok=True)
        with open(os.path.join('./pages', f'index{page_number}.html'), 'w', encoding="utf8") as file:
            file.write(rendered_page)
    
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
