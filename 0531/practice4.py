from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta 

# MongoDB에 insert 하기
#db.movies.update_one({'name':'bobby'},{'$set':{'age':19}})
# 'users'라는 collection에 {'name':'bobby','age':21}를 넣습니다.
#db.movies.update_many({'star' : 9.39},{'$set' : {'star' : 0}})

matrix = db.movies.find_one({'title' : '매트릭스'}, {'_id': False})

print(matrix['star'])

users = db.movies.find({'star' : matrix['star']})

for user in users: 
    print(user['title'])


db.movies.update_many({'star' : matrix['star']},{'$set' : {'star' : 0}})

# db.users.update_one({'name':'bobby'},{'$set':{'age':19}})