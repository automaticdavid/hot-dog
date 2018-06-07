bind = "127.0.0.1:80"
workers = 5
threads = 5
preload = True
daemon = True
accesslog = '/tmp/gunicorn.access.log'
errorlog = '/tmp/gunicorn.error.log'


