import requests
from bs4 import BeautifulSoup
from utils import write_data

import pandas as pd

def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    updated = soup.select('.timetable > .info > span')[0].text  # 업데이트날짜
    #print(updated)
    data = soup.select('.rpsa_detail > div > div')
    #print(data)
    data.pop()
    return data, updated


def parse_data(data, updated):
    confirmed_region = []  # 시도별확진자

    for i, d in enumerate(data):
        region = d.find_all('h4', class_='cityname')[0].text  # 지역이름
        temp = d.find_all('span', class_='num')
        print(region)
        confirmed, _, recovered, deaths, confirmed_rate = [
            element.text.replace(',', '') for element in temp]
        confirmed = int(confirmed)  # 확진자수
        recovered = int(recovered)  # 격리해제수
        deaths = int(deaths)  # 사망자수
        confirmed_rate = float(confirmed_rate)  # 십만명당발생율

        if i != 0:
            slicing = d.find_all('p', class_='citytit')[0].text
            confirmed_region_rate = float(
                slicing[:slicing.find('%')])  # 지역별확진자비율
        else:
            confirmed_region_rate = ''

        confirmed_region.append({
            '지역이름': region,
            '확진자수': confirmed,
            '격리해제수': recovered,
            '사망자수': deaths,
            '십만명당발생율': confirmed_rate,
            '지역별확진자비율': confirmed_region_rate,
        })

    confirmed_region.append({'업데이트날짜': updated})

    return confirmed_region

def run():
    data, updated = get_data(
        "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=")
    confirmed_region = parse_data(data, updated)
    # print(confirmed_region)
    save_dir = 'koreaRegionalData.js'
    crawler_name = 'crawlKoreaRegionalData.py'
    var_name = 'koreaRegionalData'

    write_data(confirmed_region, save_dir, crawler_name, var_name)


run()
#############################soup#####################################

# url = "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun="
# res = requests.get(url)
# res.raise_for_status()
#
# soup = BeautifulSoup(res.text, "lxml")
#
#
# current = (soup.find("dd", attrs={"class":"ca_value"}))
#print("현재 확진자 수 : " + current.get_text())

#############################pandas########################################

# f = open('확진자수크롤링.csv', 'w', encoding='utf-8')
# f.write("현재 확진자 수 : " + current.get_text())
# f.close()
#
# df = pd.read_csv("C:\\nope\\확진자수크롤링.csv")
# print(df)

#############################open_source####################################

# import json
# with open('koreacrawl.js', 'r', encoding='UTF-8-sig') as f:
#     data = json.load(f)
# import json
from datetime import date
today = date.today()
day = today.strftime(f"{today.month}/{today.day}")

from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import pandas as pd

html = urlopen("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun=")
source = html.read()
html.close()

soup = BeautifulSoup(source, 'lxml')
table = soup.find("div", class_ = "data_table mgt16")
tables2 = table.find_all("td")

num=[]
for i in range(0, len(tables2)) :
    a = tables2[i].get_text()
    num.append(a)
# print(num)

# before_tot = data[len(data)-1][1]
# print(before_tot)
today_tot = int(num[0].replace(',',''))
###print(today_tot)
# diff=today_tot - before_tot
# death = int(num[3])
# release = int(num[1].replace(',',''))
#
# now = []
# now.append(day)
# now.append(today_tot)

# now.append(diff)
# now.append(death)
# now.append(release)
#
# if data[len(data)-1][0] == day :
#     with open('koreacrawl.js', 'r') as f:
#         data = json.load(f)
# else :
#     data.append(now)
#
# with open('koreacrawl.js', 'w', encoding='utf-8') as make_file:
#     json.dump(data, make_file, indent="\t")
# data








