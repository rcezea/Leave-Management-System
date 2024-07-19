#!/usr/bin/env python3
"""
app.py
Flask Application Entry Point
"""
from os import getenv

from flask import Flask, render_template
from flask_wtf import csrf
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

# Initialize CSRF protection
csrf = csrf.CSRFProtect(app)

# Enable CORS
CORS(app)


@app.route('/')
def hello_world():
    return render_template('auth/authentication.html')


if __name__ == '__main__':
    from views import app_views
    app.register_blueprint(app_views)
    app.run(port=3000,
            host="0.0.0.0",
            debug=True)
