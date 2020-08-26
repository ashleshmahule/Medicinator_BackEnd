import dotenv
import os
import sys
from flask import Flask
from flask import request
from flask import jsonify
import predict
from flask_cors import CORS

dotenv.load_dotenv()


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome"

@app.route('/getResponse')
def getResponse():
    text=request.args.get('text')
    print(text)
    answer=predict.chatbot_response(text)

    return jsonify(answer)


if (__name__ == "__main__"):
    app.run()