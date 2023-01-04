
import re

import account.urls
import mir.urls
#import mail.urls
#import notifications.urls
#import rss.urls
#import corner.urls
#import vpn.urls
from .modules import static
from .modules import uploads
#from database import db
#from mir.controllers import error
#from mir.controllers import visitor


def routing(environ):
    status = '200 OK'
    content = b'empty'
    response_headers = [
        ('Content-type', 'text/html'),
        ('Content-Length', str(len(content)))
    ]

    #environ['PATH_REAL'] = environ['PATH_INFO']
    
    if content == b'empty':
        status, response_headers, content = account.urls.get(environ)
    
    if content == b'empty':
        status, response_headers, content = mir.urls.get(environ)
    
    '''
    if content == b'empty':
        status, response_headers, content = mail.urls.get(environ)
    
    if content == b'empty':
        status, response_headers, content = notifications.urls.get(environ)

    if content == b'empty':
        status, response_headers, content = rss.urls.get(environ)
        
    if content == b'empty':
        status, response_headers, content = corner.urls.get(environ)

    if content == b'empty':
        status, response_headers, content = vpn.urls.get(environ)
    '''
 
    if content == b'empty':
    
        if re.findall(r'^/static/\S+$', environ.get('PATH_INFO')):
            status, response_headers, content = static.get(environ)
            
        elif re.findall(r'^/uploads/\S+/.+$', environ.get('PATH_INFO')):
            status, response_headers, content = uploads.get(environ)
                
        elif environ['PATH_INFO'] == '/favicon.ico':
            #environ['PATH_INFO'] = '/static/mir/images/favicon.ico'
            status, response_headers, content = static.get(environ)
            
        elif environ['PATH_INFO'] == '/robots.txt':
            #visitor.add(environ, '')
            #environ['PATH_INFO'] = '/static/common/robots.txt'
            status, response_headers, content = static.get(environ)
            
        #elif environ['PATH_INFO'] == '/aes.js':
            #status, response_headers, content = static.get(environ)
    '''
    if content == b'empty':
        #environ['PATH_INFO'] = '/error'
        status, response_headers, content = error.get_404(environ)
    else:
        if not re.findall(r'^/static/\S+$', environ.get('PATH_INFO')):
            visitor.add(environ, '')
    '''
    
    return status, response_headers, content
    
