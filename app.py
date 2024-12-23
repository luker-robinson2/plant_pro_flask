import sqlite3
from flask import Flask, render_template, redirect, url_for, request,session
import secrets
import datetime


# py -m flask --app app run
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_breed TEXT
        )
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            humidity REAL,
            sunlight REAL,
            timestamp REAL,
            timestampText TEXT,
            plant_id INTEGER,
            image BLOB
            FOREIGN KEY (plant_id) REFERENCES plants(id)
        );
    ''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])  # Allow both GET and POST methods
def hello_world():
    # Get the message from the session (if any)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM plants")
    plants = cursor.fetchall()
    conn.close()
    message = session.get('message', None)
    return render_template('home.html', message=message)

@app.route('/submit', methods=['POST'])
def submit():
    print(f"the form submit button has been pressed")
    # Store the message in the session
    session['message'] = "sensor reading:\nhumidity: 98%\nsunlight: 50%"
    # Redirect back to the home page
    return redirect(url_for('hello_world'))

def testDB():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO plants (plant_breed)
    VALUES (?)
    ''', ('bamboo'))
    conn.commit()
    conn.close()

def takeReading():
    print(f"taking a sensor Reading")
    humidity = 0.99
    sunlight = 0.99
    image_path = './images/plant_test_image'
    timestamp = datetime.timestamp()
    timestampText = datetime.datetime.now()
    with open(image_path, 'rb') as file:
        image_data = file.read()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_readings (humidity, sunlight, timestamp, timestampText, plant_id, image)
        VALUES (?, ?, ?, ?, ?)
    ''',(humidity, sunlight, timestamp, timestampText, 1, image_data))
    conn.commit()
    conn.close()