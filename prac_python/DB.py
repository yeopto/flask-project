import requests
from bs4 import BeautifulSoup
# from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
# db = client.dbtest

data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303')
soup = BeautifulSoup(data.text, 'html.parser')

movies = soup.select('#old_content > table > tbody > tr')

for movie in movies:
  rank = movie.select_one('td.ac > img').get('alt')
  title = movie.select_one('td.title > div > a').text
  star = movie.select_one('td.point').text
  
  if rank and title and star is not None:
    print(rank, title, star)