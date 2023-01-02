
import os
import sys
import time
import datetime
#import resource


from common.router import routing

#soft, hard = resource.getrlimit(resource.RLIMIT_AS)
#resource.setrlimit(resource.RLIMIT_AS, (1024*1024*512, hard))


def app(environ, start_response):

    os.environ['TZ'] = 'Asia/Krasnoyarsk'
    time.tzset()

    status, response_headers, content = routing(environ)

    start_response(status, response_headers)
    
    yield content
    
    #return iter([content])

