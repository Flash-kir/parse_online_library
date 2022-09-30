from livereload import Server, shell
from render_pages import main as render_catalogue_pages

'''
def fetch_images(folder='./books/images'):
    images_folder = os.path.join(folder)
    os.makedirs(os.path.join(images_folder), exist_ok=True)
    day_images = []
    for filename in os.listdir(images_folder):
        day_images.append(os.path.join(images_folder, f'{filename}'))
    return day_images
'''

def main():
    render_catalogue_pages()
    server = Server()    
    server.watch('template.html', shell('python render_pages.py'))
#    server.watch('pages/*.html')
    server.serve(root='.', port='8000')


if __name__ == '__main__':
    main()
