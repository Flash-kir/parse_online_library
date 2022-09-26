import os
import json

#from http.server import HTTPServer, SimpleHTTPRequestHandler

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
    with open(os.path.join('./', 'books.json'), 'r') as books:
        books_list = json.load(books)

    books = open(os.path.join('./', 'books.json'), 'r')
    books_list = json.load(books)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(books=books_list)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    
    server = Server()
    server.watch('*.*', shell('index html'))
    server.serve(root='.', port='8000')

#    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
#    server.serve_forever()
#    with open(path, mode='r', encoding='utf-8') as my_file:

if __name__ == '__main__':
    main()
