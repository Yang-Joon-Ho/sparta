import requests
from bs4 import BeautifulSoup
#bs4 전체가 아니라 beautiful만 가져오도록 한다

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# headers는 url보다 덜 중요한 메타데이터
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)

# api가 아니라 html을 가져오는 것이므로 bs4가 필요하다.
# jquery같은거라고 생각하면 됨

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

#############################
#old_content > table > tbody
#< id = 'old_contemt'>
#   <table>
#       <tbody>
# (입맛에 맞게 코딩)

movies = soup.select('#old_content > table > tbody > tr')
# #old_content > table > tbody > tr에 해당하는 모든것을 가져와라 (리스트임)
#print(movies)

for movie in movies :
    
    a_tag = movie.select_one('td.title > div > a')
    #print(point_tag)

    if a_tag != None:
       
        no_tag = movie.select_one('td.ac > img')
        point_tag = movie.select_one('td.point')
        print(no_tag.attrs['alt'] + a_tag.attrs['title'] + point_tag.text)

        #print(f'{no_tag.attrs['alt']} {a_tag.attrs['title']} {point_tag.text}')

# testing

#localhost:27017
#27017이란 몽고디비의 포트 번호
#내 컴퓨터에서 몽고디비에 접속한 것

#관계형 데이터베이스는 직관적이나 너무 정형적이다
#따라서 통계적인 작업을 할때는 편하다 금융권에서 씀

#nosql은 데이터마다의 일관성은 부족하지만 요동성이 있다.
#데이터 각각이 중요한 경우는 nosql 씀 주로 게임에서 씀

#############################

# html에서 
# < >
# 이 사이의 내용들은 text임
# < >