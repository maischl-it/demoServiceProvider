from flask import Flask
import os

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def home():

    text = "provider"

    returnValue = text, 200

    if os.environ.get("fail", "false") == 'true':
        returnValue = "failed", 500

    return returnValue


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
