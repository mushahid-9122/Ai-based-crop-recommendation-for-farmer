# IoT/Automation Integration for Crop Recommendation System

This directory contains IoT automation components for the Crop Recommendation System, enabling automated irrigation and real-time sensor monitoring using Arduino UNO or Raspberry Pi.

## Components

### Hardware Requirements

- **Microcontroller**: Arduino UNO or Raspberry Pi
- **Sensors**:
  - Soil Moisture Sensor (analog/digital)
  - DHT11 or DHT22 Temperature & Humidity Sensor
  - Rain Sensor (optional)
- **Actuators**:
  - Relay Module (for water pump control)
  - Water Pump (12V DC)
- **Power Supply**:
  - Solar Panel (optional for sustainable power)
  - Battery Pack or DC Power Supply
- **Additional**:
  - Jumper Wires
  - Breadboard
  - Resistors (if needed)

### Software Requirements

- **Arduino IDE** (for Arduino UNO)
- **Python 3** (for Raspberry Pi)
- Required libraries:
  - Arduino: DHT sensor library
  - Raspberry Pi: Adafruit_DHT, RPi.GPIO, requests

## Hardware Connections

### Arduino UNO Connections

```
Arduino UNO Pinout:
- Digital Pin 2: DHT11/DHT22 Data Pin
- Digital Pin 3: Relay Module Signal Pin
- Analog Pin A0: Soil Moisture Sensor
- Digital Pin 4: Rain Sensor (optional)
- 5V: Power for sensors
- GND: Ground for all components

Power Connections:
- Arduino 5V -> Relay VCC
- Arduino GND -> Relay GND
- External 12V -> Water Pump (through relay)
- Solar Panel -> Battery/Charging Circuit -> Arduino VIN
```

### Raspberry Pi Connections

```
Raspberry Pi GPIO Pinout (BCM numbering):
- GPIO 4: DHT11/DHT22 Data Pin
- GPIO 18: Relay Module Signal Pin
- GPIO 17: Soil Moisture Sensor
- GPIO 27: Rain Sensor (optional)
- 5V: Power for sensors
- GND: Ground for all components

Power Connections:
- Raspberry Pi 5V -> Relay VCC
- Raspberry Pi GND -> Relay GND
- External 12V -> Water Pump (through relay)
- Solar Panel -> Battery/Charging Circuit -> Raspberry Pi Power Input
```

## Setup Instructions

### Arduino UNO Setup

1. **Install Arduino IDE**
   - Download from https://www.arduino.cc/en/software
   - Install the DHT sensor library via Library Manager

2. **Upload the Sketch**
   - Open `crop_irrigation.ino` in Arduino IDE
   - Select Board: Arduino UNO
   - Select Port: Your Arduino COM port
   - Upload the sketch

3. **Configure Thresholds**
   - Edit the threshold values in the sketch:
     ```cpp
     #define SOIL_MOISTURE_THRESHOLD 500
     #define TEMPERATURE_THRESHOLD 30.0
     #define HUMIDITY_THRESHOLD 60.0
     #define RAIN_THRESHOLD 500
     ```

### Raspberry Pi Setup

1. **Install Dependencies**

   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install Adafruit_DHT RPi.GPIO requests
   ```

2. **Run the Script**

   ```bash
   python3 crop_irrigation_rpi.py
   ```

3. **Configure Settings**
   - Edit the configuration variables in the script:
     ```python
     SOIL_MOISTURE_THRESHOLD = 500
     TEMPERATURE_THRESHOLD = 30.0
     HUMIDITY_THRESHOLD = 60.0
     RAIN_THRESHOLD = 500
     BACKEND_URL = "http://your-backend-ip:5000/api/sensor-data"
     ```

## Backend Integration

The backend API now includes endpoints for sensor data:

### POST /api/sensor-data

Receive sensor data from IoT devices.

**Request Body:**

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "soil_moisture": 450.5,
  "temperature": 25.3,
  "humidity": 65.2,
  "rain_value": 300.0
}
```

**Response:**

```json
{
  "success": true,
  "message": "Sensor data received successfully"
}
```

### GET /api/sensor-data

Retrieve the latest sensor data.

**Response:**

```json
{
  "success": true,
  "data": {
    "timestamp": "2024-01-01T12:00:00Z",
    "soil_moisture": 450.5,
    "temperature": 25.3,
    "humidity": 65.2,
    "rain_value": 300.0
  }
}
```

## Automation Logic

The system uses the following decision logic for irrigation:

1. **Soil Moisture Check**: If soil moisture is below threshold, consider watering
2. **Weather Conditions**: Check temperature and humidity levels
3. **Rain Detection**: Skip watering if rain is detected (optional)
4. **Irrigation**: Activate water pump for specified duration

### Thresholds (Adjust based on your environment)

- **Soil Moisture**: 0-1023 (lower = drier soil)
- **Temperature**: > 30°C triggers additional checks
- **Humidity**: < 60% may require watering
- **Rain Sensor**: < 500 indicates rain

## Solar Power Setup (Optional)

For sustainable operation:

1. **Solar Panel**: 12V, 10W minimum
2. **Charge Controller**: To prevent battery overcharge
3. **Battery**: 12V Lead-acid or Li-ion
4. **DC-DC Converter**: For stable 5V/3.3V output

### Wiring Diagram

```
Solar Panel -> Charge Controller -> Battery -> DC-DC Converter -> Microcontroller + Sensors
```

## Troubleshooting

### Common Issues

1. **Sensor Readings Unstable**
   - Check power connections
   - Ensure proper grounding
   - Calibrate sensor thresholds

2. **Relay Not Activating**
   - Verify relay module connections
   - Check power supply voltage
   - Test relay with simple sketch

3. **Backend Connection Failed**
   - Verify IP address and port
   - Check network connectivity
   - Ensure backend is running

4. **DHT Sensor Errors**
   - Wait 2 seconds between readings
   - Check DHT pin connections
   - Verify DHT type (11 or 22)

### Calibration

1. **Soil Moisture Sensor**
   - Place in dry soil: Record minimum value
   - Water thoroughly: Record maximum value
   - Set threshold at 30-50% of range

2. **Temperature/Humidity**
   - Compare with known thermometer/hygrometer
   - Adjust thresholds based on crop requirements

## Safety Precautions

- **Water Safety**: Ensure electrical components are properly isolated from water
- **Power Management**: Use appropriate fuses and circuit breakers
- **Weather Protection**: House electronics in waterproof enclosure
- **Regular Maintenance**: Clean sensors and check connections periodically

## Future Enhancements

- Add WiFi/Ethernet connectivity for remote monitoring
- Implement machine learning for adaptive irrigation
- Add multiple sensor nodes for larger fields
- Integrate with weather APIs for better predictions
- Add data logging and analytics

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Verify hardware connections
3. Test components individually
4. Review sensor calibration

---

**Note**: Always test the system in a controlled environment before field deployment. Monitor sensor readings and adjust thresholds based on your specific crop and soil conditions.
