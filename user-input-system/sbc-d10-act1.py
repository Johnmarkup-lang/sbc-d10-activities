from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime, date

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',       # replace with your MySQL username (default is 'root')
    'password': '',       # replace with your MySQL password (default is '')
    'host': 'localhost',
    'database': 'flask_user_input_sys'  # replace with your database name
}

def calculate_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    birthday = request.form['birthday']
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, birthday) VALUES (%s, %s)', (name, birthday))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(status='success')

@app.route('/get_users', methods=['GET'])
def get_users():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT name, birthday FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    # Calculate age for each user
    users_with_age = []
    for user in users:
        name, birthday = user
        # Convert birthday to datetime object
        birthday = datetime.strptime(str(birthday), '%Y-%m-%d').date()
        age = calculate_age(birthday)
        users_with_age.append((name, birthday.strftime('%Y-%m-%d'), age))

    return jsonify(users_with_age)

if __name__ == '__main__':
    app.run(debug=True)
