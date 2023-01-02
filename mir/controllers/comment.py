
import os
import sys
import datetime
import math

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
        
        flag = False
        
        message_id = fields['message_id'].value
        #text = default.get_link(fields['text'].value.strip())
        
        #environ.get('cursor').execute('SELECT id FROM messages WHERE id=%s', (message_id,))
        #message = environ.get('cursor').fetchone()
        
        col = environ['DB']['messages']
        message = col.find_one({'_id': ObjectId(message_id)}, {'_id'})
        
        if message:
            if 'title' in fields:
                text = async_to_sync(default.get_link)(fields['text'].value.strip())
            else:
                text = fields['text'].value.strip()
                
            text = fields['quote'].value + text
                
            #original_text = post['text'].value.strip()
            date = datetime.datetime.now()
            user = account.get(environ)
            
            if 'file' in fields:
                if fields['file'].filename != '':
                    flag = True
                    file_name = fields['file'].filename
                    file_type = fields['file'].type
                    file_size = int(fields['file_size'].value)
                    file_bin = fields['file'].value
                    
            col = environ['DB']['comments']
            
            if flag == False:
                comment = {
                    'text': text,
                    'file_name': None,
                    'file_size': None,
                    'file_type': None,
                    'file_bin': None,
                    'date': date,
                    'message_id': ObjectId(message_id),
                    'user_id': user['_id']
                }
                
                comment_id = str(col.insert_one(comment).inserted_id)

                #environ.get('cursor').execute('INSERT INTO comments (text, date, message_id, user_id) VALUES (%s, %s, %s, %s) RETURNING id',
                    #(text, date, message_id, user.id))
            else:
                comment = {
                    'text': text,
                    'file_name': file_name,
                    'file_size': file_size,
                    'file_type': file_type,
                    'file_bin': file_bin,
                    'date': date,
                    'message_id': ObjectId(message_id),
                    'user_id': user['_id']
                }
                
                comment_id = str(col.insert_one(comment).inserted_id)
                #environ.get('cursor').execute('INSERT INTO comments (text, file_name, file_size, file_type, file_bin, date, message_id, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
                    #(text, file_name, file_size, file_type, file_bin, date, message_id, user.id))
                            
            #comment_id = environ.get('cursor').fetchone().id
                            
            #environ.get('conn').commit()
                
            async_to_sync(notifications.send)(environ, user, date.strftime('%H:%M (%d.%m.%Y)') + '\n комментарий от ' + user['name'], '/message/' + str(message_id)+ '?id=' + str(comment_id) + '#' + str(comment_id),)
            
            response_headers = [
                ('Location', '/message/' + message_id + '#' + str(comment_id)),
            ]
        else:
            response_headers = [
                ('Location', '/message/' + message_id),
            ]
        
        status = '303 See Other'
        content = b''
    
    return status, response_headers, content
    
def get(environ):
    
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
        #environ.get('cursor').execute('SELECT COUNT(id) FROM  comments')
        #comments_number = environ.get('cursor').fetchone().count
        
        col = environ['DB']['comments']
        x = col.find({}, {'_id'})
        comments_number = 0
        
        for data in x:
            comments_number += 1
        
        limit = 10
        
        pages = math.ceil(comments_number/limit)
        
        arr = environ.get('PATH_INFO').split('/')
        page = int(arr[2])
        offset = limit * (page - 1)
        
        #environ.get('cursor').execute('SELECT id, name FROM users')
        #users = environ.get('cursor').fetchall()
        
        col = environ['DB']['users']
        _users = col.find({}, {'_id', 'name'})
        
        users = []
        
        class User:
            pass
            
        for data in _users:
            _user = User()
            _user.id = data['_id']
            _user.name = data['name']
            users.append(_user)

        #environ.get('cursor').execute('SELECT id, text, file_name, file_size, file_type, date, message_id, user_id FROM comments ORDER BY id DESC LIMIT %s OFFSET %s', (limit, offset,))
        #comments = environ.get('cursor').fetchall()
        
        col = environ['DB']['comments']
        _comments = col.find({}, {'_id', 'text', 'file_name', 'file_size', 'file_type', 'date', 'message_id', 'user_id'}).skip(offset).limit(limit).sort('_id', -1)
        
        comments = []
        
        for data in _comments:
            data['id'] = data['_id']
            comments.append(type('Class', (), data))

        image, audio, video = default.get_mime_type_list()
        
        status = '200 OK'
        content = render('mir', 'comments.html', users=users, comments=comments, pages=pages, page=page, image=image, audio=audio, video=video)
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
    
