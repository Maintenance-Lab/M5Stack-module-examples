from m5stack import *
from m5ui import *
from uiflow import *
import time
import unit

# set the background color to black
setScreenColor(0x000)

# initialize the env3 sensor on port A
env3_0 = unit.get(unit.ENV3, unit.PORTA)

# create the labels for the temperature, humidity and pressure
temp_title = M5TextBox(10, 30, "Temperature:", lcd.FONT_Default, 0xffa6a6, rotate=0)
temp_val_label = M5TextBox(10, 50, "temperature_val", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)

hum_title = M5TextBox(10, 99, "Humidity", lcd.FONT_Default, 0xb0adff, rotate=0)
hum_val_label = M5TextBox(10, 119, "humidity_val", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)

pres_title = M5TextBox(10, 166, "Pressure", lcd.FONT_Default, 0x94f18d, rotate=0)
pres_val_label = M5TextBox(10, 182, "pressure_val", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)

# function to generate a color based on the temperature
# first the colors are generated in values from 0 to 255 and then converted to a single hex value
# bluest color is at minTemp value, now 10 C
# reddest color is at maxTemp value, now 30 C
def temp_to_color(temp):
    minTemp = 10
    maxTemp = 30
    r = int(255 * (temp - minTemp) / (maxTemp - minTemp))
    g = 0
    b = int(255 * (maxTemp - temp) / (maxTemp - minTemp))
    color = (r << 16) + (g << 8) + b
    return color

while True:

    # read the temperature, pressure and humidity values and 
    # round them to 2 decimal places since the stickc display is smaller
    temp_value = round(env3_0.temperature,2)
    press_value = round(env3_0.pressure,2)
    humi_value = round(env3_0.humidity,2)

    # set text of label0 to temperature + env3_0.temperature + 'C'
    temp_val_label.setText(str(round(env3_0.temperature,2)) + ' C')
    # set the color of the temperature label to the color generated by the temp_to_color function
    temp_val_label.setColor(temp_to_color(temp_value))
    # set text of label0 to humidity + env3_0.humidity + '%'
    hum_val_label.setText(str(round(env3_0.humidity,2)) + ' %')
    # set text of label0 to pressure + env3_0.pressure + 'hPa'
    pres_val_label.setText(str(round(env3_0.pressure,2)) + ' hPa')

    wait_ms(10)

