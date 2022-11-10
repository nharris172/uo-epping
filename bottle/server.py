from bottle import route, run, template,request
from bottle import static_file
import json
import os
@route('/')
def index():

    level = 'unknown'

    if os.path.exists( "/posted_data/data.json"):
        level = json.load(open( "/posted_data/data.json"))['detections']

    return open('templates/home_page.html').read().replace('[BUSY_LEVEL]',level.title()).replace('[PHOTO_TIME]','')

@route('/photo.jpg')
def photo():
    if os.path.exists("/posted_data/photo.png"):

        return static_file('photo.png',root='/posted_data/')

@route('/upload/json/', method='POST')
def json_upload():
    upload = request.files.get('upload')
    file_path = "/posted_data/data.json"
    if os.path.exists(file_path):
        os.remove(file_path)
    upload.save(file_path)
    return "File successfully saved "

@route('/upload/photo/', method='POST')
def photo_upload():
    upload = request.files.get('upload')
    file_path = "/posted_data/photo.png"
    if os.path.exists(file_path):
        os.remove(file_path)
    upload.save(file_path)
    print(file_path)
    return "File successfully saved "


run(host='0.0.0.0', port=80)
