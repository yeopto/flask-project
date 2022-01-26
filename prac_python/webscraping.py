import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303', headers = headers)
# 어떤 경우엔 웹사이트에서 웹 스크래핑을 막는 경우가 있다, 이때 get메소드의 인자에 headers를 넣어줘야함.
# headers에는 User Agent값이 들어가고 자신의 User-Agent는 https://www.whatismybrowser.com/detect/what-is-my-user-agent 여기서 알 수 있다.

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
soup = BeautifulSoup(data.text, 'html.parser')
movies = soup.select('#old_content > table > tbody > tr')
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.

for movie in movies:
  img_tag = movie.select_one('td.ac > img')
  a_tag = movie.select_one('td.title > div > a')
  td_point_tag = movie.select_one('td.point')
  
  if a_tag and img_tag and td_point_tag is not None:
    print(img_tag.get('alt'), a_tag.text, td_point_tag.text) # 태그의 특정 속성값을 갖고 오기 위해서는 get메소드를 이용한다.