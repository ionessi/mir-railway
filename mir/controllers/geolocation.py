
import json
import datetime

from asgiref.sync import async_to_sync
from bson.objectid import ObjectId

from common.modules.template import render
from common.modules.body import read
from account.controllers import account
from . import default
from . import visitor
from notifications.controllers import notifications


def index(environ):

    #visitor.add(environ, '')

    if not account.get(environ):
        status = '303 See Other'
        response_headers = [
            ('Location', '/sign-in'),
            ('Set-Cookie', 'login=''; path=/; max-age=0'),
            ('Set-Cookie', 'password=''; path=/; max-age=0')
        ]
        content = b''

    else:
        status = '200 OK'
        content = render('mir', 'geolocation.html')
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(content)))
        ]
    
    return status, response_headers, content
    
def add(environ):
    
    fields = read(environ)
    
    latitude = fields['latitude'].value
    longitude = fields['longitude'].value
    #text = default.get_link(fields['text'].value.strip())
    text = async_to_sync(default.get_link)(fields['text'].value.strip())
    
    date = datetime.datetime.now()
    user = account.get(environ)
    
    flag = False
    
    if 'file' in fields:
        if fields['file'].filename != '':
            flag = True
            file_name = fields['file'].filename
            file_size = int(fields['file_size'].value)
            file_type = fields['file'].type
            file_bin = fields['file'].value
            
    col = environ['DB']['geolocations']
    
    if flag == False:
        geolocation = {
            'text': text,
            'latitude': latitude,
            'longitude': longitude,
            'file_name': None,
            'file_size': None,
            'file_type': None,
            'file_bin': None,
            'date': date,
            'user_id': user['_id']
        }
        
        col.insert_one(geolocation)
        #environ.get('cursor').execute('INSERT INTO geolocations (text, latitude, longitude, date, user_id) VALUES (%s, %s, %s, %s, %s)',
            #(text, latitude, longitude, date, user.id))
    else:
        geolocation = {
            'text': text,
            'latitude': latitude,
            'longitude': longitude,
            'file_name': file_name,
            'file_size': file_size,
            'file_type': file_type,
            'file_bin': file_bin,
            'date': date,
            'user_id': user['_id']
        }
        
        col.insert_one(geolocation)
        #environ.get('cursor').execute('INSERT INTO geolocations (text, latitude, longitude, file_name, file_size, file_type, file_bin, date, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            #(text, latitude, longitude, file_name, file_size, file_type, file_bin, date, user.id))
            
    #environ.get('conn').commit()
    
    async_to_sync(notifications.send)(environ, user, date.strftime('%H:%M (%d.%m.%Y)') + '\n' + user['name'] + ' поделился своим местоположением', '/geolocation',)
    
    status = '200 OK'
    content = ('Ваше местоположение добавлено!').encode('utf-8')
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(content)))
    ]
    
    return status, response_headers, content
    
def get(environ):

    if not account.get(environ):
        status = '303 See Other'
        response_headers = [
            ('Location', '/sign-in'),
            ('Set-Cookie', 'login=''; path=/; max-age=0'),
            ('Set-Cookie', 'password=''; path=/; max-age=0')
        ]
        content = b''

    else:
        #environ.get('cursor').execute('SELECT id, name FROM users')
        #users = environ.get('cursor').fetchall()
        
        col = environ['DB']['users']
        _users = col.find({}, {'_id', 'name'})
        
        users = []
        for data in _users:
            data['id'] = str(data['_id'])
            users.append(type('UserClass', (), data))
        
        #environ.get('cursor').execute('SELECT id, text, latitude, longitude, file_name, file_type, date, user_id FROM geolocations')
        #geolocations = environ.get('cursor').fetchall()
        
        col = environ['DB']['geolocations']
        _geolocations = col.find({}, {'_id', 'text', 'latitude', 'longitude', 'file_name', 'file_size', 'file_type', 'date', 'user_id'})
        
        geolocations = []
        for data in _geolocations:
            data['id'] = str(data['_id'])
            data['user_id'] = str(data['user_id'])
            geolocations.append(type('GeoClass', (), data))
        #print(geolocations)
        
        arr = []
        for geolocation in geolocations:
            for user in users:
                #print(geolocation.user_id)
                #print(user.id)
                if geolocation.user_id == user.id:
                    arr.append([geolocation.id, geolocation.text, geolocation.latitude, geolocation.longitude, geolocation.file_name, geolocation.file_type, geolocation.date.strftime('%H:%M (%d.%m.%Y)'), user.name])
        
        status = '200 OK'
        content = (json.dumps(arr)).encode()
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(content)))
        ]
    
    return status, response_headers, content
    
def get_file(environ):

    if not account.get(environ):
        status = '303 See Other'
        response_headers = [
            ('Location', '/sign-in'),
            ('Set-Cookie', 'login=''; path=/; max-age=0'),
            ('Set-Cookie', 'password=''; path=/; max-age=0')
        ]
        content = b''
        
    else:
        arr = environ.get('PATH_INFO').split('/')
        ID = arr[3]

        #environ.get('cursor').execute('SELECT file_type, file_bin FROM geolocations WHERE id = %s', (ID,)) 
        #geolocation = environ.get('cursor').fetchone()
        
        col = environ['DB']['geolocations']
        geolocation = col.find_one({'_id': ObjectId(ID)})

        file_type = geolocation['file_type']
        content = geolocation['file_bin']
                
        status = '200 OK'
        response_headers = [
            ('Cache-Control', 'public, max-age=31536000'),
            ('Accept-Ranges', 'bytes'),
            ('Content-Type', file_type),
            ('Content-Length', str(len(content)))
        ]

    return status, response_headers, content
    
