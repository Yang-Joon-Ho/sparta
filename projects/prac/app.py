from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

## URL 별로 함수명이 같거나,
## route('/') 등의 주소가 같으면 안됩니다.

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/mypage')
def mypage():
   return render_template('mypage.html')

   ## API 역할을 하는 부분
@app.route('/test', methods=['POST'])
def test_post():
   #request 는 프론트엔드에서 넘겨주는 딕셔너리
   # post와 get은 request에서 데이터 가져오는 방식이 다름 
   title_receive = request.form['title_give']
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 POST!'})

@app.route('/test', methods=['GET'])
def test_get():
   title_receive = request.args.get('title_give')
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 GET!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)

