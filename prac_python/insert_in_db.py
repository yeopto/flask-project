import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbtest

data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303')
soup = BeautifulSoup(data.text, 'html.parser')

movies = soup.select('#old_content > table > tbody > tr')

for movie in movies:
  a_tag = movie.select_one('td.title > div > a')
  if a_tag is not None:
    rank = movie.select_one('td:nth-child(1) > img').get('alt')
    title = a_tag.text
    star = movie.select_one('td.point').text
    doc  = {
      'rank' : rank,
      'title' : title,
      'star' : star,
    }
    db.movies.insert_one(doc)