#!/usr/bin/env python3

# see     https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

import flask
from flask import jsonify # provide data
import requests # get data
import random

app = flask.Flask(__name__)
app.config["DEBUG"] = True

vocab = ['a', 'b', 'c', 'd']

@app.route("/api/v1/number_of_commands/<int:count>", methods=["GET"])
def api_num_commands(count):
    list_of_responses = []
    # count is initially a string
    for indx in range(int(count)):
        this_cmd = random.choice(vocab)
        middle_url = "http://middle:5000/api/v1/instruction"
        # instead of a synchronous wait, we could use https://github.com/ross/requests-futures
        response = requests.post(url=middle_url, data={'command': this_cmd})
        list_of_responses.append(str(response.text))
#    middle_url = 'http://middle:5000/api/v1/test'
#    response = requests.get(url=middle_url)
#    return jsonify(response.text)

    return jsonify(list_of_responses)


@app.route("/api/v1/vocab/", methods=["GET"])
def api_list_vocab():
    return jsonify(vocab)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

# EOF
