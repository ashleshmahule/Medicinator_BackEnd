import os
import sys
from flask import Flask
from flask import request
from flask import jsonify
import predict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Welcome"


@app.route('/getResponse')
def getResponse():
    text = request.args.get('text')
    print(text)
    answer = {}
    answer['response'], answer['intent'] = predict.chatbot_response(text)

    return jsonify(answer)


@app.route('/getAlternate')
def getAlternate():
    query = request.args.get('query')
    alternates = predict.findAlternate(query)

    return jsonify(alternates)





if (__name__ == "__main__"):
    app.run()
