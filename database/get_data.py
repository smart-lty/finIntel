import time
import re
from tqdm import tqdm
import datetime
from tempfile import TemporaryFile
import requests
import requests_html as rh
import pandas as pd
from bs4 import BeautifulSoup


def get_headers():
    return {'User-Agent': rh.user_agent()}


def get_stock_data(code, isSz, startDate, endDate):
    """
    获取股票历史交易数据
    Args:
        code: 股票代码
        is_sz (0/1): 是否深股
        startDate: 开始时间
        endDate: 结束时间
    """
    # 网易财经 这里只获取收盘价，还可以有HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP参数
    url = 'http://quotes.money.163.com/service/chddata.html?code=%d%s&start=%s&end=%s&fields=TCLOSE' % (isSz, code, startDate, endDate)
    try:
        response = requests.get(url, headers=get_headers())
        csvFile = response.content.decode(encoding='gbk')
        # 使用临时文件（数据比较小），不需要额外下载
        with TemporaryFile('w+', encoding='gbk') as tmp:
            tmp.write(csvFile)
            tmp.seek(0)
            stockPrice = pd.read_csv(tmp)
            tmp.close()

        response.close()
        return stockPrice
    except Exception as e:
        print(e)
        print("Cannot Retrieve Stock Data! Please check the stock's code and other args!")


def get_stock_info(code, toDate):
    """
    获取股票资讯（股吧）

    Args:
        code: 股票代码
        toDate (str, optional): 从今日往前一直寻找到多久. Defaults to '20180101'.
    """
    newsAll = []
    # 从第一页开始
    pageNow = 1
    web = 'http://guba.eastmoney.com'
    url = '%s/list,%s,1,f_%d.html' % (web, code, pageNow)
    try:
        response = requests.get(url, headers=get_headers())
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        pager = soup.find('span', class_='pagernums', recursive=True)
        if pager:
            pager = pager['data-pager'].split('|')
            totalNews = int(pager[1])
            perNews = int(pager[2])
        else:
            raise Exception('股票%s没有足够的资讯!或被反爬虫机制检测' % code)
        flag = 0
        for i in range(perNews, totalNews, perNews):
            print("爬取资讯中：%d/%d" % (i, totalNews))
            newsNow = soup.find_all('div', class_=['articleh', 'normal_post'])
            for news in tqdm(newsNow):
                # 阅读数 万 亿
                tmpText = news.find(class_='a1').text
                read = int(re.findall('\d+', tmpText)[0])
                if re.search('万', tmpText):
                    read *= 1e4
                elif re.search('亿', tmpText):
                    read *= 1e8
                # 评论
                tmpText = news.find(class_='a2').text
                comment = int(re.findall('\d+', tmpText)[0])
                if re.search('万', tmpText):
                    comment *= 1e4
                elif re.search('亿', tmpText):
                    comment *= 1e8
                # 标题
                title = news.find(class_='a3').a
                link = web + title['href']
                title = title.text
                respNow = requests.get(link, headers=get_headers())
                soupNow = BeautifulSoup(respNow.text, 'lxml')
                try:
                    contentNow = soupNow.find(id='zwcontent')
                    tmpText = contentNow.find(class_='zwfbtime').text
                    date = re.findall('\d+-\d+-\d+', tmpText)[0]
                    if datetime.datetime.strptime(date, '%Y-%m-%d') < toDate:
                        flag = 1
                        break
                    contentNow = contentNow.find_all(
                        'p', string=re.compile('.*[10-]'))
                    if len(contentNow) == 0:
                        continue
                    else:
                        contentNow = '\n'.join([i.text for i in contentNow])
                except Exception as e:
                    print(e)
                    print('有反爬虫机制，请稍后再试！')
                    continue
                tmpDic = {'date': date, 'title': title, 'link': link,
                          'read': read, 'comment': comment, 'content': contentNow}
                newsAll.append(tmpDic)
                time.sleep(3)
            if flag == 1:
                break
            time.sleep(5)
            pageNow += 1
            url = '%s/list,%s,1,f_%d.html' % (web, code, pageNow)
            response = requests.get(url, headers=get_headers())
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
        return newsAll
    except Exception as e:
        print(e)


# get_stock_data('000006', '1', startDate='20180101',
#                endDate=datetime.date.today().strftime('%Y%m%d'))
# get_stock_info('000006', datetime.datetime.strptime('20180101', '%Y%m%d'))
