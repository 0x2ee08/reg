/*********************************************************************
This is an example sketch for our Monochrome Nokia 5110 LCD Displays

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/products/338

These displays use SPI to communicate, 4 or 5 pins are required to
interface

Adafruit invests time and resources providing this open source code,
please support Adafruit and open-source hardware by purchasing
products from Adafruit!

Written by Limor Fried/Ladyada  for Adafruit Industries.
BSD license, check license.txt for more information
All text above, and the splash screen must be included in any redistribution
*********************************************************************/

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>

Adafruit_PCD8544 display = Adafruit_PCD8544(7, 6, 5, 4, 3);

String data;

void setup()   {
  Serial.begin(9600);

  display.begin();

  display.setContrast(13);

  display.clearDisplay();   // clears the screen and buffer

} 


void loop() {
  data = Serial.readStringUntil('\n');
  
  display.setTextSize(1);
  display.setTextColor(BLACK);    
  display.println(data);
  display.display();
  display.clearDisplay();
}
