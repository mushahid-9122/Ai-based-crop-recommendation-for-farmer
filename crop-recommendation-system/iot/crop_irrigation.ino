// Crop Irrigation Automation System - Arduino UNO Version
// Components: Soil Moisture Sensor, DHT11/DHT22, Relay Module, Optional Rain Sensor

#include <DHT.h>

// Pin definitions
#define SOIL_MOISTURE_PIN A0 // Analog pin for soil moisture sensor
#define DHT_PIN 2            // Digital pin for DHT sensor
#define RELAY_PIN 3          // Digital pin for relay module (water pump)
#define RAIN_SENSOR_PIN 4    // Digital pin for rain sensor (optional)

// DHT sensor type
#define DHT_TYPE DHT11 // or DHT22

// Thresholds (adjust based on your sensors and requirements)
#define SOIL_MOISTURE_THRESHOLD 500 // Below this value, soil is dry (0-1023)
#define TEMPERATURE_THRESHOLD 30.0  // Above this temperature, check humidity
#define HUMIDITY_THRESHOLD 60.0     // Below this humidity, consider watering
#define RAIN_THRESHOLD 500          // Below this value, it's raining (0-1023)

// Timing
#define READING_INTERVAL 60000 // Read sensors every 60 seconds (60000ms)
#define PUMP_DURATION 5000     // Run pump for 5 seconds when watering

// Initialize DHT sensor
DHT dht(DHT_PIN, DHT_TYPE);

// Global variables
float temperature = 0.0;
float humidity = 0.0;
int soilMoisture = 0;
int rainValue = 0;

void setup()
{
    // Initialize serial communication
    Serial.begin(9600);
    Serial.println("Crop Irrigation System - Arduino UNO Version");
    Serial.println("Components: Soil Moisture, DHT11/DHT22, Relay, Optional Rain Sensor");

    // Initialize DHT sensor
    dht.begin();

    // Set pin modes
    pinMode(RELAY_PIN, OUTPUT);
    pinMode(SOIL_MOISTURE_PIN, INPUT);
    pinMode(RAIN_SENSOR_PIN, INPUT);

    // Ensure relay is off initially (assuming active low)
    digitalWrite(RELAY_PIN, HIGH);
}

void loop()
{
    // Read sensors
    readSensors();

    // Print sensor readings
    printSensorData();

    // Decision logic for watering
    bool shouldWater = checkWateringConditions();

    if (shouldWater)
    {
        Serial.println("Starting irrigation...");
        activatePump();
        Serial.println("Irrigation completed.");
    }
    else
    {
        Serial.println("No irrigation needed.");
    }

    // Wait before next reading
    delay(READING_INTERVAL);
}

void readSensors()
{
    // Read soil moisture
    soilMoisture = analogRead(SOIL_MOISTURE_PIN);

    // Read temperature and humidity
    temperature = dht.readTemperature();
    humidity = dht.readHumidity();

    // Read rain sensor (optional)
    rainValue = digitalRead(RAIN_SENSOR_PIN);

    // Check for DHT reading errors
    if (isnan(temperature) || isnan(humidity))
    {
        Serial.println("Failed to read from DHT sensor!");
        temperature = 0.0;
        humidity = 0.0;
    }
}

void printSensorData()
{
    Serial.print("Soil Moisture: ");
    Serial.print(soilMoisture);
    Serial.print(" | Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C | Humidity: ");
    Serial.print(humidity);
    Serial.print(" % | Rain Sensor: ");
    Serial.println(rainValue);
}

bool checkWateringConditions()
{
    // Check if soil is dry
    if (soilMoisture > SOIL_MOISTURE_THRESHOLD)
    {
        return false; // Soil is moist enough
    }

    // Check temperature and humidity conditions
    if (temperature > TEMPERATURE_THRESHOLD && humidity < HUMIDITY_THRESHOLD)
    {
        // Check rain sensor (if raining, don't water)
        if (rainValue == LOW)
        {                 // Assuming LOW means rain detected
            return false; // It's raining
        }
        return true; // Conditions met for watering
    }

    return false; // Conditions not met
}

void activatePump()
{
    // Turn on pump (assuming relay is active low)
    digitalWrite(RELAY_PIN, LOW);
    delay(PUMP_DURATION);

    // Turn off pump
    digitalWrite(RELAY_PIN, HIGH);
}

// Optional: Send data to backend via serial (for debugging or external processing)
// This function can be called to send data in JSON format
void sendDataToBackend()
{
    Serial.print("{");
    Serial.print("\"timestamp\":\"");
    Serial.print(millis()); // Simple timestamp
    Serial.print("\",\"soil_moisture\":");
    Serial.print(soilMoisture);
    Serial.print(",\"temperature\":");
    Serial.print(temperature);
    Serial.print(",\"humidity\":");
    Serial.print(humidity);
    Serial.print(",\"rain_value\":");
    Serial.print(rainValue);
    Serial.println("}");
}
