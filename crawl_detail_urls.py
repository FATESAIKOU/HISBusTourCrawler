#!/usr/bin/env python3 
import json
import urllib
import requests
import sys

from optparse import OptionParser
from bs4 import BeautifulSoup as Soup 


area_map = ['tyo', 'spk', 'sdj', 'tyo', 'ngo', 'osa', 'hij', 'fuk']

parser = OptionParser()
parser.add_option("-t", "--test", default=True, action="store_true",
            help="use options sample for test")
parser.add_option("-f", "--file",
            help="read options from file", metavar="FILE")
parser.add_option("-s", "--stdin", default=False, action="store_true",
            help="read options from stdin")

def parseHISStyleParam(search_params):
    query_str = ''
    for key in search_params:
        if type(search_params[key]) == list:
            for v in search_params[key]:
                query_str += '&' + urllib.parse.urlencode({key: v})
        else:
            query_str += '&' + urllib.parse.urlencode({key: search_params[key]})

    return query_str[1:]


def crawlDetailPageUrls(area_id, search_params):
    base_url = "https://bus-tour.his-j.com/{}/search/?".format(area_map[area_id])

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
    

if __name__== '__main__':

    (options, args) = parser.parse_args()
    
    options = vars(options)

    if options['file'] is not None:
        with open(options['file'], 'r') as src:
            search_params = json.load(src)
    elif options['stdin'] == True:
        search_params = json.loads(sys.stdin.read())
    elif options['test'] == True:
        search_params = {
            'area_id': 0,
            'sort': 'recommend',
            'departureArea[]': [3],
            'departureDate': '',
            'departureMonth': '2021-07',
            'purpose[]': '',
            'lowPrice': 0,
            'highPrice': 50000,
            'isGoOnly': '',
            'isReservable': '',
            'keyword': ''
        }
    else:
        NotImplementedError('No correct option been passed')

    urls = crawlDetailPageUrls(search_params['area_id'], search_params)

    with open('detail_urls.json', 'w') as dst:
        json.dump(urls, dst, indent=4)
