from sqlalchemy import ForeignKey
from sqlobject import *
import os
import re
from database.get_data import *
import pandas as pd


class Stock(SQLObject):
    code = col.StringCol(unique=True)
    name = col.StringCol(unique=True)
    close_prices = MultipleJoin('Price')


class Price(SQLObject):
    stock = ForeignKey('Stock')
    date = col.DateCol()
    close_price = col.FloatCol()


class News(SQLObject):
    stock = ForeignKey('Stock')
    date = col.DateCol()
    title = col.StringCol()
    read = col.FloatCol()
    comment = col.FloatCol()
    link = col.StringCol(unique=True)
    content = col.StringCol()


def connect():
    """
    连接数据库（不初始化）
    """
    URI = 'sqlite:/%s' % os.path.abspath("stocks.db")
    connection = connectionForURI(URI)
    sqlhub.processConnection = connection


def init():
    """
    初始化SQLite数据库
    """
    if os.path.exists(os.path.abspath("stocks.db")):
        os.unlink(os.path.abspath("stocks.db"))
    connect()
    Stock.createTable()
    Price.createTable()
    News.createTable()


def update_stock(code, startDate='20211210', endDate=datetime.date.today().strftime('%Y%m%d')):
    sz = re.compile('(sz|SZ)')
    num = re.findall('\d+', code)
    if len(num) != 1:
        raise Exception('输入股票代码有误！')
    isSz = 0
    if re.search(sz, code):
        isSz = 1
    code = num[0]
    stockPrice = get_stock_data(code, isSz, startDate, endDate)
    assert isinstance(stockPrice, pd.DataFrame)
    name = stockPrice['名称'][0]
    try:
        stock = Stock(code=code, name=name)
    except:
        print('股票已存在')
    print("更新价格数据...")
    for _, i in tqdm(stockPrice.iterrows()):
        date = i['日期']
        price = i['收盘价']
        try:
            Price(stock=stock, date=date, close_price=price)
        except:
            continue
    newsAll = get_stock_info(
        code, datetime.datetime.strptime(startDate, '%Y%m%d'))
    assert newsAll is not None, '没有资讯'
    print("更新资讯...")
    for news in tqdm(newsAll):
        try:
            News(stock=stock, **news)
        except:
            continue
