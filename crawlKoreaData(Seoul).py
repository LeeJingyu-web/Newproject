import requests
from bs4 import BeautifulSoup
from utils import write_data

import pandas as pd


def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    updated = soup.find('p', class_='txt-status').text  # 업데이트날짜

    data = soup.select('.seoul-map-wrap>.seoul-map.seoul-map-all>span')

    data.pop()
    return data, updated


def parse_data(data, updated):
    confirmed_seoul = []  # 시도별확진자
    for i, d in enumerate(data):
        region = d.find_all('em', class_='sr-only')[0].text  # 지역이름
        confirmed = d.find_all('span', class_='num')[0].text
        confirmed = int(confirmed)

        confirmed_seoul.append({
            '지역이름': region,
            '확진자수': confirmed
        })

    confirmed_seoul.append({'업데이트날짜': updated})

    return confirmed_seoul


def run():
    data, updated = get_data(
        "https://www.seoul.go.kr/coronaV/coronaStatus.do")
    confirmed_region = parse_data(data, updated)
    # print(confirmed_region)
    save_dir = 'koreaData(Seoul).js'
    crawler_name = 'crawlKoreaData(Seoul).py'
    var_name = 'koreaData(Seoul)'

    write_data(confirmed_region, save_dir, crawler_name, var_name)


run()
