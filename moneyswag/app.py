from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

#기사 html에 보여주기
@app.route('/article', methods=['GET'])
def listing():

    article = db.articles.find_one({}, {'_id' : 0})
    return jsonify({'result':'success', 'articles':article})

    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    # 2. articles라는 키 값으로 영화정보 내려주기
   

## API 역할을 하는 부분
#최신 기사 가져오기 
@app.route('/article', methods=['POST'])
def saving():

    #url_receive = request.form['url_give']  # 클라이언트로부터 url을 받는 부분
    #comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분

    url_receive = request.form['url_give']
	# 2. meta tag를 스크래핑하기
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    temp_url = soup.select_one('#leftColumn > div.largeTitle > article.js-article-item.articleItem > div.textDiv')
    
    title = temp_url.select_one('a.title').text
    
    #db에 동일한 기사가 없다면 
    if title != db.articles.find_one({})['title']:
        db.articles.delete_many({})
        description = temp_url.select_one('p').text
        url_url = 'https://kr.investing.com' + temp_url.select_one('a')['href'] #한번 더 들어갈 기사 주소
       
        data = requests.get(url_url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        url_image = soup.select_one('#carouselImage')['src']

        article = {'url': url_url, 'image': url_image,
                    'title': title, 'desc': description}

        db.articles.insert_one(article)


    return jsonify({'result': 'success', 'msg':'POST 연결되었습니다!'})


## API 역할을 하는 부분
@app.route('/index', methods=['POST'])
def index_saving():    
    
    url_receive = request.form['url_give']

	# 다우 지수 가져오기 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    temp_index = soup.select_one('#last_last').text

    # 날짜 가져오기
    temp_date = soup.select_one('#quotes_summary_current_data > div > div > div > span.bold.pid-169-time').text

    if db.dow_index.find_one({}) is not None:
        db.dow_index.delete_one({})
        
    dow_index = { 'dow_index' : temp_index, 'date' : temp_date}
    db.dow_index.insert_one(dow_index)

    return jsonify({'result': 'success'})


## API 역할을 하는 부분
@app.route('/index', methods=['GET'])
def index_giving(): 

    dow_index = db.dow_index.find_one({}, {'_id' : 0})
    return jsonify({'result':'success', 'dow_index':dow_index})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)