
import os

from jinja2 import Environment, FileSystemLoader


def mail():
    #incoming_unread_messages_number = os.environ['incoming_unread_messages_number']
    
    if (int(os.environ['incoming_unread_messages_number']) >= 1):
        return os.environ['incoming_unread_messages_number']
    else:
        return ''

def render(path_temp, path, **kwargs):

    env = Environment(loader=FileSystemLoader('./templates/' + path_temp))
    
    env.globals['mail'] = mail
    
    template = env.get_template(path)
    html = template.render(kwargs).encode('utf-8')
    
    return html
