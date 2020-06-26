from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from bson import ObjectId

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
   return render_template('index.html')

@app.route('/interest.html')
def interest():
    return render_template('interests.html')

@app.route('/dashboard.html')
def stock_detail():
    print('in stock_detail')
    return render_template('dashboard.html')

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
    # if title != db.articles.find_one({})['title']:
    if db.articles.find_one({'title' : title}) is None:
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


@app.route('/search', methods=['POST'])
def stock_searching():

    #종목 명을 받음
    stock_receive = request.form['stock_give']
    url_receive = request.form['url_give']
    
    search_url = url_receive + stock_receive     

    driver.get(search_url)
        
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    stocks = soup.select('#fullColumn > div > div > div > div > a')
    
    datas = []
    for stock in stocks:
        if stock.select_one('span[class="second"]') is None:
            continue
        datas.append({'href' : stock['href'],
                'symbol' : stock.select_one('span[class="second"]').text,
                'name' : stock.select_one('span[class="third"]').text,
                'exchange' : stock.select_one('span[class="fourth"]').text
                })

    print(len(datas))
    print(datas)
    if len(datas) == 0:
        return jsonify({'result' : 'fail'})
    else :
        return jsonify({'result' : 'success', 'dictionary' : datas})

    #stock = db.stocks.find_one({'name' : stock_receive}, {'_id' : 0})

    # if stock is None:
    #     return jsonify({'result' : 'fail', 'msg' : '니가 검색한 종목 없음ㅋㅋ'})
    # else:
    #     return jsonify({'result' : 'success', 'stock' : stock})

@app.route('/stock', methods=['POST'])
def stock_saving():

    companyName = request.form['companyName']
    symbol = request.form['symbol']
    primaryExchange = request.form['primaryExchange']
    close = request.form['close']
    industry = request.form['industry']
    website = request.form['website']
    sector = request.form['sector']
    description = request.form['description']

    stock = {'companyName': companyName, 'symbol': symbol,
                'primaryExchange': primaryExchange, 'close': close,
                'industry' : industry, 'website' : website,
                'sector' : sector, 'desc' : description}

    db.stocks.insert_one(stock)

    return jsonify({'result' : 'success'})

@app.route('/stock', methods=['GET'])
def stock_giving():
    stocks = objectIdDecoder(list(db.stocks.find({})))
    return jsonify({'result':'success', 'stocks':stocks})

def objectIdDecoder(list) :
    results = []
    for doc in list:
        doc['_id'] = str(doc['_id'])
        results.append(doc)
    
    return results

@app.route('/stock', methods=['DELETE'])
def delete():

    #클라이언트가 삭제하고자 하는 데이터의 id를 받음

    id_receive = ObjectId(request.form['id_give'])
    db.stocks.delete_one({'_id' : id_receive})
    
    # id_receive = request.form['id_give'] 
    # print(id_receive)
    # db.articles.remove({'_id' : ObjectId(id_receive)})
    return jsonify({'result' : 'success'})


@app.route('/dashboard',methods = ['POST', 'GET'])
def result():

    if request.method == 'POST':
        result = request.form
        return render_template("dashboard.html", result = result)
    
    # elif request.method == 'GET':
    #     print(result)
    #     return jsonify({'result' : 'success', 'symbol' : result})

@app.route('/stock_price', methods=['POST'])
def stock_price():

    url_receive = request.form['url_give']

	# 과거 주가 데이터 가져오기 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    # tr들만 뽑아내기
    prices = soup.select('#Col1-1-HistoricalDataTable-Proxy > section > div > table > tbody > tr')

    # temp = prices.select_one('td > span').text
    # print(temp)
    
    # 1번째가 날짜, 2번쨰가 시가, 3번째가 고가, 4번째가 저가, 5번째가 종가, 6번째가 매매 규모

    datas = []
    for price in prices:
        if len(price.select('td')) <= 2:
            continue
        datas.append({'date' : price.select('td')[0].text, 
        'open' : price.select('td')[1].text,
        'high' : price.select('td')[2].text,
        'low' : price.select('td')[3].text,
        'close' : price.select('td')[4].text,
        'volume' : price.select('td')[6].text,})

    if len(datas) == 0:
        return jsonify({'result' : 'fail'})
    else :
        return jsonify({'result' : 'success', 'dictionary' : datas})
    

@app.route('/current_price', methods=['POST'])
def current_price():
    
    url_receive = request.form['url_give']

	# 과거 주가 데이터 가져오기 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    # tr들만 뽑아내기
    prices = soup.select('#quote-header-info > div > div > div > span')
    
    price = prices[1].text
    rate = prices[2].text

    price_rate = {'price' : price, 'rate' : rate}
    
    return jsonify({'result' : 'succcess', 'price_rate' : price_rate})

@app.route('/order', methods=['POST'])
def save_order():
    
    symbol_receive = request.form['symbol_give']
    price_receive = int(request.form['price_give'])
    date_receive = request.form['date_give']
    quantity_receive = int(request.form['quantity_give'])
    total_receive = int(request.form['total_give'])

    stock = {'symbol': symbol_receive, 'price': price_receive,
                'date': date_receive, 'quantity': quantity_receive,
                'total' : total_receive }

    db.stock_orders.insert_one(stock)
    
    temp = list(db.stock_total.find({'symbol' : symbol_receive}, {'_id' : 0}))
    if len(temp) == 0:
        total = {'symbol' : symbol_receive, 'price' : price_receive, 'quantity': quantity_receive, 'total' : total_receive}
        db.stock_total.insert_one(total)
    else :
        #평균 단가 구해야함ㅋㅋ
        before = db.stock_total.find_one({'symbol' : symbol_receive}, {'_id' : 0})
        total_price_temp = before['price'] * before['quantity'] + total_receive
        total_quantity_temp = before['quantity'] + quantity_receive
        total_total_temp = before['total'] + total_receive 

        price = total_price_temp / total_quantity_temp 
        db.stock_total.update_one({'symbol' : symbol_receive}, { '$set' : { 'price' : price, 'quantity' : total_quantity_temp, 'total' : total_total_temp} })


    return jsonify({'result' : 'success'})

@app.route('/get_total', methods=['POST'])
def get_total():
    

@app.route('/get_order', methods=['POST'])
def get_order():

    symbol_receive = request.form['symbol_give']
    orders = objectIdDecoder(list(db.stock_orders.find({'symbol' : symbol_receive})))

    return jsonify({'result' : 'success', 'orders' : orders})

@app.route('/sell_stock', methods=['DELETE'])
def sell_stock():

    id_receive = ObjectId(request.form['id_give'])
    db.stock_orders.delete_one({'_id' : id_receive})
    
    return jsonify({'result' : 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

