from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Cobrakai@123',
    database='train_booking'
)

def get_all_stations():
    cursor = db.cursor()
    cursor.execute("SELECT id, station_code, station_name, city FROM stations")
    stations = cursor.fetchall()
    cursor.close()
    return stations

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        hashed_password = generate_password_hash(password)
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('Username already exists!')
                return redirect(url_for('register'))
            cursor.execute(
                "INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)",
                (username, hashed_password, email, phone)
            )
            db.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            print("Registration error:", e)
            flash('Registration failed.')
            return redirect(url_for('register'))
        finally:
            cursor.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        if result and check_password_hash(result[0], password):
            stations = get_all_stations()
            return render_template('dashboard.html', username=username, stations=stations)
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)