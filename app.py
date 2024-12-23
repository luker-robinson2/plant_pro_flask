import sqlite3
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import secrets
import datetime
from makeDB import init_db, clear_db, takeReading, getReading


# py -m flask --app app run
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
clear_db()
init_db()

@app.route("/", methods=["GET", "POST"])  # Allow both GET and POST methods
def hello_world():
    # Get the message from the session (if any)
    message = session.get('message', None)
    plantID = session.get('plantID', None)
    return render_template('home.html', message=message, plantID=plantID)

@app.route('/submit', methods=['POST'])#submit button code
def submit():
    print(f"the form submit button has been pressed")
    # Store the message in the session
    session['message'] = "sensor reading:\nhumidity: 98%\nsunlight: 50%"
    session['plantID'] = "1"
    # Redirect back to the home page
    return redirect(url_for('hello_world'))

@app.route('/sensor', methods=['POST'])#input from esp32 sensor
def sensor_data():
    # Get JSON data from the POST request
    data = request.get_json()
    
    if data and 'plantID' in data and 'humidity' in data and 'sunlight' in data:
        plant_id = data['plantID']
        humidity = data['humidity']
        sunlight = data['sunlight']
        # Process the sensor data (print or store it)
        print(f"Received sensor data: {data}")
        takeReading(plant_id, humidity, sunlight, False)
        return jsonify({"status": "success", "message": "Data received"}), 200
    else:
        return jsonify({"status": "error", "message": "No data received"}), 400
    
@app.route('/get-sensor-data', methods=['GET'])#webpage is asking for the sensor readings, so query the database
def get_sensor_data():
    plant_id = 1
    print(f"getting sensor readings for: {plant_id}")
    data = getReading(1)
    if 'error' in data:
        return jsonify(data), 404  # Return error if no data found
    if data:
        # Process the sensor data (print or store it)
        print(f"User requested sensor data: {data}")
        return jsonify({"plantID": plant_id, "humidity": data[0],"sunlight": data[1],"timestamp": data[2]}), 200
    else:
        return jsonify({'error': 'Plant ID not found'}), 404

clear_db()