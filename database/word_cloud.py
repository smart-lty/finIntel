from database.manage_data import *
import datetime
from dateutil import rrule
from sqlobject import AND
import jieba
import re
from wordcloud import WordCloud
from PIL import Image
import numpy as np

def draw_wordcloud(days=365):
    connect()
    today = datetime.date.today()
    first_day = today - datetime.timedelta(days=days)
    news = News.select(AND(News.q.date<=today, News.q.date>=first_day))
    text = ""
    for new in news:
        text += new.title + " " + new.content + " "
    remove = ["，", "。", "\n", "\xa0"]
    for i in remove:
        text = text.replace(i, " ")
    word = jieba.lcut(text)
    
    new_word = [w for w in word if not re.match("\d+\.?\d*", w) and not re.match("\s+", w) and w!="年" and w!="月" and w!="日" and "万" not in w and "亿" not in w]
    fig = WordCloud(background_color="white", font_path='database/SimHei.ttf',mask=np.array(Image.open("database/back.png"))).generate(" ".join(new_word))
    fig.to_file("wc.png")
    photo = Image.open("wc.png")
    photo.show()