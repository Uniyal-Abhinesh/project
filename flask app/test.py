import json
import mysql.connector

with open('stations.json') as f:
    data = json.load(f)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="train"
)
cursor = conn.cursor()

for feature in data['features']:
    props = feature['properties']
    code = props.get('code', '')
    name = props.get('name', '')
    city = props.get('address', '')

    if code and name:
        cursor.execute(
            "INSERT INTO stations (station_code, station_name, city) VALUES (%s, %s, %s)",
            (code, name, city)
        )

conn.commit()
conn.close()
