
from common.modules.template import render
from account.controllers import account
from . import visitor


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
        content = render('mir', 'links.html')
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(content)))
        ]
    
    return status, response_headers, content
