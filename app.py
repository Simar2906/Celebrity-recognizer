import os
from flask import Flask, flash, render_template, redirect, request, url_for

from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image
import cv2
from imageio import imread
from glob import glob
import numpy as np
import youtube_dl
import pafy
import vlc
import time


app = Flask(__name__)

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
        url = request.form.get('url')
        start = request.form.get('start')
        stop = request.form.get('stop')
        directory = 'tmp/uploaded'
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        instance = vlc.Instance()
        player=instance.media_player_new() 
        media=instance.media_new(playurl) 
        start_str = 'start-time=' + str(start)
        stop_str = 'stop-time=' + str(stop)
        media.add_option(start_str)
        media.add_option(stop_str) 
        media.get_mrl() 
        player.set_media(media) 
        player.play() 
        time.sleep(5)
        #player.pause()
        player.video_take_snapshot(0, directory, i_width=player.video_get_width(), i_height=player.video_get_height())
        print('screenshot taken')

        for filename in os.listdir(directory):
            image = cv2.imread(os.path.join(directory,filename))
            break
        
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
        player.stop()
        for file in os.scandir(directory):
            os.remove(file.path)
        
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