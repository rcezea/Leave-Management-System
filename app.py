#!/usr/bin/env python3
"""
app.py
Flask Application Entry Point
"""

import os
from os import getenv
from flask import Flask, jsonify, abort, request
from views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=3000,
            host="0.0.0.0",
            debug=True)
