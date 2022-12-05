from bottle import route, run, template,request, response
from bottle import static_file
import json
import os
import glob
from PIL import Image

@route('/')
def index():

    level = 'unknown'

    if os.path.exists( "/posted_data/data.json"):
        level = json.load(open( "/posted_data/data.json"))['detections']

    return open('templates/home_page.html').read().replace('[BUSY_LEVEL]',level.title()).replace('[PHOTO_TIME]','')

@route('/data_json/')
def data_json():
    photos = []
    json_obj = {}
    for photo in glob.glob('/posted_data/*.png'):
        photos.append(photo.replace('/posted_data/','').replace('.png','-500.png'))
    for json_path in glob.glob('/posted_data/*-data.json'):
        named_obj = json.load(open(json_path))
        json_obj[named_obj['name']] = named_obj
    response.content_type = 'application/json'
    return json.dumps({'photos':photos,'json':json_obj})


@route('/photo/<p_name>.png')
def photo(p_name):
    if os.path.exists(f"/posted_data/{p_name}.png"):
        im = Image.open(f"/posted_data/{p_name}.png")
        new_im = im.resize((500, 500))
        new_im.save(f'{p_name}-500.png')
        return static_file(f'{p_name}.png',root='/posted_data/')

@route('/upload/json/', method='POST')
def json_upload():
    upload = request.files.get('upload')
    file_path = "/posted_data/data.json"
    if os.path.exists(file_path):
        os.remove(file_path)
    upload.save(file_path)
    json_data = json.load(open(file_path))
    with open('/posted_data/NAME.txt','w') as name:
        name.write(json_data['name'])
    json.dump(json_data,open(f"/posted_data/{json_data['name']}-data.json",'w'))
    return "File successfully saved "

@route('/upload/photo/', method='POST')
def photo_upload():
    upload = request.files.get('upload')
    file_path = f"/posted_data/{open('/posted_data/NAME.txt').read()}.png"
    if os.path.exists(file_path):
        os.remove(file_path)
    upload.save(file_path)
    print(file_path)
    return "File successfully saved "


run(host='0.0.0.0', port=80)
