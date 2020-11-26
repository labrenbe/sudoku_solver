from flask import Flask
from flask import request
from flask_cors import CORS

DEBUG = True

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route("/solve", methods=["POST"])
def solve():
    print(request)
    return '... Solved!'


if __name__ == '__main__':
    app.run()
