import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from commons.folder import create_folders, remove_folders
from commons.scrap import WebDriver


# 네이버 파이낸스에서 키워드 검색 후, 기사 리스트에서 각 기사들을 스크래핑
def execute_scrapping(srch_key, total_page=1):
    driver = WebDriver()
    driver.add_options(["window-size=1080,720", "headless"])
    driver = driver.create_driver()
    driver.get("https://finance.naver.com/news/")

    driver.find_element(by=By.NAME, value="q").clear()
    driver.find_element(by=By.NAME, value="q").send_keys(srch_key)
    driver.find_element(by=By.CLASS_NAME, value="schNews").find_element(by=By.TAG_NAME, value="a").click()

    cur_page = 1
    pad = 0

    # 기사 리스트 페이지 이동
    while cur_page <= total_page:
        print(f"{pad + cur_page}번 페이지 읽는중...")
        path = f"./data/{srch_key}/{str(pad+1).zfill(3)}_{str(pad+10).zfill((3))}/{str(pad + cur_page).zfill(3)}/"
        create_folders(path)

        len(driver.find_elements(by=By.CLASS_NAME, value="articleSubject"))
        # 기사 리스트에서 각 기사 원문 크롤링
        for i in range(5):
            driver.find_elements(by=By.CLASS_NAME, value="articleSubject")[i].find_element(
                by=By.TAG_NAME, value="a"
            ).click()
            soup = BeautifulSoup(driver.page_source, features="html.parser")
            try:
                mainContents = soup.select(".articleCont")[0].text.strip()
                # print(mainContents)
                date = datetime.strptime(soup.select(".article_date")[0].text, "%Y-%m-%d %H:%M").strftime("%Y%m%d%H%M")
                if mainContents:
                    f = open(path + f"article_{str(date)}.txt", "w", encoding="utf-8")
                    f.write(mainContents)
                    f.close()
            except IndexError:
                print('크롤링 순서 에러')
            del soup
            driver.back()
            driver.implicitly_wait(10)

        cur_page += 1
        cur_css = f"table.Nnavi > tbody > tr > td:nth-child({cur_page})"
        driver.execute_script(
            'var pgLL = document.querySelector(".pgLL");'
            'var pgL = document.querySelector(".pgL");'
            "if (pgLL)"
            "pgLL.parentNode.removeChild(pgLL);"
            "if (pgL)"
            "pgL.parentNode.removeChild(pgL);"
        )
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, cur_css))).click()

        if cur_page > 10:
            cur_page = 1
            total_page -= 10
            pad += 10

    time.sleep(3)
    driver.close()


if __name__ == "__main__":
    path = "./data/"
    srch_key = "대한항공"
    remove_folders(path + srch_key)
    execute_scrapping(srch_key, total_page=10)
