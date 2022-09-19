# Парсим онлайн библиотеку

Программа скачивает книги с сайта https://tululu.org/ и складывает в папку "/books".
Также скачиваются обложки книг в папку "/images". По окончании скачивания книг сохраняется файл, содержащий список словарей с параметрами книг, скачанных с сайта https://tululu.org/

## Установка

Клонируйте репозиторий:

    git clone git@github.com:Flash-kir/parse_online_library.git

Для установки компонентов выполните:

    pip install -r requirenments.txt

Для запуска вызовите:

    python parse_tululu_category.py [-h] [-s START_PAGE] [-e END_PAGE] [-f DEST_FOLDER] [-i SKIP_IMGS] [-t SKIP_TXT] [-j JSON_PATH]

    -s START_PAGE, --start_page START_PAGE номер страницы в разделе фантастики, с которой начинается скачивание, по умолчанию значение 1
    -e END_PAGE, --end_page END_PAGE номер страницы в разделе фантастики, которой закончится скачивание, по умолчанию значение 701
    -f DEST_FOLDER, --dest_folder DEST_FOLDER путь к каталогу с результатами парсинга: картинкам, книгам, JSON, по умолчанию пустое значение
    -i SKIP_IMGS, --skip_imgs SKIP_IMGS не скачивать картинки, по умолчанию False
    -t SKIP_TXT, --skip_txt SKIP_TXT не скачивать книги, по умолчанию False
    -j JSON_PATH, --json_path JSON_PATH указать свой путь к *.json файлу с результатами, по умолчанию пустое значение

## get_book_html

Функция получает в качестве аргумента:
book_url - url книги на сайте https://tululu.org/
Возвращает текст html страницы книги.

## parse_book_page

Функция получает в качестве аргументов: 
book_url - url книги на сайте https://tululu.org/ 
book_html - текст html страницы книги
Парсит название книги, автора, жанр и комментари.
Возвращает словарь c ключами:
'title' - название книги
'author' - имя автора
'filepath' - тип строка, содержит название книги и имя автора
'image_path' - url адрес обложки книги
'comments' - список текстов комментариев книги
'genres' - список жанров, к которым относится книга

## check_for_redirect

Функция получает response и вызывает исключение в случае отсутствия книги.

## download_book_text_to_file

Функция получает на вход аргументы:

book_id - id книги на сайте https://tululu.org/
filename - имя файла, в который будет сохранен текст книги
dest_folder - путь к каталогу с результатами парсинга: картинкам, книгам, JSON
folder - каталог, в который необходимо сохранить текст книги (по умолчанию "/books")

Проверяет есть ли книга по url адресу и в случае успеха сохраняет ее в файл.

## download_image

Функция получает на вход аргументы:

url - url адрес обложки книги
dest_folder - путь к каталогу с результатами парсинга: картинкам, книгам, JSON
folder - каталог, в который необходимо сохранить изображение обложки книги (по умолчанию "/images")

Проверяет есть ли изображение по url адресу и в случае успеха сохраняет его в файл.

## get_book_id_from_url

Функция получает на вход:
book_url - url книги на сайте https://tululu.org/
Возвращает id книги на сайте https://tululu.org/

## download_book

Функция получает на вход аргументы:
book_url - url книги на сайте https://tululu.org/
dest_folder - путь к каталогу с результатами парсинга: картинкам, книгам, JSON
skip_imgs - не скачивать книги
skip_txt - не скачивать книги
Возвращает словарь:
    {
        'title': строка,
        'author': строка,
        'image_src': строка, # пустой если skip_imgs = True
        'book_path': строка, # пустой если skip_txt = True
        'comments': список комментариев,
        'genres': список жанров
    }

## get_category_page

Функция получает в качестве аргумента:
page_num - номер страницы списка книг из раздела фантастики на сайте https://tululu.org/
Возвращает текст html страницы книги.

## parse_category_page

Функция получает на вход аргументы:
page_html - html текст страницы списка книг из раздела фантастики на сайте https://tululu.org/
dest_folder - путь к каталогу с результатами парсинга: картинкам, книгам, JSON
skip_imgs - не скачивать книги
skip_txt - не скачивать книги
Возвращает список из 25 словарей книг со страницы списка книг из раздела фантастики на сайте https://tululu.org/, текст которой принимает функция.
