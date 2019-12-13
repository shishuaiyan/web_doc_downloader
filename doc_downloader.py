#coding=utf-8
import re, os
from pprint import pprint
import requests
from bs4 import BeautifulSoup


class WebDownloader(object):

    def __init__(self, base_url):
        self.base_url = base_url
        self.links = set()
        self.count = 0
        self.url_list = []
        self.downloaded_list = []

    def get_html(self, url):
        html = None
        try:
            html = requests.get(url).text
        except Exception as e:
            print('web requests url error: {}\nlink: {}'.format(e, url))
        return html

    def parse_html(self, html, verbose=False):
        soup = BeautifulSoup(html, parser='lxml', features="lxml")
        for link in soup.findAll('a'):
            if link.has_attr('href'):
                href = str(link.get('href'))
                if href.startswith('http'):
                    self.links.add(href)
                    if verbose:
                        print(link.get('href'))

    def download(self, save_dir):
        target_ext = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
        for link in self.links:
            link = str(link)
            is_target = False
            for ext in target_ext:
                if link.endswith(ext):  # handle direct pdf url link
                    is_target = True
                    file_name = link.split('/')[-1]
                    if file_name not in self.downloaded_list:
                        try:
                            r = requests.get(link)
                            save_path = os.path.join(save_dir, file_name) if save_dir else file_name
                            with open(save_path, 'wb+') as f:
                                f.write(r.content)
                            self.count += 1
                            self.downloaded_list.append(file_name)
                            if len(self.downloaded_list) > 50:
                                self.downloaded_list.pop(0)
                            if os.path.getsize(save_path) < 50000:  # 小于50k
                                os.remove(save_path)
                            print("  file {}: {} download complete".format(self.count, link))
                        except Exception as e:
                            print('Downloading error:{}\nlink:{}'.format(e, link))
                        break
            if len(self.url_list) < 100:
                if not is_target:
                    self.url_list.append(link)


    def pipeline(self, url, save_dir=None):
        html = self.get_html(url)
        if html:
            self.parse_html(html)
            self.download(save_dir)

    def run(self, base_url):
        self.pipeline(base_url)
        for url in self.url_list:
            self.pipeline(url)
            self.url_list.pop(0)

# url = 'https://cs231n.github.io/neural-networks-1/'
url = 'https://zh.wikipedia.org/wiki/%E4%BD%9C%E6%96%87'
wd = WebDownloader(url)
wd.run(url)
