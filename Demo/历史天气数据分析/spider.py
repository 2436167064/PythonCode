import requests
import xpinyin
from lxml import etree
import csv


def get_weather(url):
    weather_info = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37'
    }
    resp = requests.get(url, headers=headers)
    resp_list = etree.HTML(resp.text).xpath("//ul[@class='thrui']/li")  # 提取当页所有数据（每个月）

    for li in resp_list:
        day_weather_info = {}
        # 日期
        day_weather_info['data_time'] = li.xpath('./div[1]/text()')[0].split(' ')[0]
        # 最高气温
        high = li.xpath('./div[2]/text()')[0]
        day_weather_info['high'] = high[:high.find('℃')]
        # 最低气温
        low = li.xpath('./div[3]/text()')[0]
        day_weather_info['low'] = low[:low.find('℃')]
        # 天气状况
        day_weather_info['weather'] = li.xpath('./div[4]/text()')[0]
        # 风向
        day_weather_info['wind'] = li.xpath('./div[5]/text()')[0].split(' ')[0]
        weather_info.append(day_weather_info)
    # print(weather_info)
    return weather_info


def scraping(city, year):
    print('正在爬取数据...')

    weathers = []

    for month in range(1, 13):
        weather_time = f'{year}' + ('0' + str(month) if month < 10 else str(month))
        url = f'http://lishi.tianqi.com/{xpinyin.Pinyin().get_pinyin(city, "")}/{weather_time}.html'
        weather = get_weather(url)
        weathers.append(weather)

    with open(f'{city}.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # 写入列名：columns_name
        writer.writerow(['日期', '最高气温', '最低气温', '天气', '风向'])

        # 写入数据
        list_year = []
        for month_weather in weathers:
            for day_weather_dict in month_weather:
                list_year.append(list(day_weather_dict.values()))
        writer.writerows(list_year)

    print('数据爬取完成')
