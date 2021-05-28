import os
from flask import Flask, flash, render_template, redirect, request, url_for

from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image
import cv2
from imageio import imread
from glob import glob
import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = "supertopsecretprivatekey"

def image_name():
    class_names = glob("105_classes_pins_dataset/*/") # Reads all the folders in which images are present
    class_names = sorted(class_names) # Sorting them
    name_id_map = dict(zip(range(len(class_names)),class_names))
    #print(name_id_map)
    return name_id_map
    
name_id = image_name()


@app.route('/', methods=['GET', 'POST'])
def home():
    model = load_model('models\MobileNetV2_3.h5')
    model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    if request.method == 'GET':
        # show the upload form
        prediction = 0
        return render_template('index.html')

    if request.method == 'POST':
        image_file = request.files['image']
        filename = image_file.filename
        filepath = os.path.join('tmp/uploaded/', filename)
        image_file.save(filepath)
        image = imread(filepath)
        image = face_extractor(image)
        image = image / 255
        #print(image.shape)
        image = cv2.resize(image, (160, 160)) 
        #print(image.shape)
        #prediction = 0
        prediction = model.predict(image.reshape(-1, 160, 160, 3))
        #i,j = np.unravel_index(prediction.argmax(), prediction.shape)
        flag = 0
        non_celeb = 0
        for k in range(0, 105):
            if(prediction[0][k] > 0.90):
                i, j = 0, k
                flag = 1
                break
            elif(prediction[0][k] > 0.5):
                non_celeb = 1
        if(flag == 0):
                if(non_celeb == 1):
                    return render_template('index.html', prediction = 'Non Celebrity Face Detected')
                return render_template('index.html', prediction = 'No Face Found')
        prediction[i,j]
        print(j)
        predicted_class = get_name(j)[30:-1]
        print(prediction)
        return render_template('index.html', prediction = predicted_class)

def face_extractor(img):
    # Function detects faces and returns the cropped face
    # If no face detected, it returns the input image
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    
    if faces is ():
        return img
    
    # Crop all faces found
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face


def get_name(j):
    return name_id[j]
if __name__ == '__main__':
    app.run(debug=True)