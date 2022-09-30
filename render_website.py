from livereload import Server, shell
from render_pages import main as render_catalogue_pages

def main():
    render_catalogue_pages()
    server = Server()    
    server.watch('template.html', shell('python render_pages.py'))
    server.serve(root='.', port='8000')


if __name__ == '__main__':
    main()
