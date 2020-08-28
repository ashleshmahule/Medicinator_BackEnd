import os
import sys
from flask import Flask
from flask import request
from flask import jsonify
import predict
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
answer = {}
baseIntent = 'welcome'
intent = ''



@app.route('/')
def home():
    return "Welcome"


@app.route('/getResponse')
def getResponse():
    obj = request.args.get('object')
    obj = json.loads(obj)
    intent=obj['intent']
    text = obj['query']
    print(text)
    answer['response'], answer['intent'] = predict.chatbot_response(text)

    return jsonify(answer)


@app.route('/getAlternate')
def getAlternate():
    obj = request.args.get('object')
    obj = json.loads(obj)
    intent=obj['intent']

    tosend={}

    if intent == 'medicine.alternate':
        query = obj['query']

        alternates = predict.findAlternate(query)
        seperator = '\n'
        altStr = seperator.join(alternates)

        tosend['response'] = altStr
        tosend['intent'] = baseIntent

        return jsonify(tosend)

    else:
        tosend['response'] = "Sorry, couldn't understand"
        tosend['intent'] = baseIntent

        return jsonify(tosend)

@app.route('/getDiagnosis')
def getDiagnosis():

    return()


if (__name__ == "__main__"):
    app.run()
