import sqlite3
import datetime

def init_db():
    # Connect to SQLite database (it will create the database file if it doesn't exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create the `plants` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_breed TEXT
        )
    ''')
    
    # Create the `sensor_readings` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            humidity REAL,
            sunlight REAL,
            timestamp REAL,
            timestampText TEXT,
            plant_id INTEGER,
            image BLOB,
            FOREIGN KEY (plant_id) REFERENCES plants(id)
        )
    ''')
    conn.commit()
    conn.close()

def makePlant(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO plants (id, plant_breed)
        VALUES (?,?)
    ''', (id, 'bamboo'))  # Ensure it's a tuple by adding the trailing comma
    conn.commit()
    conn.close()

def getPlants():
    print(f"getting plants")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM plants;
    ''')  # Ensure it's a tuple by adding the trailing comma
    data = cursor.fetchall()
    for row in data:
        print(row)
    conn.commit()
    conn.close()
    return data


def takeReading(id, humidity, sunlight, includeImg):
    print(f"Taking a sensor reading of: {id}")
    image_path = './images/plant_test_image.jpg'  # Ensure the image exists
    timestamp = datetime.datetime.now().timestamp()
    timestampText = datetime.datetime.now().isoformat()  # Use ISO format for text timestamp
    if includeImg:#if you want to send an image to the database then get it, if not then dont
        with open(image_path, 'rb') as file:
            image_data = file.read()
    else:
        image_data = None

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_readings (humidity, sunlight, timestamp, timestampText, plant_id, image)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (humidity, sunlight, timestamp, timestampText, id, image_data))
    conn.commit()
    conn.close()

def getReading():
    print(f"getting sensor readings")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT humidity, sunlight, timestampText FROM sensor_readings ORDER BY timestamp DESC;
    ''')
    data = cursor.fetchone()
    for row in data:
        print(row)
    conn.close()
    return data

def getReading(plant_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT humidity, sunlight, timestampText FROM sensor_readings WHERE plant_id = (?) ORDER BY timestamp DESC;
    ''', (plant_id,))
    data = cursor.fetchone()
    print(data)
    if data is None:
        conn.close()
        return {'error': 'No data found for plant ID {plant_id}'}

    conn.close()
    return data

def getImageFromReading():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT image FROM sensor_readings;
    ''')
    data = cursor.fetchone()[0]
    print(f"Fetched image data!!!")
    with open('./images/plant_image_from_database.jpg', 'wb') as file:
        file.write(data)
    conn.close()

def clear_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Delete all records from both tables
    cursor.execute('DELETE FROM sensor_readings')
    cursor.execute('DELETE FROM plants')
    
    # Optionally, reset the AUTOINCREMENT counters
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "sensor_readings"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "plants"')
    
    conn.commit()
    conn.close()
    print("Database cleared!")

# Call the function to initialize the database and perform test actions
# init_db()
# makePlant(1)
# makePlant(2)
# takeReading(1, 50.00, 60.00, True)
# takeReading(2, 70.00, 60.00, True)
# getPlants()
# getReading()
# # getImageFromReading()
# clear_db()
