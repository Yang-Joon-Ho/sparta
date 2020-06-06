from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta 

# MongoDB에 insert 하기
#db.movies.update_one({'name':'bobby'},{'$set':{'age':19}})
# 'users'라는 collection에 {'name':'bobby','age':21}를 넣습니다.
#db.movies.update_many({'star' : 9.39},{'$set' : {'star' : 0}})

print('가수 이름 입력 : ')
input = input()

musics = db.musics.find({})

print('\n' + input + '의 노래 : ')
for music in musics :
    string = music['artist']
    string = string.split('(')
    
    first = string[0].strip(' ')
    last = ''
    if len(string) > 1:
        last = string[1].strip(')')

    if input == first :
        print(music['title'])
    elif input == last:
        print(music['title'])
    

