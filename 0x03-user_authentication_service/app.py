#!/usr/bin/env python3
"""
Module: app.py
Flask app
"""


from flask import Fals, jsonify


app= Flask(__name__)


@app.route('/')
def index():
    return jsonify({"message": "Bienvenue"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
