import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from commons.folder import create_folders

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1080,720")
    options.add_argument("headless")
    driver = webdriver.Chrome("../resources/chromedriver.exe", options=options)
    driver.get("https://finance.naver.com/news/")

    driver.find_element_by_name("q").clear()
    driver.find_element_by_name("q").send_keys("엔비디아")
    driver.find_element_by_class_name("schNews").find_element_by_tag_name("a").click()

    cur_page = 1
    total_page = 2

    # 기사 리스트 페이지 이동
    while cur_page <= total_page:
        samples = len(driver.find_elements_by_class_name("articleSubject"))
        path = f"./data/{str(cur_page).zfill(3)}/"
        create_folders(path)

        # 기사 리스트에서 각 기사 원문 크롤링
        for i in range(samples):
            time.sleep(2)
            driver.find_elements_by_class_name("articleSubject")[i].find_element_by_tag_name("a").click()
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")
            mainContents = soup.select(".articleCont")
            print(mainContents[0].text)
            date = datetime.strptime(soup.select(".article_date")[0].text, "%Y-%m-%d %H:%M").strftime("%Y%m%d%H%M")

            f = open(path + f"article_{str(date)}.txt", "w", encoding="utf-8")
            f.write(mainContents[0].text.strip())
            f.close()
            time.sleep(2)
            del soup
            driver.back()
        cur_page += 1
        cur_css = f"table.Nnavi > tbody > tr > td:nth-child({cur_page})"
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, cur_css))).click()

    time.sleep(3)
    driver.close()
