from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras import backend as K
import numpy as np
import imutils
import cv2
import tempfile
import boto3
import os
from azure.storage.blob import BlockBlobService, PublicAccess
from google.cloud import storage


class NotSanta:

    def classify(self, model_name, image_path):
        
        # load the trained convolutional neural network
        model = load_model(model_name)

        # load the image
        image = cv2.imread(image_path)
        orig = image.copy()

        # pre-process the image for classification
        image = cv2.resize(image, (100, 100))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)

        # classify the input image
        (not_car, car) = model.predict(image)[0]

        # build the label

        if car > not_car:
            label = "It's a CAR"
            proba = car
        else: 
            label = "Not a car."
            proba = not_car

        label = "{}: {:.2f}%".format(label, proba * 100)

        # draw the label on the image
        output = imutils.resize(orig, width=400)

        cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
	    1, (0, 255, 0), 3)

        f = tempfile.NamedTemporaryFile(mode='w+b', delete=False, dir='static', suffix='.jpg')
        cv2.imwrite( f.name, output)

        del model
        K.clear_session()
        
        return(f.name)


class ObjectStore:

    def __init__(self, OBJECT_STORE, filepath):
        self.store = OBJECT_STORE
        self.filepath = filepath

    def upload(self): 

        filepath = self.filepath
        store = self.store

        if store  == 's3':
            result = self.s3_upload(filepath)
        elif store == 'blob':
            result = self.blob_upload(filepath)           
        elif store == 'local':
            filename = os.path.basename(filepath)
            return(filename)
        else: 
            raise

        return(result)

    def s3_upload(self, filepath):

        S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
        S3_KEY = os.environ.get("S3_KEY")
        S3_SECRET = os.environ.get("S3_SECRET")
        S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET_NAME)

        s3 = boto3.client(
            "s3",
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )

        filename = os.path.basename(filepath)

        try:
            s3.upload_file(
                filepath,
                S3_BUCKET_NAME,
                filename,
                ExtraArgs={
                   "ACL": "public-read"
                }
            )
            s3_result = "{}{}".format(S3_LOCATION, filename)
            return(s3_result)

        except Exception as e:
            print("S3 ERROR: ", e)
            raise


    def blob_upload(self, filepath):

        BLOB_CONTAINER = os.environ.get("BLOB_CONTAINER")
        BLOB_KEY = os.environ.get("BLOB_KEY")
        BLOB_ACCOUNT = os.environ.get("BLOB_ACCOUNT")

        filename = os.path.basename(filepath)

        try:

            block_blob_service = BlockBlobService(
                        account_name=BLOB_ACCOUNT, 
                        account_key=BLOB_KEY)

            block_blob_service.create_blob_from_path(
                BLOB_CONTAINER,
                filename,
                filepath)

            blob_result = "https://{}.blob.core.windows.net/results/{}".format(BLOB_ACCOUNT, filename)

        except Exception as e:
            print("BLOB ERROR: ", e)
        
        return(blob_result)
        

    def goog_upload(sefl, filepath):

        bucket_name = os.environ.get("GOOG_BUCKET_NAME")
        destination_blob_name = os.path.basename(filepath)
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(filepath)











