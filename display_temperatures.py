import requests
import json
import configparser

# Read the configuration file
config = configparser.ConfigParser()
config.read('hue_config.ini')

# Get credentials from the config file
bridge_ip = config['hue']['bridge_ip']
username = config['hue']['username']

# Get all sensors from the Hue Bridge
url = f"http://{bridge_ip}/api/{username}/sensors"
response = requests.get(url)
sensors = json.loads(response.text)

temp_sensors = {}
motion_sensors = {}

# Separate temperature and motion sensors and store them by uniqueid
for sensor_id, sensor_data in sensors.items():
    if sensor_data["type"] == "ZLLTemperature":
        temp_sensors[sensor_data["uniqueid"]] = sensor_data
    elif sensor_data["type"] == "ZLLPresence":
        motion_sensors[sensor_data["uniqueid"]] = sensor_data

# Match temperature sensors to motion sensors based on uniqueid pattern
for temp_sensor_uniqueid, temp_sensor_data in temp_sensors.items():
    for motion_sensor_uniqueid, motion_sensor_data in motion_sensors.items():
        # Check if the uniqueids are similar, indicating a paired sensor
        if temp_sensor_uniqueid[:-5] == motion_sensor_uniqueid[:-5]:  # Compare most of the uniqueid
            motion_sensor_name = motion_sensor_data["name"]
            temperature = temp_sensor_data["state"]["temperature"] / 100

            print(f"Motion Sensor: {motion_sensor_name}")
            print(f"Temperature: {temperature} °C")
            break  # Move to the next temperature sensor once a match is found
