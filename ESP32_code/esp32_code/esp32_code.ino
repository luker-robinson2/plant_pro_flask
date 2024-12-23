#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <String.h>

// Replace with your Wi-Fi credentials
const char* ssid = "";
const char* password = "";
const char* plantID = "1";
// The IP address of the machine running the Flask server (replace with your local IP)
const char* serverUrl = "http://ip:5000/sensor";
const int ledPin = 2; // Define the GPIO pin connected to your LED


int idx = 0;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT); // Set the LED pin as output
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to Wifi");
  }
  Serial.println("Connected to Wifi!!!");
  sendData();

}



void loop() {
  delay(1000);
  sendData();

}

void sendData(){
  float cycleValsHumidity[5] = {50.00,60.00,70.00,80.00,90.00};
  float cycleValsSunlight[5] = {10.00,20.00,30.00,40.00,50.00};
  if (idx > 4) {
    idx = 0;
  }
  float humidity = cycleValsHumidity[idx];
  float sunlight = cycleValsSunlight[idx];
  idx++;

  StaticJsonDocument<200> doc;
  doc["plantID"] = 1;
  doc["sunlight"] = sunlight;
  doc["humidity"] = humidity;

  // Serialize JSON object to a string
  String jsonData;
  serializeJson(doc, jsonData);

  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int httpResponse = http.POST(jsonData);
  if (httpResponse > 0) {
    Serial.print("HTTP Response Code:");
    Serial.println(httpResponse);
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.print("HTTP Error :( ");
    Serial.println(httpResponse);
  }
  http.end();
}