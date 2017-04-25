#!/usr/bin/env python3
from lxml import html
import bs4
from urllib.request import urlopen


class DataCollector(object):
    def __init__(self, path):
        with open(path, 'r') as f:
            self.urls = f.read().splitlines()

    def get_data(self):
        all_data = []
        for url in self.urls:
            conn = urlopen(url)
            html_ = conn.read()
            cur_data = bs4.BeautifulSoup(html_, 'html.parser')
            all_data.append(cur_data.get_text())

        return all_data

    def print_to_file(self, data, filename):
        with open(filename, 'w') as f:
            f.write('\n\n'.join(data))


def main():
    pass


if __name__ == '__main__':
    main()
