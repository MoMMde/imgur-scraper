import os, string, requests, shutil
from threading import Thread
from argparse import *
from sys import argv
from random import randint, choice


BASE_URL = 'https://i.imgur.com/'

parser = ArgumentParser(description='Lets see what we can find...')
parser.add_argument('-threads', '-T', type=int, default=8, help='How many Threads should be started')

args = parser.parse_args()

def create_url(length: int) -> str:
    url = BASE_URL + ''.join(choice(string.ascii_letters + string.digits) for _ in range(3))
    url += ''.join(choice(string.ascii_lowercase + string.digits) for _ in range(3))
    return url

def scrape_pictures(thread):
    print(f'Initial thread execute: {thread}')
    while 1:
        url = create_url(randint(5, 6)) + '.jpg'
        filename = url.rsplit('/', 1)[-1]
        
        response = requests.get(url, allow_redirects=False)

        output_stream = open(filename, 'wb')
        for chunk in response.iter_content(1024):
            output_stream.write(chunk)
        output_stream.close()
        
        print(response.status_code)
        if response.status_code in [400, 302, 301, 300]:
            print(f'{thread} -> Invalid: {filename}')
            os.remove(filename)
        else:
            print(f'{thread} -> Valid: {filename}')

for i in range(args.threads):
    try:
        thread = Thread(target=scrape_pictures, args=(i,))
        thread.start()
    except:
        print(f'Couldn\'t start Thread: {i}')
print(f'Started {args.threads}')
