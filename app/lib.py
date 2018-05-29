from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras import backend as K
import numpy as np
import imutils
import cv2
import tempfile

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
        (unkown, car, cat) = model.predict(image)[0]

        # build the label

        if car > unkown and car > cat:
            label = "CAR"
            proba =car 
        elif cat > unkown and cat > car:
            label = "CAT"
            proba = cat
        else: 
            label = "What?"
            proba = unkown

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



