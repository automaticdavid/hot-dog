import os
import socket
import boto3
from flask import Flask, render_template, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from lib import NotSanta

dir_results = os.getcwd() + '/static/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads/'
app.config['RESULTS'] = dir_results
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['MODEL'] = "model/model.model"

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET_NAME)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

curr_host = socket.gethostname() 
curr_ip = socket.gethostbyname(socket.gethostname())

class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, u'Image only!'), FileRequired(u'File was empty!')])
    submit = SubmitField(u'Upload')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        result = NotSanta().classify(app.config['MODEL'], 'uploads/' + filename)
        result_name = os.path.basename(result.name)
    else:
        result_name = None
        s3_result = None

    if result_name:

        s3 = boto3.client(
            "s3",
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )

        try:
            s3.upload_fileobj(
                result,
                S3_BUCKET_NAME,
                result_name,
                ExtraArgs={
                   "ACL": "public-read",
                   # "ContentType": f.content_type
                }
            )
            s3_result = "{}{}".format(S3_LOCATION, result_name)

        except Exception as e:
            print("S3 ERROR: ", e)
            raise

    return render_template('index.html', form=form, file=s3_result, host=curr_host, ip=curr_ip)


if __name__ == '__main__':
     # app.debug = True
    app.run()
