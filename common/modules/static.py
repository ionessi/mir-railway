
import requests

def get(environ):
    #print(environ['RAW_URI'])
    url = 'http://mirumir.infinityfreeapp.com' + environ['RAW_URI']
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
    cookies = dict(__test='52b50e0de65515a3125cefdeaa677792')
    res = requests.get(url, timeout=30, headers=headers, cookies=cookies, allow_redirects=False)
    #print(res.headers['Cache-Control'])
    content = res.content
    
    status = '200 OK'

    response_headers = [
        ('Cache-Control', 'public, max-age=31536000'),
        ('Accept-Ranges', 'bytes'),
        ('Content-Type', res.headers['Content-Type']),
        ('Content-Length', str(len(content)))
    ]

    return status, response_headers, content
    
