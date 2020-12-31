from flask import Flask, jsonify, request
from flask_cors import CORS
from keras.models import load_model
from data_pipeline import get_inputs, get_pred

app = Flask(__name__)
CORS(app)

# load models
beto_model = load_model('models/BETO_RNN')
bert_model = load_model('models/BERT_CNN')
print('models successfully loaded')

@app.route("/")
def index():
    return 'Flask Backend'

@app.route("/predict/spanish", methods = ["POST"])
def predict_spanish():
    data = request.json
    text = data.get('text')
    input_ids, input_masks, input_segments = get_inputs(text, 'beto')
    label, value = get_pred(input_ids, input_masks, input_segments, beto_model)
    result = {
        'fake': str(label),
        'value': str(value)
    }
    return jsonify(result)

@app.route("/predict/english", methods = ["POST"])
def predict_english():
    data = request.json
    text = data.get('text')
    input_ids, input_masks, input_segments = get_inputs(text, 'bert')
    label, value = get_pred(input_ids, input_masks, input_segments, bert_model)
    result = {
        'fake': str(label),
        'value': str(value)
    }
    return jsonify(result)
