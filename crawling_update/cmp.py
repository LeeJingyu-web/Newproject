import requests
from bs4 import BeautifulSoup
from utils import write_data
import json
import time
import datetime

def compare_data(js_file1, js_file2):
    confirmed_cmp_seoul = []
    with open(js_file1, "r", encoding="utf-8") as f1:
        with open(js_file2, "r", encoding="utf-8") as f2:
            json_data_1 = json.load(f1)
            json_data_2 = json.load(f2)
            for i in range(0, len(json_data_1) - 1):
                #지역이름 같은지 확인해야됨
                region = json_data_1[i]['지역이름']
                confirmed_1 = json_data_1[i]['확진자수']
                confirmed_2 = json_data_2[i]['확진자수']
                cmp_data = confirmed_1 - confirmed_2

                confirmed_cmp_seoul.append({
                    '지역이름' : region,
                    '전날비교' : cmp_data
                 })

            return confirmed_cmp_seoul

시간 = time.localtime()
year = 시간.tm_year
mon = 시간.tm_mon
day = 시간.tm_mday
today = str(datetime.date(year, mon, day))
yesterday = str(datetime.date(year, mon, day-1))

today_file = 'koreaData_Seoul_' + today + '.js'
yesterday_file = 'koreaData_Seoul_' + yesterday + '.js'

def run():
    data = compare_data(today_file, yesterday_file)
    # print(confirmed_region)
    save_dir = 'cmp_koreaData_Seoul_new.js'
    crawler_name = 'cmp_crawlKoreaData_Seoul.py'
    var_name = 'cmp_koreaData_Seoul'

    write_data(data, save_dir, crawler_name, var_name)


run()




