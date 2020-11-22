import requests
from bs4 import BeautifulSoup
from utils import write_data

import pandas as pd

def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    updated = soup.find('small', class_='date').text # 업데이트날짜
    data = soup.select('.content_box>.mt-4.zone>dl')
    data.pop()

    return data, updated


def parse_data(data, updated):
    confirmed_Gyeonggi = []  # 시도별확진자
    for i , d in enumerate(data):
        region = d.find_all('dt')[0].text
        confirmed = d.find_all('strong')[0].text
        confirmed = confirmed.replace(',','')
        confirmed = int(confirmed)

        confirmed_Gyeonggi.append({
            '지역이름': region,
            '확진자수': confirmed
        })

    del confirmed_Gyeonggi[0]
    return confirmed_Gyeonggi

def run():
    data, updated = get_data(
        "https://www.gg.go.kr/contents/contents.do?ciIdx=1150&menuId=2909")
    confirmed_region = parse_data(data, updated)
    # print(confirmed_region)
    save_dir = 'koreaData(Gyeonggi).js'
    crawler_name = 'crawlKoreaData(Gyeonggi).py'
    var_name = 'koreaData(Gyeonggi)'

    write_data(confirmed_region, save_dir, crawler_name, var_name)


run()






