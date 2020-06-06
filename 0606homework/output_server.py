from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta 

# MongoDB에 insert 하기
#db.movies.update_one({'name':'bobby'},{'$set':{'age':19}})
# 'users'라는 collection에 {'name':'bobby','age':21}를 넣습니다.
#db.movies.update_many({'star' : 9.39},{'$set' : {'star' : 0}})

artist = db.musics.find_one({'artist' : '아이유 (IU)'}, {'_id': False})

singers = db.musics.find({'artist' : artist['artist']})

print('아이유 노래 : \n')
for singer in singers: 
    print(singer['title'])
