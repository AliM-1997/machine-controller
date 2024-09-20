#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>

const char* ssid = "***";               
const char* password = "@@@ali*#*";    
const char* serverUrl = "http://192.168.1.4:8000/api/v1/sensor-data"; 

#define ONE_WIRE_BUS 4 // GPIO pin for DS18B20

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

WiFiClient client;  // Create WiFiClient object

void setup() {
  Serial.begin(9600);
  sensors.begin();

  WiFi.begin(ssid, password);
  Serial.println();
  Serial.println("Connecting to Wi-Fi");

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.print("NodeMCU IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("Failed to connect to Wi-Fi");
  }
}

void loop() {
  // Request temperature from DS18B20
  sensors.requestTemperatures();
  float temperatureC = sensors.getTempCByIndex(0);

  if (temperatureC == DEVICE_DISCONNECTED_C) {
    Serial.println("Error: Could not read temperature data");
  } else {
    Serial.print("Temperature: ");
    Serial.print(temperatureC);
    Serial.println(" °C");

    // Send temperature data to server
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(client, serverUrl);

      http.addHeader("Content-Type", "application/json");

      // Create JSON object
      StaticJsonDocument<200> jsonDoc;
      jsonDoc["Temperature"] = temperatureC;

      String jsonString;
      serializeJson(jsonDoc, jsonString);

      Serial.println("JSON String: " + jsonString);

      int httpResponseCode = http.POST(jsonString); 

      // Check HTTP response code
      Serial.print("HTTP Response Code: ");
      Serial.println(httpResponseCode);

      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println("Server response: " + response);
      } else {
        Serial.print("Error sending POST request: ");
        Serial.println(httpResponseCode);
        Serial.println(http.errorToString(httpResponseCode)); 
      }

      http.end();  // Close the connection
    } else {
      Serial.println("Error: Not connected to Wi-Fi");
    }
  }

  delay(5000);  // Wait 10 seconds before sending the next reading
}
