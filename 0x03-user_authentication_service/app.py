#!/usr/bin/env python3
"""
Module: app.py
Flask app
"""


from flask import Flask, jsonify


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    """
    this method returns the message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('users', methods=['POST'])
def users():
    """
    This method implements the endpoint to register a user
    """
    email = request.formget('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "user email already registeres"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
