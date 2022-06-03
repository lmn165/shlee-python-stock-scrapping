import datetime

import requests
import urllib3
from bs4 import BeautifulSoup as soup
urllib3.disable_warnings()

if __name__ == '__main__':
    baseurl = 'https://finance.naver.com/news/news_read.naver?article_id=0000673432&office_id=031&mode=search&query=amd&page=1'

    nametag = 'articleCont'

    resultarray = []

    pagehtml = requests.get(baseurl, verify=False)
    pagehtmlbs = soup(pagehtml.text, 'html.parser')
    idxname = pagehtmlbs.find('div', class_=nametag)
    idxname.find('div').decompose()
    # print(idxname.text)
    date = datetime.datetime.strptime(pagehtmlbs.find('span', class_='article_date').text, '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M')

    f = open(f'./data/article_{str(date)}.txt', 'w', encoding='utf-8')

    f.write(idxname.text)

    f.close()