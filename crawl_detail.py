#!/usr/bin/env python3
"""
@argv[1]: The json file containing bus tour detail urls for crawling
"""
import time
import json
import urllib
import requests
import sys
import bs4

from pathlib import Path
from optparse import OptionParser
from bs4 import BeautifulSoup as Soup
from modules.storage import get_storage_instance


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

    # [booking]
    detail_info['booking_info'] = []
    cal_root = page.find('div', attrs={'id': 'calendarWrap'})
    year_month = '20' + \
        cal_root.find('option', attrs={'selected': 'selected'})['data-key']

    available_dates = [c.parent for c in cal_root.find_all('li', string='募集中')]
    for date in available_dates:
        date_info = '{}/{}/{}'.format(
            year_month[0:4], year_month[4:6],
            date.select('li:nth-of-type(1)')[0].getText()
        )

        adult_price = date.select(
            'li:nth-of-type(3)')[0].find('span').getText().replace(',', '')
        child_price = date.select(
            'li:nth-of-type(4)')[0].find('span').getText().replace(',', '')

        detail_info['booking_info'].append({
            'date': date_info,
            'adult_price': adult_price,
            'child_price': child_price
        })

    # [tour point] get image image-meta image-article
    detail_info['tour_points'] = []

    tour_point_root = page.find('p', string='ツアーポイント').parent
    tour_points = tour_point_root.find_all(
        'div', attrs={'class': 'contents-box'})

    for tour_point in tour_points:
        title = tour_point.find(
            'p', attrs={'class': 'point-box-ttl'}).getText().strip()
        article = tour_point.find(
            'div', attrs={'class': 'point-box-txt'}).getText().strip()

        images_info = []
        for image in tour_point.find_all('img'):
            images_info.append({
                'src': image['src'],
                'caption': image.next_sibling.getText().strip()
            })

        detail_info['tour_points'].append({
            'title': title,
            'article': article,
            'images_info': images_info
        })

    # [hotel] get hotel image image-meta image-article
    detail_info['hotels'] = []

    if page.find('p', string='ホテル') is not None:
        hotel_root = page.find('p', string='ホテル').parent
        hotels = hotel_root.find_all('div', attrs={'class': 'contents-box'})

        for hotel in hotels:
            title = hotel.find(
                'p', attrs={'class': 'point-box-ttl'}).getText().strip()
            article = hotel.find(
                'div', attrs={'class': 'point-box-txt'}).getText().strip()

            images_info = []
            for image in hotel.find('div', attrs={'class': 'swiper-wrapper'}).find_all('div', attrs={'class': 'swiper-slide'}):
                images_info.append({
                    'src': image['style'].split("url(")[1].split(")")[0]
                })

            detail_info['hotels'].append({
                'title': title,
                'article': article,
                'images_info': images_info
            })

    # [schedule]
    detail_info['schedule'] = []

    schedule_root = page.find('p', string='行程表').parent

    for daily_schedule in schedule_root.find_all('ol'):
        schedule_details = []
        for schedule_detail in daily_schedule.find_all('li'):
            text = schedule_detail.getText().strip()

            if text != '↓':
                schedule_details.append(text)

        detail_info['schedule'].append(
            schedule_details
        )

    return detail_info


def crawlEventDetail(detail_url):
    # build query url & send request
    resp = requests.get(detail_url)

    # create beautifulsoup obj
    page = Soup(resp.content.decode('utf-8'), features="html.parser")

    # get detail
    detail_info = extractDetail(page)

    # add event url
    detail_info['event_url'] = detail_url

    return detail_info


if __name__ == '__main__':
    detail_urls = json.loads(
        Path(sys.argv[1]).read_text()
    )

    storage = get_storage_instance(
        json.loads(
            Path(sys.argv[2]).read_text()
        )
    )

    downloaded_events = storage.list()

    for detail_url in detail_urls:
        event_code = detail_url.split('=')[1].split('&')[0]

        output_file = f"bus_tour_{event_code}.json"
        if output_file in downloaded_events:
            continue

        try:
            detail_info = crawlEventDetail(detail_url)

            storage.uploadData(
                json.dumps(detail_info, ensure_ascii=False, indent=4),
                output_file
            )
        except Exception as e:
            print(e)
