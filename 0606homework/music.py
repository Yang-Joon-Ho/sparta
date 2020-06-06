import requests
from bs4 import BeautifulSoup


from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  
# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')


# select를 이용해서, tr들을 불러오기
musics = soup.select('#body-content > div.newest-list > div.music-list-wrap > table.list-wrap > tbody > tr.list')

#print(musics)

for music in musics:

    title = music.select_one('td.check > input')['title']

    if title is not None:
        #td.number의 텍스트 부분을 보면 랭킹 이외에 랭킹의 상승 하강을 나타내는 텍스트가 있다
        #여기서 파이썬으로 문자열을 조작하는 것이 아닌 애초에 텍스트를 일부만 가져올 수 있는 방법은 없나?
        num = music.select_one('td.number').text.split()[0] 
        singer = music.select_one('td.info > a.artist').text

        strFormat = '%-3s'
        strOut = strFormat % (num)

        print(strOut + title + ' - ' + singer)
        