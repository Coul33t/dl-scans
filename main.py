# Getting the pages
import requests
# Finding the desired informations
from bs4 import BeautifulSoup as BS
# creating directories
import os
# Better than using strings for paths
import pathlib

def get_single_tome(page: requests.Response, path: pathlib.Path) -> None:
    soup = BS(page.content, 'html.parser')

    # For each <img> tag
    for i, img in enumerate(soup.find_all('img')):
        # If the image has the 'data-src' attribute and if it's a jpg
        if img.has_attr('data-src') and 'jpg' in img['data-src']:

            file_path = pathlib.Path(path / pathlib.Path(str(i) + '.jpg'))
            
            # For each page of the manga
            with open(file_path, 'wb') as output_file:
                stream = requests.get(img['data-src'], stream=True)
                total_length = int(stream.headers.get('content-length'))
                #for chunk in progress.bar(stream.iter_content(chunk_size=1024), expected_size=(1 + total_length / 1024), label=f'Page {str(i)}'):
                for chunk in stream.iter_content(chunk_size=1024):
                        if chunk:
                            output_file.write(chunk)
                            output_file.flush()
                
                stream.close()
                print(f'Page {str(i)}', end='\r')

def create_folder(folder_name: pathlib.Path) -> bool:
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        print(f'ERROR: folder {folder_name} already exists.')
        return False

    return True

def main():
    base_url = "https://mangascan.cc/manga/samurai-deeper-kyo/"
    # First page of first tome is https://scansmangas.ws/scans/samurai-deeper-kyo/1/1.jpg
    # -> https://scansmangas.ws/scans/samurai-deeper-kyo/TOME/PAGE.jpg
    base_image_url = "https://scansmangas.ws/scans/samurai-deeper-kyo/"

    output_directory = pathlib.Path("Samurai Deeper Kyo/")

    create_folder(output_directory)

    for i in range(38):
        current_tome = str(i + 1)
        current_url = base_url + current_tome

        print(f'Querying url {current_url} ...')

        page = requests.get(current_url)

        print(f'Page was returned.')

        tome_path = pathlib.Path(output_directory / pathlib.Path(current_tome))
        create_folder(tome_path)

        print(f'Tome {current_tome}:')
        get_single_tome(page, tome_path)


if __name__ == '__main__':
    main()