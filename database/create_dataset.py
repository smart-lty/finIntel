from database.manage_data import *
from random import shuffle
import pandas as pd
import datetime
from sqlobject import AND


def update_database():
    init()
    codes = pd.read_excel("database/codes.xlsx")
    stock_codes = codes.iloc[:100, 0].to_list()
    for stock_code in stock_codes:
        update_stock(stock_code)


def get_current_weekday(day: datetime.date):
    """
    Return current weekday of current day.
    """
    if day.weekday() == 6:
        pre_day = day - datetime.timedelta(days=2)
    elif day.weekday() == 5:
        pre_day = day - datetime.timedelta(days=1)
    else:
        pre_day = day
    return pre_day
        

def get_next_weekday(day: datetime.date):
    """
    Return next weekday of current day.
    """
    if day.weekday() == 4:
        next_day = day + datetime.timedelta(days=3)
    elif day.weekday() == 5:
        next_day = day + datetime.timedelta(days=2)
    else:
        next_day = day + datetime.timedelta(days=1)
    return next_day
        

def read_database():
    connect()
    
    data = pd.DataFrame(columns=["label", "text"])
    
    news = News.select()
    print(news.count())
    for new in news:
        stock_id, date, title, content = new.stockID, new.date, new.title, new.content
        text = (title + " " + content).replace("\n", " ").replace("\r", " ").replace("\t", " ")

        res1 = Price.select(AND(Price.q.stockID==stock_id, Price.q.date==get_current_weekday(date)))
        res2 = Price.select(AND(Price.q.stockID==stock_id, Price.q.date==get_next_weekday(date)))
        
        if res1.count() and res2.count():
            today_price = float(res1[0].close_price)
            next_day_price = float(res2[0].close_price)
            label = int(next_day_price >= today_price)
            data = data.append(
                pd.DataFrame({
                "label": [label],
                "text": [text],
            }), ignore_index=True)
            
        else:
            continue
            
    indexs = data.index.tolist()
    shuffle(indexs)
    train_size = int(0.8 * len(indexs))
    train, valid = indexs[:train_size], indexs[train_size:]
    train, valid = data.loc[train, :], data.loc[valid, :]
    train.reset_index(drop=True, inplace=True)
    valid.reset_index(drop=True, inplace=True)
    train.to_csv("../data/train_stock.tsv", sep="\t")
    valid.to_csv("../data/dev_stock.tsv", sep="\t")
                
                