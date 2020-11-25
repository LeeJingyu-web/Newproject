import requests
from bs4 import BeautifulSoup
from utils import write_data
import time
import datetime
from datetime import date, timedelta

def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    updated = soup.select('.timetable > .info > span')[0].text  # 업데이트날짜

    data = soup.select('.rpsa_detail > div > div')

    data.pop()
    return data, updated

def parse_data(data, updated):
    confirmed_region = []  # 시도별확진자

    for i, d in enumerate(data):
        region = d.find_all('h4', class_='cityname')[0].text  # 지역이름
        confirmed = d.find_all('span', class_='num')[0].text
        temp = d.find_all('span', class_='num')
        confirmed, _ ,recovered, deaths, confirmed_rate = [
            element.text.replace(',', '') for element in temp]
        confirmed = int(confirmed)

        confirmed_region.append({
            '지역이름': region,
            '확진자수': confirmed
        })

    confirmed_region.append({'업데이트날짜': updated})

    return confirmed_region

today = date.today()
yesterday = date.today() - timedelta(1)
a = str(today)
b = str(yesterday)


def run():
    data, updated = get_data(
        "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=")
    confirmed_region = parse_data(data, updated)
    # print(confirmed_region)
    save_dir = 'koreaData_All'+ '_'+ a +'.js'
    crawler_name = 'crawlKoreaData_All.py'
    var_name = 'koreaData_All'

    write_data(confirmed_region, save_dir, crawler_name, var_name)


run()