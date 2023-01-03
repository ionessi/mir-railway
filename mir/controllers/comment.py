
import os
import sys
import datetime
import math

import requests
from asgiref.sync import async_to_sync
#from bson.objectid import ObjectId

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

    if environ['REQUEST_METHOD'] == 'POST':
        
        fields = read(environ)

        message_id = fields['message_id'].value
        
        user = account.get(environ)

        url = 'http://mirumir.infinityfreeapp.com' + environ['RAW_URI']
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
        cookies = dict(__test='52b50e0de65515a3125cefdeaa677792', login=user['login'], password=user['password'])
        data = {'message_id': fields['message_id'].value, 'quote': fields['quote'].value, 'text': fields['text'].value}
        
        if 'title' in fields:
            data['title'] = fields['title'].value
        
        if fields['file'].filename != '':
            data['file_size'] = fields['file_size'].value
            files = {'file': (fields['file'].filename, fields['file'].value, fields['file'].type)}
            
            res = requests.post(url, timeout=60, headers=headers, cookies=cookies, data=data, files=files, allow_redirects=False)
            
        else:
            res = requests.post(url, timeout=60, headers=headers, cookies=cookies, data=data, allow_redirects=False)

        if res.encoding == 'ISO-8859-1':
            res.encoding = 'utf-8'
            
        location = res.headers['Location']

        response_headers = [
            ('Location', location),
        ]
        
        status = '303 See Other'
        content = b''
    
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
        #content = render('mir', 'comments.html', users=users, comments=comments, pages=pages, page=page, image=image, audio=audio, video=video)
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
        arr = environ.get('PATH_INFO').split('/')
        comment_id = arr[3]
        message_id = arr[4]
        
        user = account.get(environ)
        
        #environ.get('cursor').execute('SELECT user_id FROM comments WHERE id=%s', (comment_id,))
        #comment = environ.get('cursor').fetchone()
        
        col = environ['DB']['comments']
        comment = col.find_one({'_id': ObjectId(comment_id)}, {'user_id'})
        
        if comment:
            if user['_id'] == comment['user_id']:
                #environ.get('cursor').execute('DELETE FROM comments WHERE id=%s', (comment_id,))
                #environ.get('conn').commit()
                
                col.delete_one({'_id': ObjectId(comment_id)})
        
        status = '303 See Other'
        response_headers = [
            ('Location', '/message/' + message_id),
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
    #query_string = parse_qs(environ['QUERY_STRING'])
    #comment_id = int(query_string.get('id')[0])
    
    comment_id = fields['id'].value

    if environ['REQUEST_METHOD'] == 'POST':
        message_id = int(fields['message_id'].value)
        
        if 'deleted' in fields:
            with psycopg.connect(environ['db']) as conn:
                with conn.cursor() as cur:
                    cur.execute('DELETE FROM comments WHERE id=%s', (comment_id,))
                    
                conn.commit()
        
        else:
            flag = False
            
            #text = default.get_link(fields['text'].value.strip())
            text = async_to_sync(default.get_link)(fields['text'].value.strip())
            original_text = fields['text'].value.strip()
            
            if 'file' in fields:
                if fields['file'].filename != '':
                    flag = True
                    file_name = fields['file'].filename
                    file_type = fields['file'].type
                    file_size = int(fields['file_size'].value)
                    file_bin = fields['file'].value
            
            with psycopg.connect(environ['db'], row_factory=namedtuple_row) as conn:
                with conn.cursor() as cur:
                    if flag == False:
                        cur.execute('UPDATE comments SET text=%s, original_text=%s, mod=mod + 1 WHERE id=%s',
                            (text, original_text, comment_id))
                    else:
                        cur.execute('UPDATE comments SET text=%s, original_text=%s, file_name=%s, file_size=%s, file_type=%s, file_bin=%s, mod=mod + 1 WHERE id=%s',
                            (text, original_text, file_name, file_size, file_type, file_bin, comment_id))
                            
                    #comment_id = (cur.fetchone()).id
                            
                conn.commit()
                
            date = datetime.datetime.now()
            user = account.get_user(environ)
            Thread(target=notifications.send, args=(environ, user.login, date.strftime('%H:%M (%d.%m.%Y)') + '\n комментарий отредактирован пользователем: ' + user.login, 'https://musicfilm.herokuapp.com/comments?page=1',)).start()
        
        status = '303 See Other'
        response_headers = [
            ('Location', '/message?id=' + str(message_id) + '#' + str(comment_id)),
        ]
        data = b''
        
    else:
        with psycopg.connect(environ['db'], row_factory=namedtuple_row) as conn:
            with conn.cursor() as cur:
                #cur.execute('SELECT * FROM topics')
                #topics = cur.fetchall()
                cur.execute('SELECT original_text, message_id FROM comments WHERE id=%s', (comment_id,))
                comment = cur.fetchone()
                
        data = bytes(render('blog', 'edit_comment.html', comment=comment))
    
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

        #environ.get('cursor').execute('SELECT file_type, file_bin FROM comments WHERE id = %s', (ID,)) 
        #comment = environ.get('cursor').fetchone()
        
        col = environ['DB']['comments']
        comment = col.find_one({'_id': ObjectId(ID)})

        file_type = comment['file_type']
        content = comment['file_bin']
                
        status = '200 OK'
        response_headers = [
            ('Cache-Control', 'public, max-age=31536000'),
            ('Accept-Ranges', 'bytes'),
            ('Content-Type', file_type),
            ('Content-Length', str(len(content)))
        ]

    return status, response_headers, content
    
