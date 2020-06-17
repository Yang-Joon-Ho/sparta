import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import ElementNotVisibleException

#웹 드라이버 설정
path = "D:/chromedriver_win32/chromedriver"
driver = webdriver.Chrome(path)

#db 설정
client = MongoClient('localhost', 27017)
db = client.dbsparta

# DB에 저장할 영화인들의 출처 url을 가져옵니다.
def get_urls():
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    
    driver.get("https://kr.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::a%3Ceq_market_cap;1")
    wait = WebDriverWait(driver, 10)
    #wait.until(expected_conditions.invisibility_of_element((By.CLASS_NAME, 'asgjkarklghkwrjg')))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'symbol left bold elp')))
    #driver.find_element_by_xpath("//i[@class='popupCloseIcon largeBannerCloser']").click()
    data = driver.find_element_by_xpath('//*[@id="resultsTable"]/tbody/tr')
    #경로 : #resultsTable tbody tr

    print(data)
    # data = driver.page_source
    # soup = BeautifulSoup(data, 'html.parser')
    
    # #print(soup)
    # trs = soup.select('#resultsTable > tbody > tr')
    # print(trs)
    # urls = []
    # for tr in trs:
    #     a = tr.select_one('td.symbol.left.bold.elp > a')
    #     if a is not None:
    #         baseurl = 'http://kr.investing.com'
    #         url = baseurl + a['href']
    #         urls.append(url)
    #         print(url)
    #url = 'https://kr.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::a|exchange::a%3Ceq_market_cap;'

    # test_url = 'https://kr.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::a|exchange::a%3Ceq_market_cap;1'
    
    # data = requests.get(test_url, headers = headers)
    # soup = BeautifulSoup(data.text, 'html.parser')

    #data = requests.get('https://kr.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::a|exchange::a%3Ceq_market_cap;1', headers = headers)
    #print(data.text)
    #i = 0


    # for i in range(1,2) :
    #     data = requests.get(url + str(i), headers = headers)
    #     print(data)
    #     soup = BeautifulSoup(data.text, 'html.parser')
        
    #     trs = soup.select('#resultsTable > tbody > tr')
    #     print(trs)
    #     urls = []
    #     for tr in trs:
    #         a = tr.select_one('td.symbol.left.bold.elp > a')
    #         if a is not None:
    #             baseurl = 'http://kr.investing.com'
    #             url = baseurl + a['href']
    #             urls.append(url)
    #             print(url)
        
        

get_urls()

#     trs = soup.select('#old_content > table > tbody > tr')

#     urls = []
#     for tr in trs:
#         a = tr.select_one('td.title > a')
#         if a is not None:
#             baseurl = 'https://movie.naver.com/'
#             url = baseurl + a['href']
#             urls.append(url)

#     return urls

# # 출처 url로부터 영화인들의 사진, 이름, 최근작 정보를 가져오고 mystar 콜렉션에 저장합니다.
# def insert_star(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     data = requests.get(url, headers=headers)

#     soup = BeautifulSoup(data.text, 'html.parser')

#     name = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > h3 > a').text
#     img_url = soup.select_one('#content > div.article > div.mv_info_area > div.poster > img')['src']
#     recent = soup.select_one(
#         '#content > div.article > div.mv_info_area > div.mv_info.character > dl > dd > a:nth-child(1)').text

#     doc = {
#         'name': name,
#         'img_url': img_url,
#         'recent': recent,
#         'url': url,
#         'like': 0
#     }

#     db.mystar.insert_one(doc)
#     print('완료!', name)

# # 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
# def insert_all():
#     db.mystar.drop()  # mystar 콜렉션을 모두 지워줍니다.
#     urls = get_urls()
#     for url in urls:
#         insert_star(url)

# ### 실행하기
# insert_all()
