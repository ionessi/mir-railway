
import os
import re

#from .controllers import topic
from .controllers import message
from .controllers import comment
from .controllers import visitor
#from .controllers import geolocation
from .controllers import links
#from mail.controllers.index import get_the_number_of_unread_messages
#from account.controllers import account


def get(environ):
    status = '200 OK'
    content = b'empty'
    response_headers = [
        ('Content-type', 'text/html'),
        ('Content-Length', str(len(content)))
    ]
    
    #if account.get(environ):
        #os.environ['incoming_unread_messages_number'] = str(get_the_number_of_unread_messages(environ))
        
    if re.findall(r'^/messages/\d+$', environ.get('RAW_URI')):
        status, response_headers, content = message.get_all(environ)
        
    elif re.findall(r'^/messages/\d+\?\S*$', environ.get('RAW_URI')):
        status, response_headers, content = message.get_filtered_all(environ)
        
    elif environ.get('PATH_INFO') == '/message/add':
        status, response_headers, content = message.add(environ)
        
    elif re.findall(r'^/message/\w+$', environ.get('PATH_INFO')):
        status, response_headers, content = message.get(environ)
        
    elif re.findall(r'^/message/file/\w+$', environ.get('PATH_INFO')):
        status, response_headers, content = message.get_file(environ)
        
    elif re.findall(r'^/message/remove/\w+$', environ.get('PATH_INFO')):
        status, response_headers, content = message.remove(environ)
        
    elif environ.get('PATH_INFO') == '/comment/add':
        status, response_headers, content = comment.add(environ)
        
    elif re.findall(r'^/comments/\d+$', environ.get('PATH_INFO')):
        status, response_headers, content = comment.get(environ)
        
    elif re.findall(r'^/comment/file/\w+$', environ.get('PATH_INFO')):
        status, response_headers, content = comment.get_file(environ)
        
    elif re.findall(r'^/comment/remove/\w+/\w+$', environ.get('PATH_INFO')):
        status, response_headers, content = comment.remove(environ)
        
    elif re.findall(r'^/visitors/\d+$', environ.get('PATH_INFO')):
        status, response_headers, content = visitor.get(environ)
        
    elif environ.get('PATH_INFO') == '/geolocation':
        status, response_headers, content = geolocation.index(environ)
        
    elif environ.get('PATH_INFO') == '/geolocation/add':
        status, response_headers, content = geolocation.add(environ)
        
    elif environ.get('PATH_INFO') == '/geolocation/get':
        status, response_headers, content = geolocation.get(environ)
        
    elif re.findall(r'^/geolocation/file/\w+$', environ.get('PATH_INFO')):
        status, response_headers, content = geolocation.get_file(environ)
        
    elif environ['PATH_INFO'] == '/links':
        status, response_headers, content = links.index(environ)
        
        
    return status, response_headers, content
    
