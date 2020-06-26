from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

##################################### 셀레니움
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
##############################################


## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('dashboard.html')

@app.route('/stock', methods=['GET'])
def stock_giving():
    stocks = db.stocks.find({}, {'_id' : 0})
    return jsonify({'result':'success'})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)