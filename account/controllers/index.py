

import requests
#from common.modules.template import render
from . import account
#from mir.controllers import visitor


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

        url = 'http://mirumir.infinityfreeapp.com/sign-in'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
        cookies = dict(__test='52b50e0de65515a3125cefdeaa677792', login=user['login'], password=user['password'])
        
        res = requests.get(url, timeout=30, headers=headers, cookies=cookies, allow_redirects=True)

        if res.encoding == 'ISO-8859-1':
            res.encoding = 'utf-8'
            
        content = (res.text).encode()
        status = '200 OK'
        #content = render('mir', 'index.html', user=user, mail_messages_number=mail_messages_number, other_users=other_users)
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(content)))
        ]
    
    return status, response_headers, content
    
    
    
    
