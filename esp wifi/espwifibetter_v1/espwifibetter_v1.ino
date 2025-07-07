#include <WiFi.h>
#include <Wire.h>
#include <MPU9250_asukiaaa.h>

const char* ssid = "UJJWALLENOVO";
const char* password = "Ujjwal123";
const char* host = "172.16.81.202"; // Replace with your PC IP
const uint16_t port = 12345;

WiFiClient client;

#define SDA_PIN 21
#define SCL_PIN 22

MPU9250_asukiaaa mySensor;

void setup() {
  Serial.begin(115200);
  Serial.println("Booting...");

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi connected!");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());

  Wire.begin(SDA_PIN, SCL_PIN);
  mySensor.setWire(&Wire);
  mySensor.beginAccel();

  Serial.print("Connecting to server at ");
  Serial.print(host);
  Serial.print(":");
  Serial.println(port);

  if (client.connect(host, port)) {
    Serial.println("✅ Connected to socket server!");
  } else {
    Serial.println("❌ Failed to connect to socket server");
  }
}

void loop() {
  mySensor.accelUpdate();
  float aX = mySensor.accelX();
  float aY = mySensor.accelY();
  float aZ = mySensor.accelZ();

  if (client.connected()) {
    String data = String(aX, 3) + "," + String(aY, 3) + "," + String(aZ, 3) + "\n";
    client.print(data);
    Serial.print("Sent: ");
    Serial.print(data);
  } else {
    Serial.println("⚠️ Server not connected. Reconnecting...");
    client.connect(host, port);  // Try reconnect
  }

  delay(10);
}
