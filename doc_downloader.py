import re, os
from pprint import pprint
import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        html = requests.get(url).text
    except Exception as e:
        print('web requests url error: {}\nlink: {}'.format(e, url))
        assert(0)
    return html


class WebDownloader(object):

    def __init__(self, base_url):
        self.url = base_url
        self.links = set()

    def parse_html(self, verbose=False):
        html = get_html(self.url)
        soup = BeautifulSoup(html, parser='lxml', features="lxml")
        for link in soup.findAll('a'):
            if link.has_attr('href'):
                href = str(link.get('href'))
                if href.startswith('http'):
                    self.links.add(href)
                    if verbose:
                        print(link.get('href'))

    def download(self, save_dir):
        print("find {} documents in this url: ".format(len(self.links)))
        for i, link in enumerate(self.links):
            link = str(link)
            if link.endswith('.pdf'):  # handle direct pdf url link
                file_name = link.split('/')[-1]
                try:
                    r = requests.get(link)
                    save_path = os.path.join(save_dir, file_name) if save_dir else file_name
                    with open(save_path, 'wb+') as f:
                        f.write(r.content)
                    print("  file {}/{}: {} download complete".format(i, len(self.links), link))
                except Exception as e:
                    print('Downloading error:{}\nlink:{}'.format(e, link))

    def pipeline(self, save_dir=None):
        self.parse_html()
        self.download(save_dir)


url = 'https://cs231n.github.io/neural-networks-1/'
wd = WebDownloader(url)
wd.pipeline()
