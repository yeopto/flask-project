from flask import Flask, render_template, jsonify, request
from itsdangerous import json
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbtest

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/post', methods=['POST'])
def post_article():
  head_receive = request.form['head_give']
  comment_receive = request.form['comment_give']
  article = {'head': head_receive, 'comment': comment_receive}
  db.articles.insert_one(article)
  
  return jsonify({'result' : 'success'})

@app.route('/show', methods=['GET'])
def read_article():
  result = list(db.articles.find({},{'_id': False}))
  return jsonify({'result': 'success', 'articles': result})

@app.route('/delete', methods=['POST'])
def delete_article():
  title_receive = request.form['title_give']
  db.articles.delete_one({'head': title_receive})
  return jsonify({'result': 'success'})

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)