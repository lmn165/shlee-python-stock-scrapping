import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from commons.folder import create_folders, remove_folders
from commons.scrap import WebDriver


def execute_scrapping(srch_key, total_page=1):
    driver = WebDriver()
    driver.add_options(['window-size=1080,720', 'headless'])
    driver = driver.create_driver()
    driver.get('https://finance.naver.com/news/')

    driver.find_element_by_name('q').clear()
    driver.find_element_by_name('q').send_keys(srch_key)
    driver.find_element_by_class_name('schNews').find_element_by_tag_name('a').click()

    cur_page = 1

    # 기사 리스트 페이지 이동
    while (cur_page <= total_page):
        path = f'./data/{srch_key}/{str(cur_page).zfill(3)}/'
        create_folders(path)

        article_counts = len(driver.find_elements_by_class_name('articleSubject'))
        # 기사 리스트에서 각 기사 원문 크롤링
        for i in range(article_counts):
            driver.find_elements_by_class_name('articleSubject')[i].find_element_by_tag_name('a').click()
            soup = BeautifulSoup(driver.page_source, features="html.parser")
            mainContents = soup.select('.articleCont')[0].text.strip()
            print(mainContents)
            date = datetime.strptime(soup.select('.article_date')[0].text,
                                     '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M')

            f = open(path + f'article_{str(date)}.txt', 'w', encoding='utf-8')
            f.write(mainContents)
            f.close()
            del soup
            driver.back()
            driver.implicitly_wait(10)

        cur_page += 1
        cur_css = f'table.Nnavi > tbody > tr > td:nth-child({cur_page})'
        driver.execute_script('var pgLL = document.querySelector(".pgLL");'
                              'var pgL = document.querySelector(".pgL");'
                              'if (pgLL)'
                              'pgLL.parentNode.removeChild(pgLL);'
                              'if (pgL)'
                              'pgL.parentNode.removeChild(pgL);')
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, cur_css))).click()

    time.sleep(3)
    driver.close()


if __name__ == '__main__':
    path = './data/'
    srch_key = '엔비디아'
    # remove_folders(path+srch_key)
    execute_scrapping(srch_key, total_page=3)