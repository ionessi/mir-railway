
import datetime
from urllib.parse import parse_qs

import requests

from common.modules.template import render
from common.modules.body import read


def sign_in(environ):

    if environ['REQUEST_METHOD'] == 'POST':
    
        fields = read(environ)
        
        login = fields['login'].value.strip()
        password = fields['password'].value.strip()
        
        url = 'http://mirumir.infinityfreeapp.com/sign-in'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
        cookies = dict(__test='52b50e0de65515a3125cefdeaa677792', login=login, password=password)
        
        res = requests.get(url, timeout=30, headers=headers, cookies=cookies, allow_redirects=False)

        if res.encoding == 'ISO-8859-1':
            res.encoding = 'utf-8'
        
        location = res.headers['Location']

        if location == '/':
            status = '303 See Other'
            response_headers = [
                ('Location', '/'),
                ('Set-Cookie', 'login=' + login + '; path=/; max-age=31536000'),
                ('Set-Cookie', 'password=' + password + '; path=/; max-age=31536000')
            ]
        
        else:
            status = '303 See Other'
            response_headers = [
                ('Location', '/sign-in'),
                ('Set-Cookie', 'login=''; path=/; max-age=0'),
                ('Set-Cookie', 'password=''; path=/; max-age=0')
            ]
            
        content = b''
        
    else:

        status = '200 OK'
        content = render('account', 'sign_in.html')
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(content)))
        ]
    
    return status, response_headers, content
    
def sign_up(environ):
    
    if environ.get('REQUEST_METHOD') == 'POST':
    
        fields = read(environ)
        
        login = fields['login'].value.strip()
        password = fields['password'].value.strip()
        
        #environ.get('cursor').execute('SELECT * FROM users WHERE login=%s', (login,))
        #user = environ.get('cursor').fetchone()
        
        col = environ['DB']['users']
        user = col.find_one({'login': login[0]})
        
        if not user:
            name = fields['name'].value.strip()
            date = datetime.datetime.now()
            
            #environ.get('cursor').execute('INSERT INTO users (login, password, name, date) VALUES (%s, %s, %s, %s)',
                #(login, password, name, date))
            #environ.get('conn').commit()
            
            user = {
                'login': login,
                'password': password,
                'name': name,
                'date': date
            }
            
            col.insert_one(user)
            
            status = '303 See Other'
            response_headers = [
                ('Location', '/'),
                ('Set-Cookie', 'login='+login+'; path=/; max-age=31536000'),
                ('Set-Cookie', 'password='+password+'; path=/; max-age=31536000')
            ]
        
        else:
            status = '303 See Other'
            response_headers = [
                ('Location', '/sign-up'),
                ('Set-Cookie', 'login=''; path=/; max-age=0'),
                ('Set-Cookie', 'password=''; path=/; max-age=0')
            ]
                    
        content = b''
        
    else:
        status = '200 OK'
        content = render('account', 'sign_up.html')
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(content)))
        ]
    
    return status, response_headers, content

def get(environ):

    if 'HTTP_COOKIE' in environ:
        cookies = parse_qs(environ['HTTP_COOKIE'], separator='; ')
        login = cookies.get('login')
        password = cookies.get('password')

        if login and password:

            user = {'login': login[0], 'password': password[0]}
                    
            if user:
                return user
                
            else:
                return False
                
        else:
            return False
    
    else:
        return False

