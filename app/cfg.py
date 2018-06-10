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

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
S3_LOCATION = 'http://{}.s3.amazonoaws.com/'.format(S3_BUCKET_NAME)


raw_env =  [ 
    'S3_BUCKET_NAME =' + S3_BUCKET_NAME, 
    'S3_KEY = ' + S3_KEY,
    'S3_SECRET = ' + S3_SECRET,
    'S3_LOCATION = ' + S3_LOCATION
    ]


