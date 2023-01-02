
import os

from .controllers import index
from .controllers import account
#from mail.controllers.index import get_the_number_of_unread_messages


def get(environ):
    content = b'empty'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/html'),
        #('Content-Length', str(len(data)))
    ]
    
    #if account.get(environ):
        #os.environ['incoming_unread_messages_number'] = str(get_the_number_of_unread_messages(environ))
    
    if environ['PATH_INFO'] == '/':
        status, response_headers, content = index.get(environ)
        
    elif environ.get('PATH_INFO') == '/sign-in':
        status, response_headers, content = account.sign_in(environ)
        
    elif environ.get('PATH_INFO') == '/sign-up':
        status, response_headers, content = account.sign_up(environ)

        
    return status, response_headers, content
    
