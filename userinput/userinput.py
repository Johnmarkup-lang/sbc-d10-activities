from flask import Flask, render_template, request, jsonify
from datetime import datetime, date

app = Flask(__name__, template_folder='templates')

users = []  # Store users in memory

def calculate_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    global users
    name = request.form['name']
    birthday = request.form['birthday']
    
    users.append({'name': name, 'birthday': datetime.strptime(birthday, '%Y-%m-%d').date()})
    
    return jsonify(status='success')

@app.route('/get_users', methods=['GET'])
def get_users():
    global users
    users_with_age = []
    for user in users:
        age = calculate_age(user['birthday'])
        users_with_age.append({'name': user['name'], 'age': age})
    
    return jsonify(users_with_age)

if __name__ == '__main__':
    app.run(debug=True)
