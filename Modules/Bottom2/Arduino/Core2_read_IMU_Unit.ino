#include <M5Core2.h>
#include "I2C_MPU6886.h"

I2C_MPU6886 imu(I2C_MPU6886_DEFAULT_ADDRESS, Wire1);

// Accelerometer axis
float accX = 0.0F;
float accY = 0.0F;
float accZ = 0.0F;

// Gyroscope axis
float gyroX = 0.0F;
float gyroY = 0.0F;
float gyroZ = 0.0F;

// Temperature of the IMU chip
float temp = 0;

void setup() {
  // Begin function initializes important M5Core2 functions
  M5.begin();
  // Clear whole screen for better graphics
  M5.Lcd.fillScreen(WHITE);
  M5.Lcd.setTextColor(BLACK);

  // Function initializes wire function
  Wire1.begin(21, 22);
  // Begin function initializes imu functions
  imu.begin();
}

void loop() {
  // Get all data of the IMU
  imu.getGyro(&gyroX, &gyroY, &gyroZ);
  imu.getAccel(&accX, &accY, &accZ);
  imu.getTemp(&temp);

  // Print gyroscope axis
  M5.Lcd.fillRect(95, 20, 200, 20, WHITE);
  M5.Lcd.setCursor(30, 20);
  M5.Lcd.printf("Gyroscope: %6.2f  %6.2f  %6.2f  o/s", gyroX, gyroY, gyroZ);
  // Print accelerometer axis
  M5.Lcd.fillRect(120, 40, 150, 20, WHITE);
  M5.Lcd.setCursor(30, 40);
  M5.Lcd.printf("Accelerometer: %5.2f   %5.2f   %5.2f   ", accX, accY, accZ);
  // Print temperature of the IMU chip
  M5.Lcd.fillRect(160, 80, 50, 20, WHITE);
  M5.Lcd.setCursor(30, 80);
  M5.Lcd.printf("IMU chip temperature: %.2f C", temp);

  delay(500);
}
