import requests
import numpy as np
import json
from flask import Flask, request, jsonify, render_template

import  tensorflow as tf
import base64
import os
import re

app = Flask(__name__)
BACKEND_IP = os.environ.get("BACKEND_IP")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.htm', PREDICT_URL=request.host_url+"predict")

@app.route('/predict', methods=['POST'])
def predict():
    """Predict genres based on synopsis."""
    try:
        contents = base64.decodebytes(request.data)
        tensor = tf.io.decode_png(contents=contents, channels=1)/255

        api = "http://"+BACKEND_IP+":8501/v1/models/digits:predict"
        payload = { "instances": [tensor.numpy().tolist()] }

        reply = requests.post(url = api, json = payload) 
  
        predictions = json.loads(reply.content).get('predictions')
        prediction = np.argmax(predictions)
        return jsonify(int(prediction))
    except Exception as e:
        return 'prediction NOK : ' + str(e)