#!/usr/bin/env python3
import json
import urllib
import requests
import sys

from pathlib import Path
from bs4 import BeautifulSoup as Soup
from modules.storage import get_storage_instance


area_map = ['tyo', 'spk', 'sdj', 'tyo', 'ngo', 'osa', 'hij', 'fuk']


def parseHISStyleParam(search_params):
    query_str = ''
    for key in search_params:
        if type(search_params[key]) == list:
            for v in search_params[key]:
                query_str += '&' + urllib.parse.urlencode({key: v})
        else:
            query_str += '&' + \
                urllib.parse.urlencode({key: search_params[key]})

    return query_str[1:]


def crawlDetailPageUrls(area_id, search_params):
    base_url = "https://bus-tour.his-j.com/{}/search/?".format(
        area_map[area_id])

    detail_urls = []
    i = 0
    while True:
        i += 1
        search_params['page'] = i

        # build query url & send request
        resp = requests.get(base_url + parseHISStyleParam(search_params))

        # create beautifulsoup obj
        page = Soup(resp.content.decode('utf-8'), features="html.parser")

        # get all url
        tmp_urls = list(map(
            lambda p: 'https://bus-tour.his-j.com' + p.find('a').get('href'),
            page.find_all('p', attrs={'class': 'result-btn'})
        ))

        detail_urls.extend(tmp_urls)

        if len(tmp_urls) == 0:
            break

    return detail_urls


if __name__ == '__main__':
    search_params = json.loads(
        Path(sys.argv[1]).read_text()
    )

    storage = get_storage_instance(
        json.loads(
            Path(sys.argv[2]).read_text()
        )
    )

    urls = crawlDetailPageUrls(search_params['area_id'], search_params)

    storage.uploadData(
        json.dumps(urls, ensure_ascii=False, indent=4),
        'detail_urls.json'
    )
