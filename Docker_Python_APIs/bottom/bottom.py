#!/usr/bin/env python3

# see     https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

import flask
from flask import jsonify # provide data
import requests # get data

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route("/api/v1/instructions/", methods=["GET"])
def api_all_derivations():
    return jsonify(vocab)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

# EOF
