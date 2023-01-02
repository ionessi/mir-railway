
import os.path
import mimetypes
from urllib.parse import parse_qs

def get(path_info):

    path_info = path_info[1:]
    
    if os.path.exists(path_info):
        f = open(path_info, 'rb')
        data = f.read()
        f.close()

        mime_type = mimetypes.guess_type(path_info)[0]
        
        status = '200 OK'
        response_headers = [
            ('Cache-Control', 'public, max-age=31536000'),
            #('Cache-Control', 'public, max-age=0'),
            ('Accept-Ranges', 'bytes'),
            ('Content-type', mime_type),
            ('Content-Length', str(len(data)))
        ]
    else:
        data = b'empty'
        status = '404 NOT FOUND'
        response_headers = [
            #('Cache-Control', 'public, max-age=31536000'),
            #('Cache-Control', 'public, max-age=0'),
            #('Accept-Ranges', 'bytes'),
            #('Content-type', mime_type),
            ('Content-Length', str(len(data)))
        ]

    return status, response_headers, data
    
