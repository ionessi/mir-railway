
import asyncio
import re

import requests


def get_mime_type_list():
    image = ['image/gif', 'image/jpeg', 'image/png', 'image/webp', 'image/x-icon']
    audio = ['audio/mpeg', 'audio/webm', 'audio/mp4', 'audio/ogg']
    video = ['video/mp4', 'video/webm', 'video/ogg']

    return image, audio, video

'''
def get_link(message):
    if re.findall(r'https://\S+|http://\S+', message):
        urls = re.findall(r'https://\S+|http://\S+', message)
        
        for url in urls:
            message = message.replace(url, 'FYFYR')

        for url in urls:
            message = message.replace(
                'FYFYR',
                '<a class="cropped-link" href="' + url + '" target="_blank">' + url + '</a>',
                1
            )
    
    return message
'''

async def get_link(message):
    if re.findall(r'https://\S+|http://\S+', message):
        urls = re.findall(r'https://\S+|http://\S+', message)

        tasks = []
        titles = []
        
        for url in urls:
            tasks.append(asyncio.create_task(get_title(url)))
            
        for task in tasks:
            titles.append(await task)
        
        i = 0
        
        for title in titles:
            message = message.replace(
                urls[i], 'FYFYR'
            )
            
            i += 1
            
        i = 0
        
        for title in titles:
            if title == '':
                message = message.replace(
                    'FYFYR',
                    '<a class="cropped-link" href="' + urls[i] + '" target="_blank">' + urls[i] + '</a>',
                    1
                )
                
            else:
                message = message.replace(
                    'FYFYR',
                    '<small>' + title + '\n' + '</small><a class="cropped-link" href="' + urls[i] + '" target="_blank">' + urls[i] + '</a>',
                    1
                )
            
            i += 1
    
    return message
    
async def get_title(url):
    #headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 11; Infinix X688B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36'}
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
    
    try:
        res = requests.get(url, timeout=7, headers=headers, allow_redirects=True)
        
        if res.encoding == 'ISO-8859-1':
            res.encoding = 'utf-8'
            
        text = (res.text).replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', ' ')

    except:
        text = ''
    
    pattern = r'<title.*?>(.+?)</title>'
    
    try:
        title = re.findall(pattern, text)[0].strip()

    except:
        title = ''
    
    return title
    
    
