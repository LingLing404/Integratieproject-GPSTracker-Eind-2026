import json
import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt

load_dotenv()

INFLUX_URL = "http://10.6.121.191:8086"
INFLUX_TOKEN = os.environ.get("INFLUX_TOKEN")
INFLUX_ORG = os.environ.get("INFLUX_ORG")
INFLUX_BUCKET = os.environ.get("INFLUX_BUCKET")

MQTT_BROKER = "10.6.121.191"
MQTT_PORT = 1883
MQTT_TOPIC = "trackers/location"

INDEX_FILE = "device_index.json"

def load_device_index() -> dict:
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE) as f:
            return json.load(f)
    return {"map": {}, "next": 1}

def save_device_index(data: dict):
    with open(INDEX_FILE, "w") as f:
        json.dump(data, f)

def get_device_index(device_id: str) -> int:
    data = load_device_index()
    if device_id not in data["map"]:
        data["map"][device_id] = data["next"]
        data["next"] += 1
        save_device_index(data)
    return data["map"][device_id]

def send_location_to_mqtt(device_name, device_id, latitude, longitude, timestamp):
    index = get_device_index(device_id)
    payload = json.dumps({
        "device_name": device_name,
        "device_id": device_id,
        "device_index": index,
        "latitude": float(latitude),
        "longitude": float(longitude),
        "timestamp": timestamp
    })
    try:
        client = mqtt.Client()
        client.username_pw_set("mqttuser", "gps-tracking")
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.publish(MQTT_TOPIC, payload)
        client.disconnect()
        print(f"✅ MQTT gepubliceerd voor {device_name}!")
    except Exception as e:
        print(f"❌ Fout bij MQTT publiceren: {e}")

def send_location_to_influx(device_name, device_id, latitude, longitude, timestamp):
    # Eerst naar MQTT publiceren
    send_location_to_mqtt(device_name, device_id, latitude, longitude, timestamp)
    
    # Dan rechtstreeks naar InfluxDB schrijven
    index = get_device_index(device_id)
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point("location") \
        .tag("device_name", device_name) \
        .tag("device_id", device_id) \
        .field("latitude", float(latitude)) \
        .field("longitude", float(longitude)) \
        .field("device_index", float(index)) \
        .time(timestamp, WritePrecision.S)

    try:
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print(f"✅ InfluxDB geschreven voor {device_name} (index {index})!")
    except Exception as e:
        print(f"❌ Fout bij schrijven naar InfluxDB: {e}")
    finally:
        client.close()