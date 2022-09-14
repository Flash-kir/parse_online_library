import requests

def main():
    url = 'https://tululu.org/txt.php?id=32168'
    response = requests.get(url)
    response.raise_for_status()
    book_file_name = '«Пески Марса» Артура Кларка.txt'

    with open(book_file_name, 'wb') as file:
        file.write(response.content)

if __name__ == '__main__':
    main()