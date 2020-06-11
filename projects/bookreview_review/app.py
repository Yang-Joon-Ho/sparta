from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
#Flask 인스턴스를 생성한 것이다. python에서 __name__은 
#모듈의 이름을 뜻한다. app이라는 파이썬 파일을 만들었다고 
#보면 된다. 

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta


##html을 주는 부분
@app.route('/')
def home() :
    return render_template('index.html')

##API 역할 하는 부분
@app.route('/reviews', methods=['POST'])
def write_review():
    title_receive = request.form['title_give']
    author_receive = request.form['author_give']
    review_receive = request.form['review_give']

    review = {
        'title' : title_receive,
        'author' : author_receive,
        'review' : review_receive
    }
    db.reviews.insert_one(review)   

    return jsonify({'result':'success', 'msg' : '리뷰가 성공적으로 작성 되었습니다.',})

@app.route('/reviews', methods=['GET'])
def read_reviews():

    reviews = list(db.reviews.find({}, {'_id' : 0}))
    return jsonify({'result' : 'success', 'reviews' : reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
