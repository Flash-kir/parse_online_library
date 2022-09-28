import os
import json

import more_itertools

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell


def fetch_images(folder='./books/images'):
    images_folder = os.path.join(folder)
    os.makedirs(os.path.join(images_folder), exist_ok=True)
    day_images = []
    for filename in os.listdir(images_folder):
        day_images.append(os.path.join(images_folder, f'{filename}'))
    return day_images


def main():
    books = open(os.path.join('./', 'books.json'), 'r')
    books_catalogue = [book for book in json.load(books) if book['book_path'] != '']
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    page_books_count = 20
    books_lists_devided_by_20 = list(more_itertools.chunked(books_catalogue, page_books_count))
    page_numbers = []
    for page_number, books_lists in enumerate(books_lists_devided_by_20):
        near_pages = {
            'current': page_number + 1,
            'page_count': len(books_lists_devided_by_20)
        }
        page_numbers.append(page_number + 1)
        template = env.get_template('template.html')
        rendered_page = template.render(
            books=books_lists, 
            page_numbers=page_numbers, 
            near_pages=near_pages
        )
        os.makedirs(os.path.join('./pages'), exist_ok=True)
        with open(os.path.join('./pages', f'index{page_number + 1}.html'), 'w', encoding="utf8") as file:
            file.write(rendered_page)
    
    server = Server()
    server.watch('*.*')
    server.serve(root='.', port='8000')
#    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
#    server.serve_forever()


if __name__ == '__main__':
    main()
