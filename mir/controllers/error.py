
from common.modules.template import render
from . import visitor


def get_404(environ):

    #environ['PATH_INFO'] = environ['PATH_REAL']
    
    visitor.add(environ, '404 NOT FOUND')
    
    status = '404 NOT FOUND'
    content = render('mir', '404.html')
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(content)))
    ]

    return status, response_headers, content

