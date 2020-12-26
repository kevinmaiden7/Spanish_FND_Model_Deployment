from flask import Flask, jsonify, request
from keras.models import load_model

app = Flask(__name__)

# Load models
beto_model = load_model('assets/BETO/BETO_RNN.tf')

@app.route("/")
def index():
    return 'Flask Backend'

@app.route("/predict", methods = ["POST"])
def predict():
    data = request.json
    print(data)

    # return a response in json format 
    #return jsonify(data)
    return 'predict function'
