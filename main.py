import os, string, requests, shutil
from threading import Thread
from argparse import *
from sys import argv
from random import randint, choice
from PIL import Image

BASE_URL = 'https://i.imgur.com/'
MEDIA_DATA_URL = 'https://api.imgur.com/post/v1/media/{id}?include=media%2Cadconfig%2Caccount'

parser = ArgumentParser(description='Lets see what we can find...')
parser.add_argument('--threads', '-T', type=int, default=8, help='How many Threads should be started')
parser.add_argument('--directory', '-D', type=str, default='./output', help='Where all the Images should be stored')
parser.add_argument('--minsize', '-M', type=str, default="100x100", help='Minimum size the Image can be | Enter by scaleX`x`scaleY as string. Example: 100x100')
parser.add_argument('--id-length', '-L', type=str, default="6-7", help="Range or single value on how long the image id should be")
parser.add_argument('--disallow-ghost', '-G', type=bool, default=False, help='If ghost images should be deleted')

args = parser.parse_args()
print(f'[ D ] Arguments: {args}')

if not os.path.exists(args.directory):
    os.makedirs(args.directory)
    print(f'[ I ] Created output directory: ''{args.directory}''')

def create_url() -> str:
    if '-' in args.id_length:
        from_range, to_range = args.id_length.split('-')
        final_length = randint(int(from_range), int(to_range))
    else:
        final_length = int(args.id_length)
    iid = ''.join(choice(string.ascii_letters + string.digits) for _ in range(final_length))
    url = BASE_URL + iid
    #url += ''.join(choice(string.ascii_lowercase + string.digits) for _ in range(3))
    return (url, iid)

def is_ghost_image(image_id: str):
    response = requests.get(MEDIA_DATA_URL.replace("{id}", image_id))
    return response.status_code == 404

def crawl_pictures(thread: int, directory: str, minX: int=0, minY: int=0, disallow_ghost: bool=False):
    print(f'[ T ] Created thread: {thread}')
    while 1:
        url, iid = create_url()
        url += '.jpg'
        filename = url.rsplit('/', 1)[-1]

        response = requests.get(url, allow_redirects=False)

        image_dir = f'{directory}/{filename}'
        output_stream = open(image_dir, 'wb')
        for chunk in response.iter_content(1024):
            output_stream.write(chunk)
        output_stream.close()
        if response.status_code in [404, 400, 302, 301, 300]:
            print(f'[ X ] Invalid code: {filename}')
            os.remove(image_dir)
        else:
            image = Image.open(image_dir)
            size = image.size
            if size[0] < minX or size[1] < minY:
                print(f'[ E ] {image_dir} minimum requirements haven''t matched')
                os.remove(image_dir)
            else:
                print(f'[ I ] {filename} was found by thread {thread}')
                if not is_ghost_image(iid):
                    print(f'[ I ] {filename} is a normal image')
                else:
                    if disallow_ghost == True:
                        os.remove(image_dir)
                        print('[ W ] Deleting Ghost image...')
                    print(f'[ W ] {filename} is a ghost image')



if args.threads == 0:
    print('Thread Count is 0, there won''t be any crawling done')
    exit(0)


minX, minY = args.minsize.split('x')

print(f'Minimum Size is: {minX}x{minY}')
for i in range(args.threads):
    try:
        thread = Thread(target=crawl_pictures, args=(i, args.directory, int(minX), int(minY), args.disallow_ghost))
        thread.start()
    except: 
        print(f'Couldn\'t start Thread: {i}')
