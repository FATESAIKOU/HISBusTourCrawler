#!/usr/bin/env python3
import sys
import json

from pathlib import Path
from selenium import webdriver
from modules.storage import get_storage_instance


area_map = ['tyo', 'spk', 'sdj', 'tyo', 'ngo', 'osa', 'hij', 'fuk']


def getOptionValueTextPair(driver, input_name):
    info_key = "{ 'text': x.getAttribute('data-text'), 'value': x.value }"

    js_query = """
        return Array.from(
                document.querySelectorAll(
                    'input[name="{}"]'
                )
            ).map(function(x) {{
                return {}
            }})
    """
    return driver.execute_script(js_query.format(input_name, info_key))


def crawlSearchOptions(area_id):
    base_url = f"https://bus-tour.his-j.com/{area_id}/search/"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(base_url)
    driver.implicitly_wait(10)

    departure_area_info = getOptionValueTextPair(driver, "departureArea[]")
    purpose_info = getOptionValueTextPair(driver, "purpose[]")
    destination_info = getOptionValueTextPair(driver, "destination[]")
    tour_type_info = getOptionValueTextPair(driver, "type[]")

    driver.close()

    # '' means free-style
    return {
        'departure_area_options': departure_area_info,
        'departureDate': '',
        'departureMonth': '',
        'purpose_options': purpose_info,
        'destination_options': destination_info,
        'tour_type_options': tour_type_info,
        'lowPrice': '',
        'highPrice': '',
        'isGoOnly': [True, False],
        'isReservable': [True, False],
        'keyword': ''
    }


if __name__ == '__main__':
    storage = get_storage_instance(
        json.loads(
            Path(sys.argv[1]).read_text()
        )
    )

    for area_id in area_map:
        search_option_db = {}
        search_option_db[area_id] = crawlSearchOptions(area_id)
        storage.uploadData(
            json.dumps(search_option_db, ensure_ascii=False, indent=4),
            "{}_search_option_db.json".format(area_id)
        )
