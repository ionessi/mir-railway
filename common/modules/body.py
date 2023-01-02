
import cgi

def read(environ):
    fields = cgi.FieldStorage(
        fp = environ['wsgi.input'],
        environ = environ,
    )
    
    return fields

