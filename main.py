import os, string, requests, shutil
from threading import Thread
from argparse import *
from sys import argv
from random import randint, choice
from PIL import Image

BASE_URL = 'https://i.imgur.com/'

parser = ArgumentParser(description='Lets see what we can find...')
parser.add_argument('--threads', '-T', type=int, default=8, help='How many Threads should be started')
parser.add_argument('--directory', '-D', type=str, default='./output', help='Where all the Images should be stored')
parser.add_argument('--minsize', '-M', type=str, default=None, help='Minimum size the Image can be')

args = parser.parse_args()

if not os.path.exists(args.directory):
    os.makedirs(args.directory)
    print(f'Made directory: {args.directory}')

def create_url(length: int) -> str:
    url = BASE_URL + ''.join(choice(string.ascii_letters + string.digits) for _ in range(3))
    url += ''.join(choice(string.ascii_lowercase + string.digits) for _ in range(3))
    return url

def image_size(path: str) -> tuple:
    image = Image.open(path)
    return image.size

def crawl_pictures(thread: int, directory: str, minX: int=0, minY: int=0):
    print(f'Initial thread execute: {thread}')
    while 1:
        url = create_url(randint(5, 6)) + '.jpg'
        filename = url.rsplit('/', 1)[-1]

        response = requests.get(url, allow_redirects=False)

        image_dir = f'{directory}/{filename}'
        output_stream = open(image_dir, 'wb')
        for chunk in response.iter_content(1024):
            output_stream.write(chunk)
        output_stream.close()
        
        if response.status_code in [404, 400, 302, 301, 300]:
            print(f'{thread} -> Invalid: {filename}')
            os.remove(image_dir)
        else:
            size = image_size(image_dir)
            print(size)
            print(size[0])
            print(size[1])
            print(size[0] < minX)
            print(size[1] < minY)
            if size[0] < minX or size[1] < minY:
                print(f'{image_dir} -- Does not match minimum requirements. Deleting!')
                os.remove(image_dir)
            print(f'{thread} -> Valid: {filename}')


if args.threads == 0:
    print('Thread Count is 0, there won\'t be any crawling')
    exit(0)


minX, minY = args.minsize.split('x')

print(f'Minimum Size is: {minX}x{minY}')
for i in range(args.threads):
    try:
        thread = Thread(target=crawl_pictures, args=(i, args.directory, int(minX), int(minY),))
        thread.start()
    except:
        print(f'Couldn\'t start Thread: {i}')
