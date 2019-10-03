import requests
import numpy as np
import json
from flask import Flask, request, jsonify, render_template

import  tensorflow as tf
import base64
import os
import re

app = Flask(__name__)
BACKEND_IP = os.getenv("BACKEND_IP", default="10.0.60.74")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.htm', PREDICT_URL=request.host_url+"predict")

@app.route('/predict', methods=['POST'])
def predict():
    """Predict genres based on synopsis."""
    try:
        # contents = base64.decodebytes(request.data)
        # tensor = tf.io.decode_png(contents=contents, channels=1)/255

        data = json.loads(request.data)['data']
        reshaped = tf.reshape(data, [280, 280, 1])
        resized = tf.image.resize(reshaped, size=[28,28], method='gaussian')
        normalized = resized/255

        # casted = tf.dtypes.cast(resized, dtype=tf.uint8)
        # encoded = tf.io.encode_jpeg(casted)
        # tf.io.write_file("C:\\Users\\sdf\\Desktop\\ML\\code\\tensorflow\\resized.jpeg", encoded)
        
        payload = { "instances":  normalized.numpy().tolist()}#[tensor.numpy().tolist()]
        api = "http://"+BACKEND_IP+":8501/v1/models/digits:predict"

        reply = requests.post(url = api, json = payload) 
  
        predictions = json.loads(reply.content).get('predictions')
        prediction = np.argmax(predictions)
        return jsonify(int(prediction))
    except Exception as e:
        return 'prediction NOK : ' + str(e)