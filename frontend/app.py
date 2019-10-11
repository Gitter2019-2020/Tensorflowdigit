import requests
import numpy as np
import json
import time
from flask import Flask, request, jsonify, render_template

import  tensorflow as tf
import os

app = Flask(__name__)
BACKEND_IP = os.getenv("BACKEND_IP", default="10.0.60.74")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.htm', PREDICT_URL=request.host_url+"predict")

@app.route('/add', methods=['GET'])
def add():
    return render_template('add.htm', ADD_URL=request.host_url+"add_training_digit")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = json.loads(request.data)['data']
        reshaped = tf.reshape(data, [280, 280, 1])
        resized = tf.image.resize(reshaped, size=[28,28], method='gaussian')
        normalized = resized/255

        payload = { "instances":  normalized.numpy().tolist()}
        api = "http://"+BACKEND_IP+":8501/v1/models/digits:predict"

        reply = requests.post(url = api, json = payload) 
  
        predictions = json.loads(reply.content).get('predictions')
        prediction = np.argmax(predictions)
        return jsonify(int(prediction))
    except Exception as e:
        return 'prediction NOK : ' + str(e)

@app.route('/add_training_digit', methods=['POST'])
def add_training_digit():
    try:
        data = json.loads(request.data)['data']
        label = json.loads(request.data)['label']
        reshaped = tf.reshape(data, [280, 280, 1])
        resized = tf.image.resize(reshaped, size=[28,28], method='gaussian')

        casted = tf.dtypes.cast(resized, dtype=tf.uint8)
        encoded = tf.image.encode_png(casted)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        tf.io.write_file("../backend/images/training/"+label+"/"+timestr+".png", encoded)
        
        return jsonify(True)
    except Exception as e:
        return 'prediction NOK : ' + str(e)