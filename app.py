#!/usr/bin/env python3
"""
app.py
Flask Application Entry Point
"""
from os import getenv
from flask import Flask, render_template
from flask_wtf import csrf
from flask_cors import CORS
from views import app_views
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['WTF_CSRF_SECRET_KEY'] = getenv('WTF_CSRF_SECRET_KEY')

# Initialize CSRF protection
csrf = csrf.CSRFProtect(app)

# Enable CORS
CORS(app)


@app.route('/')
def hello_world():
    return render_template('auth/authentication.html')


app.register_blueprint(app_views)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000', debug=True)
