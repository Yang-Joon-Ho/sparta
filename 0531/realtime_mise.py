import requests # requests 라이브러리 설치 필요

r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
# 위의 내용은 ajax에서 하던것과 같다. data부분은 생략되었고, success는 없다.
# html의 경우 여러가지의 화면으로 나누어져 있고 각 화면 당 연결되어 있는 서버 또한 다르다 
# 단 서버단의 경우 굳이 async로 할 필요가 없다 그러면 너무 복잡하다.
# 서버에서는 async가 아닌 sync를 사용하므로 success부분이 없다.
# 백엔드에서는 코드의 가시성을 위해 sync로 하는게 낫다
# 요청에 대한 결과 ajax로 치면 response가 r이다. 

print(r)
#응답이 200으로 오는데, 정상적으로 응답이 왔다는것을 의미함, 서버 에러이면 500, 클라이언트 에러면 400 이런식이다. 

rjson = r.json() # dictionary 형태로 변환하라
print(rjson)

print(rjson['RealtimeCityAir']['row'][0]['NO2'])
#asynchronous, synchronous 기억할 것
