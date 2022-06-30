# -*- coding=gbk -*-

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Radar, Timeline
from spider import scraping
import datetime


def weather(df, city, year):
    df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x))  # 转换成日期类型
    df['month'] = df['日期'].dt.month
    df_agg = df.groupby(['month', '天气']).size().reset_index()
    df_agg.columns = ['month', '天气', 'count']

    time_line = Timeline()
    time_line.add_schema(play_interval=2000)  # 设置时间间隔 2s

    for month in df_agg['month'].unique():
        if (int(year) == datetime.date.today().year and month < datetime.date.today().month) \
                or int(year) < datetime.date.today().year:
            weather_info = df_agg[df_agg['month'] == month][['天气', 'count']] \
                .sort_values(by='count', ascending=True).values.tolist()
            bar = Bar()
            bar.add_xaxis([x[0] for x in weather_info])  # x轴 天气名称
            bar.add_yaxis('', [x[1] for x in weather_info])  # y轴 出现次数
            bar.reversal_axis()
            bar.set_series_opts(label_opts=opts.LabelOpts(position='right'))  # 将计数标签放置在图形右边
            bar.set_global_opts(title_opts=opts.TitleOpts(title=f'{year}年{month}月的天气情况', subtitle=city))
            time_line.add(bar, f'{month}月')

    time_line.render('weather.html')


def temperature(df, city, year):
    df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x))
    df['month'] = df['日期'].dt.month
    df['day'] = df['日期'].dt.day

    time_line = Timeline()
    time_line.add_schema(play_interval=2000)

    for month in df['month'].unique():
        if (int(year) == datetime.date.today().year and month < datetime.date.today().month) \
                or int(year) < datetime.date.today().year:
            data = df[df['month'] == month]
            line = Line()
            line.add_xaxis(data['day'].tolist())
            line.add_yaxis(
                series_name='最高气温',
                y_axis=data['最高气温'].tolist(),
                markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_='average', name='平均值')])
            )
            line.add_yaxis(
                series_name='最低气温',
                y_axis=data['最低气温'].tolist(),
                markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_='average', name='平均值')])
            )
            line.set_global_opts(title_opts=opts.TitleOpts(title=f'{year}年{month}月份的气温变化', subtitle=city))
            time_line.add(line, f'{month}月')

    time_line.render('temperature.html')


def wind(df, city, year):
    directions = ['西北风', '北风', '东北风', '东风', '东南风', '南风', '西南风', '西风']
    schema = []
    v = []
    days = df['风向'].value_counts()
    days_max = int(days.max())
    for d in directions:
        schema.append(opts.RadarIndicatorItem(name=d, max_=days_max + 5))
        v.append(int(days[d]))
    v = [v]
    radar = Radar()
    radar.add(
        series_name='风向统计',
        data=v
    )
    radar.add_schema(
        schema=schema,
        splitarea_opt=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)),
    )
    radar.set_global_opts(title_opts=opts.TitleOpts(title=f'{year}年风向统计', subtitle=city))
    radar.render('wind.html')


def analyse(city, year):
    scraping(city, year)
    print('正在进行数据分析...')
    file_data = pd.read_csv(f'{city}.csv', encoding='gbk')
    weather(file_data, city, year)
    temperature(file_data, city, year)
    wind(file_data, city, year)
    print('数据分析完成')
