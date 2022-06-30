from data_show import analyse
import datetime

if __name__ == '__main__':
    city = input('请输入你要查找的城市：')
    year = input('请输入你要查找的年份：')
    while int(year) < 2011 or int(year) > datetime.date.today().year:
        print('输入错误，请重新输入')
        year = input('请输入你要查找的年份：')
    analyse(city, year)
