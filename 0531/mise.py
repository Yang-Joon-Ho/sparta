import requests # requests 라이브러리 설치 필요

r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
rjson = r.json()

gus = rjson['RealtimeCityAir']['row']
#gus라는 리스트에 삽입

for gu in gus:
    if gu['IDEX_MVL'] > 80:
	    print(gu['MSRSTE_NM'], gu['IDEX_MVL'])

# 스크래핑, 크롤링 모두 request를 이용하여 웹 페이지에 접근한다

# 스크래핑
# : 특정 목적을 가지고 특정 페이지에 접근하는 것

# 크롤링
# : 특정 웹사이트와 연결된 모든것에 접속하는 방식

