from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from bson import ObjectId

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
#client = MongoClient('mongodb://ho1920:foavkq250@localhost',27017)
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def listing():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    # 2. articles라는 키 값으로 영화정보 내려주기
    articles = objectIdDecoder(list(db.articles.find({}).sort('_id',-1)))

    return jsonify({'result':'success', 'articles':articles})

def objectIdDecoder(list) :
    results = []
    for doc in list:
        doc['_id'] = str(doc['_id'])
        results.append(doc)
    
    return results

@app.route('/memo', methods=['DELETE'])
def delete():

    #클라이언트가 삭제하고자 하는 데이터의 id를 받음

    id_receive = ObjectId(request.form['id_give'])
    db.articles.delete_one({'_id' : id_receive})

    print(id_receive)
    # id_receive = request.form['id_give'] 
    # print(id_receive)
    # db.articles.remove({'_id' : ObjectId(id_receive)})
    return jsonify({'result' : 'success'})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():

    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    
    try:
        data = requests.get(url_receive, headers = headers)
        #reqeusts.get을 통해 해당 url에 headers를 가지고 접속
        #html을 가져온다
    except requests.exceptions.MissingSchema:
        return jsonify({'result':'success', 'msg' : 'url 제대로 적으셈ㅋ'})
    except requests.exceptions.InvalidURL:
        return jsonify({'result':'success', 'msg' : 'url 제대로 적으셈ㅋ'})
    except requests.exceptions.InvalidSchema:
        return jsonify({'result':'success', 'msg' : 'url 앞에 붙어있는거 지우셈'})
    #한글 인코딩이 깨지는 문제를 해결하기 위함
    data.encoding = None
    soup = BeautifulSoup(data.text, 'html.parser')

    #기존에는 suop.select로 여러개의 meta 태그를 가져왔다면 
    #이 경우에는 meta 태그의 특정 속성값을 지닌 데이터들을 
    #하나씩 가져온것이다. 
    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_desc = soup.select_one('meta[property="og:description"]')
		
    url_image = og_image['content']
    url_title = og_title['content']
    url_desc = og_desc['content']

    article = {
        'url' : url_receive,
        'comment' : comment_receive,
        'image' : url_image,
        'title' : url_title,
        'description' : url_desc
    }

    db.articles.insert_one(article)

    # 1. 클라이언트로부터 데이터를 받기
	# 2. meta tag를 스크래핑하기
	# 3. mongoDB에 데이터 넣기
    return jsonify({'result': 'success', 'msg' : '저장 완료'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
