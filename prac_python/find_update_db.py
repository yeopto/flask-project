from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbtest

matrix = db.movies.find_one({'title' : '매트릭스'})
matrix_score = matrix['star']

movies = list(db.movies.find({'star' : matrix_score}))

for movie in movies:
  print(movie['title'])