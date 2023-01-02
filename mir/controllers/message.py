
import json
import os
import sys
import datetime
import math
from urllib.parse import parse_qs
#from bson.objectid import ObjectId

import requests
from asgiref.sync import async_to_sync

from common.modules.template import render
from common.modules.body import read
from account.controllers import account
from . import default
#from . import visitor
#from notifications.controllers import notifications


def add(environ):
    
    if not account.get(environ):
        status = '303 See Other'
        response_headers = [
            ('Location', '/sign-in'),
            ('Set-Cookie', 'login=''; path=/; max-age=0'),
            ('Set-Cookie', 'password=''; path=/; max-age=0')
        ]
        content = b''

    elif environ.get('REQUEST_METHOD') == 'POST':
        
        fields = read(environ)

        _tags = fields['tags'].value.strip()
        
        if _tags == '':
            _tags = 'общение'
        
        _tags = _tags.lower().split(' ')
        
        tags = []
        
        for _tag in _tags:
            tags.append(_tag.strip())
        
        #tags = json.dumps(sorted(tags))
        tags = sorted(tags)
        
        if 'title' in fields:
            text = async_to_sync(default.get_link)(fields['text'].value.strip())
        else:
            text = fields['text'].value.strip()
            
        date = datetime.datetime.now()
        user = account.get(environ)
        
        #print(user)
        
        flag = False
        
        if 'file' in fields:
            if fields['file'].filename != '':
                flag = True
                file_name = fields['file'].filename
                file_type = fields['file'].type
                file_size = int(fields['file_size'].value)
                file_bin = fields['file'].value
                
        col = environ['DB']['messages']
                
        if flag == False:
            message = {
                'tags': tags,
                'text': text,
                'file_name': None,
                'file_size': None,
                'file_type': None,
                'file_bin': None,
                'date': date,
                'user_id': user['_id']
            }
            
            message_id = str(col.insert_one(message).inserted_id)
            
            #environ.get('cursor').execute('INSERT INTO messages (tags, text, date, user_id) VALUES (%s, %s, %s, %s) RETURNING id',
                #(tags, text, date, user.id))
        else:
            message = {
                'tags': tags,
                'text': text,
                'file_name': file_name,
                'file_size': file_size,
                'file_type': file_type,
                'file_bin': file_bin,
                'date': date,
                'user_id': user['_id']
            }
            
            message_id = str(col.insert_one(message).inserted_id)
            #environ.get('cursor').execute('INSERT INTO messages (tags, text, file_name, file_size, file_type, file_bin, date, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
                #(tags, text, file_name, file_size, file_type, file_bin, date, user.id))
                
        #message_id = environ.get('cursor').fetchone().id
        
        #environ.get('conn').commit()
        
        async_to_sync(notifications.send)(environ, user, date.strftime('%H:%M (%d.%m.%Y)') + '\n сообщение от ' + user['name'], '/message/' + str(message_id))
        
        status = '303 See Other'
        response_headers = [
            ('Location', '/messages/1'),
        ]
        content = b''
        
    else:
    
        #environ.get('cursor').execute('SELECT tags FROM messages')
        #_tags = environ.get('cursor').fetchall()
        
        col = environ['DB']['messages']
        _tags = col.find({}, {'tags'})
        
        tags = []
        
        for _tag in _tags:
            #print(_tag['tags'])
            ttt = _tag['tags']
            
            for t in ttt:
                if t not in tags:
                    tags.append(t)
            
        tags = sorted(tags)
        
        print(tags)
        
        status = '200 OK'
        content = render('mir', 'add_message.html', tags=tags)
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(content)))
        ]
    
    return status, response_headers, content
    
def get_all(environ):

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
        #arr = environ.get('PATH_INFO').split('/')
        #page = arr[2]

        user = account.get(environ)

        url = 'http://mirumir.infinityfreeapp.com' + environ['RAW_URI']
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
        cookies = dict(__test='52b50e0de65515a3125cefdeaa677792', login=user['login'], password=user['password'])
        
        res = requests.get(url, timeout=30, headers=headers, cookies=cookies, allow_redirects=False)

        if res.encoding == 'ISO-8859-1':
            res.encoding = 'utf-8'
            
        content = (res.text).encode()

        status = '200 OK'
        #content = render('mir', 'messages.html', users=users, tags=tags, messages=messages, pages=pages, page=page, image=image, audio=audio, video=video)
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(content)))
        ]
    
    return status, response_headers, content
    
def get_filtered_all(environ):

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

        user = account.get(environ)

        url = 'http://mirumir.infinityfreeapp.com' + environ['RAW_URI']
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
        cookies = dict(__test='52b50e0de65515a3125cefdeaa677792', login=user['login'], password=user['password'])
        
        res = requests.get(url, timeout=30, headers=headers, cookies=cookies, allow_redirects=False)

        if res.encoding == 'ISO-8859-1':
            res.encoding = 'utf-8'
            
        content = (res.text).encode()
        
        status = '200 OK'
        #content = render('mir', 'messages.html', users=users, tags=tags, tags_number=tags_number, users_filters=users_filters, tags_filters=tags_filters, messages=messages, pages=pages, page=page, image=image, audio=audio, video=video)
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
        user = account.get(environ)

        url = 'http://mirumir.infinityfreeapp.com' + environ['RAW_URI']
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
        cookies = dict(__test='52b50e0de65515a3125cefdeaa677792', login=user['login'], password=user['password'])
        
        res = requests.get(url, timeout=30, headers=headers, cookies=cookies, allow_redirects=False)

        if res.encoding == 'ISO-8859-1':
            res.encoding = 'utf-8'
            
        content = (res.text).encode()
        
        status = '200 OK'
        #content = render('mir', 'messages.html', users=users, tags=tags, tags_number=tags_number, users_filters=users_filters, tags_filters=tags_filters, messages=messages, pages=pages, page=page, image=image, audio=audio, video=video)
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(content)))
        ]

    return status, response_headers, content
    
def remove(environ):
    
    if not account.get(environ):
        status = '303 See Other'
        response_headers = [
            ('Location', '/sign-in'),
            ('Set-Cookie', 'login=''; path=/; max-age=0'),
            ('Set-Cookie', 'password=''; path=/; max-age=0')
        ]
        content = b''
        
    else:
        #arr = environ.get('PATH_INFO').split('/')
        #message_id = arr[3]
        
        user = account.get(environ)
        
        #environ.get('cursor').execute('SELECT user_id FROM messages WHERE id=%s', (message_id,))
        #message = environ.get('cursor').fetchone()
        
        col = environ['DB']['messages']
        message = col.find_one({'_id': ObjectId(message_id)}, {'user_id'})
        
        if message:
            if user['_id'] == message['user_id']:
                #environ.get('cursor').execute('DELETE FROM messages WHERE id=%s', (message_id,))
                #environ.get('conn').commit()
                col.delete_one({'_id': ObjectId(message_id)})
                
                col = environ['DB']['comments']
                col.delete_many({'message_id': ObjectId(message_id)})
        
        status = '303 See Other'
        response_headers = [
            ('Location', '/message/' + str(message_id)),
        ]
        content = b''
            
    return status, response_headers, content

'''
def edit(environ):
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html'),
    ]
    data = b'empty'
    
    if not account.is_verified(environ):
        status = '303 See Other'
        response_headers = [
            ('Location', '/sign-in'),
            ('Set-Cookie', 'login=''; path=/; max-age=0'),
            ('Set-Cookie', 'password=''; path=/; max-age=0')
        ]
        data = b''

        return status, response_headers, data
        
    fields = read(environ)

    post_id = fields['id'].value

    if environ['REQUEST_METHOD'] == 'POST':
    
        if 'deleted' in fields:
            environ.get('cursor').execute('DELETE FROM messages WHERE id=%s', (message_id,))
                    
            environ.get('conn').commit()
                
            status = '303 See Other'
            response_headers = [
                ('Location', '/'),
            ]
            data = b''
        
        else:
        
            url = '/default'
            title = fields['title'].value.strip()
            description = fields['description'].value.strip()
            code = fields['code'].value.strip()

            environ.get('cursor').execute('UPDATE posts SET url=%s, title=%s, description=%s, code=%s WHERE id=%s', (url, title, description, code, post_id))
            environ.get('conn').commit()
            
            if 'nopush' not in fields:
                user = account.get_user(environ)
                date = datetime.datetime.now()
                async_to_sync(notifications.send)(environ, user.login, date.strftime('%H:%M (%d.%m.%Y)') + '\n пост отредактирован пользователем: ' + user.login, 'https://stalevar.pythonanywhere.com/post/' + str(post_id))
        
            status = '303 See Other'
            response_headers = [
                ('Location', '/post/' + post_id),
            ]
            data = b''
        
    else:
        environ.get('cursor').execute('SELECT * FROM message WHERE id=%s', (post_id,))
        message = environ.get('cursor').fetchone()
        
        if post:
            data = render('mir', 'edit_post.html', post=post)
    
    return status, response_headers, data
'''
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

        #environ.get('cursor').execute('SELECT file_type, file_bin FROM messages WHERE id = %s', (ID,)) 
        #message = environ.get('cursor').fetchone()
        
        col = environ['DB']['messages']
        message = col.find_one({'_id': ObjectId(ID)})

        file_type = message['file_type']
        content = message['file_bin']
                
        status = '200 OK'
        response_headers = [
            #('Connection', 'keep-alive'),
            #('Cache-Control', 'public, max-age=0'),
            #('Transfer-Encoding', 'gzip, chunked'),
            ('Cache-Control', 'public, max-age=31536000'),
            ('Accept-Ranges', 'bytes'),
            ('Content-Type', file_type),
            ('Content-Length', str(len(content)))
        ]

    return status, response_headers, content

