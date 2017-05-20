#!/usr/bin/env python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse, urlunparse
from time import sleep


def load_links(url, sleep_time=1, attempts=5, timeout=20):

    sleep(sleep_time)
    parsed_url = urlparse(url)
    links = []

    for i in range(attempts):
        try:
            soup = BeautifulSoup(urlopen(url, timeout=timeout), 'lxml')
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
