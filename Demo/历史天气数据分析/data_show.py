# -*- coding=gbk -*-

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Radar, Timeline
from spider import scraping
import datetime


def weather(df, city, year):
    df['����'] = df['����'].apply(lambda x: pd.to_datetime(x))  # ת������������
    df['month'] = df['����'].dt.month
    df_agg = df.groupby(['month', '����']).size().reset_index()
    df_agg.columns = ['month', '����', 'count']

    time_line = Timeline()
    time_line.add_schema(play_interval=2000)  # ����ʱ���� 2s

    for month in df_agg['month'].unique():
        if (int(year) == datetime.date.today().year and month < datetime.date.today().month) \
                or int(year) < datetime.date.today().year:
            weather_info = df_agg[df_agg['month'] == month][['����', 'count']] \
                .sort_values(by='count', ascending=True).values.tolist()
            bar = Bar()
            bar.add_xaxis([x[0] for x in weather_info])  # x�� ��������
            bar.add_yaxis('', [x[1] for x in weather_info])  # y�� ���ִ���
            bar.reversal_axis()
            bar.set_series_opts(label_opts=opts.LabelOpts(position='right'))  # ��������ǩ������ͼ���ұ�
            bar.set_global_opts(title_opts=opts.TitleOpts(title=f'{year}��{month}�µ��������', subtitle=city))
            time_line.add(bar, f'{month}��')

    time_line.render('weather.html')


def temperature(df, city, year):
    df['����'] = df['����'].apply(lambda x: pd.to_datetime(x))
    df['month'] = df['����'].dt.month
    df['day'] = df['����'].dt.day

    time_line = Timeline()
    time_line.add_schema(play_interval=2000)

    for month in df['month'].unique():
        if (int(year) == datetime.date.today().year and month < datetime.date.today().month) \
                or int(year) < datetime.date.today().year:
            data = df[df['month'] == month]
            line = Line()
            line.add_xaxis(data['day'].tolist())
            line.add_yaxis(
                series_name='�������',
                y_axis=data['�������'].tolist(),
                markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_='average', name='ƽ��ֵ')])
            )
            line.add_yaxis(
                series_name='�������',
                y_axis=data['�������'].tolist(),
                markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_='average', name='ƽ��ֵ')])
            )
            line.set_global_opts(title_opts=opts.TitleOpts(title=f'{year}��{month}�·ݵ����±仯', subtitle=city))
            time_line.add(line, f'{month}��')

    time_line.render('temperature.html')


def wind(df, city, year):
    directions = ['������', '����', '������', '����', '���Ϸ�', '�Ϸ�', '���Ϸ�', '����']
    schema = []
    v = []
    days = df['����'].value_counts()
    days_max = int(days.max())
    for d in directions:
        schema.append(opts.RadarIndicatorItem(name=d, max_=days_max + 5))
        v.append(int(days[d]))
    v = [v]
    radar = Radar()
    radar.add(
        series_name='����ͳ��',
        data=v
    )
    radar.add_schema(
        schema=schema,
        splitarea_opt=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)),
    )
    radar.set_global_opts(title_opts=opts.TitleOpts(title=f'{year}�����ͳ��', subtitle=city))
    radar.render('wind.html')


def analyse(city, year):
    scraping(city, year)
    print('���ڽ������ݷ���...')
    file_data = pd.read_csv(f'{city}.csv', encoding='gbk')
    weather(file_data, city, year)
    temperature(file_data, city, year)
    wind(file_data, city, year)
    print('���ݷ������')
