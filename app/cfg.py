import os
bind = "0.0.0.0:80"
workers = 2
threads = 2
daemon = True
accesslog = '/tmp/gunicorn.access.log'
errorlog = '/tmp/gunicorn.error.log'
reload = True
#enable_stdio_inheritance = True
#loglevel = 'debug'
