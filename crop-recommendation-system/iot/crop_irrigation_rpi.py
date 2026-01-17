#!/usr/bin/env python3
"""
Crop Irrigation Automation System - Raspberry Pi Version
Python script for sensor reading and automated irrigation control using Raspberry Pi
Components: Soil Moisture Sensor, DHT11/DHT22, Relay Module, Optional Rain Sensor

Requirements:
- pip install Adafruit_DHT RPi.GPIO requests
"""

import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import requests
import json
from datetime import datetime

# Pin definitions (BCM numbering)
SOIL_MOISTURE_PIN = 17    # GPIO pin for soil moisture sensor (analog via ADC)
DHT_PIN = 4               # GPIO pin for DHT sensor
RELAY_PIN = 18            # GPIO pin for relay module (water pump)
RAIN_SENSOR_PIN = 27      # GPIO pin for rain sensor (optional)

# DHT sensor type
DHT_SENSOR = Adafruit_DHT.DHT11  # or Adafruit_DHT.DHT22

# Thresholds (adjust based on your sensors and requirements)
SOIL_MOISTURE_THRESHOLD = 500   # Below this value, soil is dry (0-1023)
TEMPERATURE_THRESHOLD = 30.0    # Above this temperature, check humidity
HUMIDITY_THRESHOLD = 60.0       # Below this humidity, consider watering
RAIN_THRESHOLD = 500            # Below this value, it's raining (0-1023)

# Timing
READING_INTERVAL = 60            # Read sensors every 60 seconds
PUMP_DURATION = 5                # Run pump for 5 seconds when watering

# Backend API configuration (optional)
BACKEND_URL = "http://localhost:5000/api/sensor-data"  # Update with your backend URL

def setup_gpio():
    """Setup GPIO pins"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay off (assuming active low)
    GPIO.setup(SOIL_MOISTURE_PIN, GPIO.IN)
    GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN)

def read_soil_moisture():
    """Read soil moisture sensor (simplified - may need ADC for accurate reading)"""
    # Note: This is a simplified digital read. For analog sensors, use ADC like MCP3008
    return GPIO.input(SOIL_MOISTURE_PIN)

def read_dht_sensor():
    """Read temperature and humidity from DHT sensor"""
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return temperature, humidity

def read_rain_sensor():
    """Read rain sensor (simplified)"""
    return GPIO.input(RAIN_SENSOR_PIN)

def control_pump(state):
    """Control water pump via relay"""
    GPIO.output(RELAY_PIN, state)

def send_data_to_backend(soil_moisture, temperature, humidity, rain_value):
    """Send sensor data to backend API"""
    try:
        data = {
            "timestamp": datetime.now().isoformat(),
            "soil_moisture": soil_moisture,
            "temperature": temperature,
            "humidity": humidity,
            "rain_value": rain_value
        }
        response = requests.post(BACKEND_URL, json=data)
        if response.status_code == 200:
            print("Data sent to backend successfully")
        else:
            print(f"Failed to send data to backend: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to backend: {e}")

def main():
    print("Crop Irrigation System - Raspberry Pi Version")
    print("Components: Soil Moisture, DHT11/DHT22, Relay, Optional Rain Sensor")

    setup_gpio()

    try:
        while True:
            # Read sensors
            soil_moisture = read_soil_moisture()
            temperature, humidity = read_dht_sensor()
            rain_value = read_rain_sensor()

            print(f"Soil Moisture: {soil_moisture}")
            print(f"Temperature: {temperature} °C")
            print(f"Humidity: {humidity} %")
            print(f"Rain Sensor: {rain_value}")

            # Decision logic for watering
            should_water = False

            if soil_moisture < SOIL_MOISTURE_THRESHOLD:
                if temperature and temperature > TEMPERATURE_THRESHOLD and humidity and humidity < HUMIDITY_THRESHOLD:
                    if rain_value > RAIN_THRESHOLD:
                        should_water = True

            if should_water:
                print("Starting irrigation...")
                control_pump(GPIO.LOW)  # Turn on pump
                time.sleep(PUMP_DURATION)
                control_pump(GPIO.HIGH)  # Turn off pump
                print("Irrigation completed.")
            else:
                print("No irrigation needed.")

            # Send data to backend (optional)
            if temperature and humidity:
                send_data_to_backend(soil_moisture, temperature, humidity, rain_value)

            time.sleep(READING_INTERVAL)

    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
