
import datetime
import math

import requests

from common.modules.template import render
from account.controllers import account


def add(environ, text):
    if 'RAW_URI' in environ:
        path = '<a href="' + environ.get('RAW_URI') + '">' + environ.get('RAW_URI') + '</a> <span class="w3-text-red">' + text + '</span>'
    else:
        path = '<a href="' + environ.get('REQUEST_URI') + '">' + environ.get('REQUEST_URI') + '</a> <span class="w3-text-red">' + text + '</span>'
    
    if not account.get(environ):
        path += ' <span class="w3-text-red">FALSE</span>'

    if 'HTTP_TRUE_CLIENT_IP' in environ:
        ip = environ['HTTP_TRUE_CLIENT_IP']
    else:
        ip = '172.0.0.1'
        
    user_agent = environ.get('HTTP_USER_AGENT')
    
    #environ.get('cursor').execute('SELECT * FROM visitors')
    #visitors = environ.get('cursor').fetchall()
    
    col = environ['DB']['visitors']
    _visitors = col.find()
    
    visitors = []
    
    for data in _visitors:
        visitors.append(type('Class', (), data))

    flag = False
    
    date = datetime.datetime.now()

    if visitors:
        for visitor in visitors:
            if ip == visitor.ip and path == visitor.path:
                                
                #environ.get('cursor').execute('UPDATE visitors SET path=%s, date=%s, user_agent=%s WHERE id=%s',
                                #(path, date, user_agent, visitor.id))
                                
                query = {
                    '_id': visitor._id
                }
                                
                newvalues = {
                    '$set': {
                        'method': environ['REQUEST_METHOD'],
                        'path': path,
                        'user_agent': user_agent,
                        'date': date
                    }
                }
                
                col.update_one(query, newvalues)
                
                flag = True
                
                break
                
    if flag == False:
        #environ.get('cursor').execute('INSERT INTO visitors (ip, path, user_agent, date) VALUES (%s, %s, %s, %s)',
                        #(ip, path, user_agent, date))
        visitor = {
            'method': environ['REQUEST_METHOD'],
            'path': path,
            'ip': ip,
            'user_agent': user_agent,
            'date': date
        }
        
        col.insert_one(visitor)
            
    #environ.get('conn').commit()
        
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
        
        arr = environ.get('PATH_INFO').split('/')
        page = arr[2]
        
        user = account.get(environ)

        url = 'http://mirumir.infinityfreeapp.com/visitors/' + page
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
        cookies = dict(__test='52b50e0de65515a3125cefdeaa677792', login=user['login'], password=user['password'])
        
        res = requests.get(url, timeout=30, headers=headers, cookies=cookies, allow_redirects=True)

        if res.encoding == 'ISO-8859-1':
            res.encoding = 'utf-8'
            
        content = (res.text).encode()
        
        status = '200 OK'
        #content = render('mir', 'visitors.html', visitors=visitors, pages=pages, page=page)
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(content)))
        ]
    
    return status, response_headers, content

