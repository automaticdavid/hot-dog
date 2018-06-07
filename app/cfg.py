bind = "127.0.0.1:80"
workers = 5
threads = 5
max-requests = 5
preload = true
daemon = true
access-logfile = /tmp/gunicorn.access.log
capture-output = true
error-logfile = /tmp/gunicorn.error.log


