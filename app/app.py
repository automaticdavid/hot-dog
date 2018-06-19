import os
import socket
from flask import Flask, render_template, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from lib import NotSanta
from lib import ObjectStore

dir_results = os.getcwd() + '/static/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads/'
app.config['RESULTS'] = dir_results
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

MODEL = "model/model.model"
OBJECT_STORE = os.environ.get("OBJECT_STORE")


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
        upload_filename = photos.save(form.photo.data)
        result_filename = NotSanta().classify(MODEL, 'uploads/' + upload_filename)
    else:
        result_filename = None
        result = None

    if result_filename:
        result = ObjectStore(OBJECT_STORE, result_filename).upload()

    if OBJECT_STORE != 'local':
    	return render_template('index.html', form=form, file=result, host=curr_host, ip=curr_ip)
    else: 
    	return render_template('index.local.html', form=form, file=result, host=curr_host, ip=curr_ip)


if __name__ == '__main__':
    # app.debug = True
    app.run()
