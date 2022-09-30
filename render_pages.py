import os
import json

import more_itertools
from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():
    books = open(os.path.join('./', 'books.json'), 'r')
    books_catalogue = [book for book in json.load(books) if book['book_path'] != '']
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    page_books_count = 20
    devided_books_lists = list(more_itertools.chunked(books_catalogue, page_books_count))
    for page_number, books_lists in enumerate(devided_books_lists, start=1):
        near_pages = {
            'current': page_number,
            'page_count': len(devided_books_lists)
        }
        template = env.get_template('template.html')
        rendered_page = template.render(
            books=books_lists, 
            near_pages=near_pages
        )
        os.makedirs(os.path.join('./pages'), exist_ok=True)
        with open(os.path.join('./pages', f'index{page_number}.html'), 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    main()
