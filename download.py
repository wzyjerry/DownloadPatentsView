import re
from os import makedirs, remove
from os.path import exists, getsize, join
from urllib.request import urlretrieve
from datetime import datetime
import requests

page = requests.get('https://www.patentsview.org/download/')
magic_str = r'href\w*=\w*"([^"]+.zip)"'
filelist = list(re.findall(magic_str, page.text))
timestamp = filelist[-1].split('/')[-3]
print(datetime.now(), 'Newest data is:', timestamp)
page = requests.get('https://www.patentsview.org/download/detail_desc_text.html')
filelist.extend(list(re.findall(magic_str, page.text)))

def remote_filesize(url):
    headers = requests.head(url)
    return int(headers.headers.get('Content-Length', 0))

def local_filesize(filename):
    return int(getsize(filename))

def cbk(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print(datetime.now(), '%.2f%%' % per)

def auto_down(url, filename):
    try:
        urlretrieve(url, filename, cbk)
    except:
        print('Network conditions is not good.Reloading.')
        auto_down(url, filename)

# Check if folder exists
data_root = join('data', timestamp)
if not exists(data_root):
    print('Data folder not found... Creating...')
    makedirs(data_root)
    print('Created.')
else:
    print('Data folder exists.')

for url in filelist:
    filename = url.split('/')[-1]
    fullname = join(data_root, filename)
    except_filesize = remote_filesize(url)
    while True:
        if not exists(fullname):
            print(datetime.now(), 'Downloading %s:' % filename)
            auto_down(url, fullname)
            print(datetime.now(), 'Downloaded.')
        else:
            if local_filesize(fullname) == except_filesize:
                print('%s already exists... skiping...' % filename)
                break
            else:
                print('%s is partial... deleting...' % filename)
                remove(fullname)
                print('Deleted.')
print('All file exists.')
print(datetime.now(), 'End.')
