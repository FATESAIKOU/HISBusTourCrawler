#!/usr/bin/env python3 
import json
import urllib
import requests
import sys
import bs4

from optparse import OptionParser
from bs4 import BeautifulSoup as Soup 


def extractDetail(page):
    detail_info = {}

    # event title
    event_title = page.find('h2', attrs={'class': 'result-box-ttl'}).getText()
    detail_info['event_title'] = event_title

    # [summary meta]
    detail_info['summary'] = {}
    sum_details = page.find_all('span', attrs={'class': 'result-details-ttl'})
    for sum_detail in sum_details:
        
        title = sum_detail.getText()
        value = "Not Found"
        if type(sum_detail.next_sibling) is bs4.element.NavigableString:
            value = sum_detail.next_sibling
        elif type(sum_detail.next_sibling) is bs4.element.Tag:
            value = sum_detail.next_sibling.getText().strip()
        else:
            NotImplementedError("Unknow class type [summary detail]")

        detail_info['summary'][title] = value

    # [tour point] get image image-meta image-artical
    detail_info['tour_points'] = []

    tour_point_root = page.find('p', string='ツアーポイント').parent
    tour_points = tour_point_root.find_all('div', attrs={'class': 'contents-box'})

    for tour_point in tour_points:
        title = tour_point.find('p', attrs={'class': 'point-box-ttl'}).getText().strip()
        artical = tour_point.find('div', attrs={'class': 'point-box-txt'}).getText().strip()
        
        images_info = []
        for image in tour_point.find_all('img'):
            images_info.append({
                'src': image['src'],
                'caption': image.next_sibling.getText().strip()
            })

        detail_info['tour_points'].append({
            'title': title,
            'artical': artical,
            'images_info': images_info
        })

    # [hotel] get hotel image image-meta image-artical
    detail_info['hotels'] = []

    if page.find('p', string='ホテル') is not None:
        hotel_root = page.find('p', string='ホテル').parent
        hotels = hotel_root.find_all('div', attrs={'class': 'contents-box'})

        for hotel in hotels:
            title = hotel.find('p', attrs={'class': 'point-box-ttl'}).getText().strip()
            artical = hotel.find('div', attrs={'class': 'point-box-txt'}).getText().strip()

            images_info = []
            for image in hotel.find('div', attrs={'class': 'swiper-wrapper'}).find_all('div', attrs={'class': 'swiper-slide'}):
                images_info.append({
                    'src': image['style'].split("url(")[1].split(")")[0]
                })

            detail_info['hotels'].append({
                'title': title,
                'artical': artical,
                'images_info': images_info
            })

    # [schedual]
    detail_info['schedual'] = []
    
    schedual_root = page.find('p', string='行程表').parent

    for daily_schedual in schedual_root.find_all('ol'):
        schedual_details = []
        for schedual_detail in daily_schedual.find_all('li'):
            text = schedual_detail.getText().strip()

            if text != '↓':
                schedual_details.append(text)

        detail_info['schedual'].append(
            schedual_details
        )

    return detail_info

def crawlEventDetail(detail_url):
    # build query url & send request
    resp = requests.get(detail_url)

    # create beautifulsoup obj
    page = Soup(resp.content.decode('utf-8'), features="html.parser")

    # get detail
    detail_info = extractDetail(page)

    return detail_info
    

if __name__== '__main__':
    detail_url = sys.argv[1]
    
    detail_info = crawlEventDetail(detail_url)
    
    print(json.dumps(detail_info, ensure_ascii=False, indent=4))
