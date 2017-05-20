#!/usr/bin/env python3
from lxml import html
import bs4
from urllib.request import urlopen
from urllib.parse import urlparse, urlunparse
from time import sleep
from enum import Enum


class SourceKind(Enum):
    PATH = 0
    URL = 1


def load_links(url, sleep_time=1, attempts=5, timeout=20):

    sleep(sleep_time)
    parsed_url = urlparse(url)
    links = []

    for i in range(attempts):
        try:
            soup = bs4.BeautifulSoup(urlopen(url, timeout=timeout), 'lxml')
            break

        except Exception as e:
            print(e)
            if i == attempts - 1:
                raise e

    for tag_a in soup('a'):
        if 'href' in tag_a.attrs:
            link = list(urlparse(tag_a['href']))

            if link[0] == '':
                link[0] = parsed_url.scheme
            if link[1] == '':
                link[1] = parsed_url.netloc

            links.append(urlunparse(link))

    return links


def get_site(url):
    return urlparse(url).netloc


class DataCollector(object):
    def __init__(self, source, kind):
        if kind == SourceKind.PATH:
            self._init_with_path(source)
        else:
            self._init_with_url(source)

    def _init_with_path(self, path):
        with open(path, 'r') as f:
            self.urls = f.read().splitlines()

    def _init_with_url(self, url):
        self.urls = load_links(url)

    def get_data(self, sleep_time=1, attempts=5, timeout=20):
        all_data = []

        for ind, url in enumerate(self.urls):
            print('Analyzing {} url of {} urls...'
                  .format(ind + 1, len(self.urls)))
            for i in range(attempts):
                try:
                    soup = bs4.BeautifulSoup(urlopen(url, timeout=timeout),
                                             'lxml')
                    all_data.append(soup.get_text())
                    break

                except Exception as e:
                    print(e)
                    if i == attempts - 1:
                        raise e

        self.all_data = all_data
        print('That\'s all')

    def get_all_data(self):
        return self.all_data

    def print_to_file(self, data, filename):
        with open(filename, 'w') as f:
            f.write('\n\n'.join(data))


def main():
    pass


if __name__ == '__main__':
    main()
