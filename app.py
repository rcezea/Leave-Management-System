#!/usr/bin/env python3
"""
app.py
Flask Application Entry Point
"""

from flask import Flask, render_template
from views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.route('/')
def hello_world():
    return render_template('auth/authentication.html')


if __name__ == '__main__':
    app.run(port=3000,
            host="0.0.0.0",
            debug=True)
