from flask import Flask, request, render_template
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])

def index():
    return render_template('index.html')

def home():
    if( request.method == "POST"):
        model = load_model('/models/MobileNetV2_3.h5')
        #user_input = request.form.get('size')
        #prediction  = model.predict([[user_input ,19.5,306.5947,9,24.98034,121.53951]])
        print('model loaded')
    return render_template('index.html')#, prediction = prediction)   

def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return "File saved successfully"

if __name__ == '__main__':
    app.run(debug = True)