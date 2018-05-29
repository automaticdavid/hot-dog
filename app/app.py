import os
import socket
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
        result = NotSanta().classify("model/cats_and_cars.model", 'uploads/' + filename)
        result_name = os.path.basename(result)
    else:
        result_name = None
    print(">>>", result_name)

    return render_template('index.html', form=form, file=result_name, host=curr_host, ip=curr_ip)


if __name__ == '__main__':
    app.debug = True
    app.run()
