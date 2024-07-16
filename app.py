#!/usr/bin/env python3
"""
app.py
Flask Application Entry Point
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
from views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
user_sign = True
is_admin = False

def check_user_sign(func):
    def wrapper(*args, **kwargs):
        if not user_sign:
            return redirect(url_for('hello_world'))
        if func.__name__ == 'admin' and not is_admin:
            return redirect(url_for('dashboard'))
        if is_admin:
            return func(*args, **kwargs)
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Set the name of the wrapper function
    return wrapper

@app.route('/')
def hello_world():
    if user_sign:
        return redirect(url_for('dashboard'))
    if user_sign and is_admin:
        return redirect(url_for('admin'))
    else:
        return render_template('auth/authentication.html', user_sign=user_sign)

@app.route('/admin')
@check_user_sign
def admin():
    return render_template('dashboard/admin_dashboard.html')

@app.route('/apply')
@check_user_sign
def apply_page():
    return render_template('dashboard/apply_leave.html')

@app.route('/apply_leave', methods=['POST'])
@check_user_sign
def apply_leave():
    leave_data = request.get_json()
    print(leave_data)
    # Process the leave data (e.g., save to database)
    return jsonify({'message': 'Leave application received', 'data': leave_data})

@app.route('/leaves')
@check_user_sign
def leaves():
    return render_template('dashboard/my_leaves.html')

@app.route('/change_password', methods=['POST'])
@check_user_sign
def change_password():
    password_data = request.get_json()
    print(password_data)
    # Process the leave data (e.g., save to database)
    return jsonify({'message': 'Leave application received', 'data': password_data})

@app.route('/password')
@check_user_sign
def password_page():
    return render_template('dashboard/change_password.html')

@app.route('/dashboard')
@check_user_sign
def dashboard():
    return render_template('dashboard/employee_dashboard.html')

if __name__ == '__main__':
    app.run(port=3000,
            host="0.0.0.0",
            debug=True)