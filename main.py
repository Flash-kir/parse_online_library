import requests

def download_file_by_id(id, dir):
    url = f'https://tululu.org/txt.php?id={id}'
    response = requests.get(url)
    response.raise_for_status()
    file_name = f'{dir}/book_{id}'
    with open(file_name, 'wb') as file:
        file.write(response.content)



def main():
    for i in range(10):
        download_file_by_id(i+1, 'books')

if __name__ == '__main__':
    main()