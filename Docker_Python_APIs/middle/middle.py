#!/usr/bin/env python3

# see     https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

import flask
from flask import jsonify # provide data
from flask import request # flask dictionary of key-value returns
import requests # get data; see https://realpython.com/python-requests/
import random

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route("/api/v1/test", methods=["POST", "GET"])
def api_test():
    return jsonify("hello")

@app.route("/api/v1/instruction", methods=["POST"])
def api_recv_instruction():
    content = request.form['command']
    reslt = content + " " + str(random.choice(['0', '3', '5']))
    return jsonify(reslt)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

# EOF
