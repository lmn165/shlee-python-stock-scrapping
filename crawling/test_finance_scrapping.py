import requests
import urllib3
from bs4 import BeautifulSoup as soup
urllib3.disable_warnings()

def execute_google_finance():
    baseurl = 'https://www.google.com/finance/quote/'
    ticker = ['NVDA:NASDAQ']

    nametag = 'zzDege'
    indexvaluetag = 'YMlKec fxKbKc'

    resultarray = []

    for i in ticker:
        pagehtml = requests.get(baseurl + i, verify=False)
        pagehtmlbs = soup(pagehtml.text, 'html.parser')
        idxname = pagehtmlbs.find('div', class_=nametag).text
        print('Index Name: ' + idxname + ' 입수완료.')
        idxvalue = pagehtmlbs.find('div', class_=indexvaluetag).text
        print('Index Value: ' + idxvalue + ' 입수완료.')
        resultarray.append([idxname, idxvalue])

    print(resultarray)


if __name__ == '__main__':
    execute_google_finance()
