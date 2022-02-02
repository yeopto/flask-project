from pymongo import MongoClient

import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbtest

@app.route('/')
def home():
  return render_template('index.html')

#Create
@app.route('/api/create', methods=['POST'])
def create_stars():
  name_receive = request.form['name_give']
  url_receive = f'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={name_receive}&oquery={name_receive}&tqi=hQo3ylp0J1sssnNj42ZssssssSR-383698'
  
  headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
  data = requests.get(url_receive, headers=headers)
  soup = BeautifulSoup(data.text, 'html.parser')
  
  name = soup.select_one('#content > div.main_pack > section.sc_new > div.cm_top_wrap > div.title_area > h2 > span > strong').text
  img_url = soup.select_one('#content > div.main_pack > section.sc_new > div.cm_content_wrap > div._cm_content_area_profile > div.cm_info_box > div.detail_info > a > img')['src']
  recent_work = soup.select_one('#content > div.main_pack > section.sc_new > div.cm_content_wrap > div.cm_content_area > div._cm_content_area_work > div.cm_info_box > div.scroll_box > div.list_info > div > ul.list > li > div.area_card > div.title_box > strong > a').text
  exist = db.mystar.find_one({'name' : name})
  if exist is None:
    doc = {
      'name': name,
      'img_url': img_url,
      'recent': recent_work,
      'url': url_receive,
      'like': 0 
    }

    db.mystar.insert_one(doc)
    return jsonify({'result': 'success'})
  else:
    return jsonify({'result': 'error'}) 

#Read
@app.route('/api/list', methods=['GET'])
def show_stars():
  stars = list(db.mystar.find({}, {'_id': False}).sort('like', -1))
  return jsonify({'result': 'success', 'stars_list': stars})

#Update
@app.route('/api/like', methods=['POST'])
def like_stars():
  name_receive = request.form['name_give']

  star = db.mystar.find_one({'name': name_receive})
  new_like = star['like'] + 1
  db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})
  return jsonify({'result': 'success'})

#Update
@app.route('/api/hate', methods=['POST'])
def hate_stars():
  name_receive = request.form['name_give']

  star = db.mystar.find_one({'name': name_receive})
  new_like = star['like'] - 1
  if new_like < 0:
    return jsonify({'result': 'error'})
  else:
    db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})
    return jsonify({'result': 'success'})

#Delete
@app.route('/api/delete', methods=['POST'])
def delete_stars():
  name_receive = request.form['name_give']
  db.mystar.delete_one({'name': name_receive})
  return jsonify({'result': 'success'})

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)