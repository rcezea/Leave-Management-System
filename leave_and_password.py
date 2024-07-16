from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/apply')
def apply_page():
    return render_template('dashboard/apply_leave.html')

@app.route('/apply_leave', methods=['POST'])
def apply_leave():
    leave_data = request.get_json()
    print(leave_data)
    # Process the leave data (e.g., save to database)
    return jsonify({'message': 'Leave application received', 'data': leave_data})

@app.route('/leaves')
def leaves():
    return render_template('dashboard/my_leaves.html')

@app.route('/')
def home():
    return render_template('dashboard/employee_dashboard.html')

@app.route('/change_password', methods=['POST'])
def change_password():
    password_data = request.get_json()
    print(password_data)
    # Process the leave data (e.g., save to database)
    return jsonify({'message': 'Leave application received', 'data': password_data})

@app.route('/password')
def password_page():
    return render_template('dashboard/change_password.html')

if __name__ == '__main__':
    app.run(debug=True)
