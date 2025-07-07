#include <Wire.h>
#include <MPU9250_asukiaaa.h>

#ifdef _ESP32_HAL_I2C_H_
#define SDA_PIN 21
#define SCL_PIN 22
#endif

MPU9250_asukiaaa mySensor;

float aX, aY, aZ, aSqrt;
float gX, gY, gZ;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("MPU9250 Max Range (Manual Reg Write)");

#ifdef _ESP32_HAL_I2C_H_
  Wire.begin(SDA_PIN, SCL_PIN);
  mySensor.setWire(&Wire);
#endif

  mySensor.beginAccel();
  mySensor.beginGyro();

  // 🔧 Set max range using direct I2C writes
  Wire.beginTransmission(0x68); // MPU9250 default I2C address
  Wire.write(0x1C); // ACCEL_CONFIG
  Wire.write(0x18); // Set ±16g
  Wire.endTransmission();

  Wire.beginTransmission(0x68);
  Wire.write(0x1B); // GYRO_CONFIG
  Wire.write(0x18); // Set ±2000°/s
  Wire.endTransmission();
}

void loop() {
  int result = mySensor.accelUpdate();
  if (result == 0) {
    aX = mySensor.accelX();
    aY = mySensor.accelY();
    aZ = mySensor.accelZ();
    aSqrt = mySensor.accelSqrt();

    Serial.println("---- Accelerometer (±16g) ----");
    Serial.print("X: "); Serial.print(aX);
    Serial.print("  Y: "); Serial.print(aY);
    Serial.print("  Z: "); Serial.print(aZ);
    Serial.print("  √Sum: "); Serial.println(aSqrt);
  } else {
    Serial.println("⚠️ Failed to read accel");
  }

  result = mySensor.gyroUpdate();
  if (result == 0) {
    gX = mySensor.gyroX();
    gY = mySensor.gyroY();
    gZ = mySensor.gyroZ();

    Serial.println("---- Gyroscope (±2000°/s) ----");
    Serial.print("X: "); Serial.print(gX);
    Serial.print("  Y: "); Serial.print(gY);
    Serial.print("  Z: "); Serial.println(gZ);
  } else {
    Serial.println("⚠️ Failed to read gyro");
  }

  Serial.println();
  delay(500);
}
