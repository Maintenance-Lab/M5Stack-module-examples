from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
import unit

# Initate the screen
screen = M5Screen()
screen.clean_screen()

# set screen background color to black
screen.set_screen_bg_color(0x000)

# Initate the env3 sensor on port A of the core 2
env3_0 = unit.get(unit.ENV3, unit.PORTA)

# Initate the labels, one for the title and one for the value
temp_title = M5Label('Temp', x=35, y=10, color=0xFFFFFF, font=FONT_MONT_14, parent=None)
temp_val_label = M5Label('00.00 C', x=100, y=10, color=0xcb4848, font=FONT_MONT_14, parent=None)

hum_title = M5Label('Humidity', x=10, y=40, color=0xFFFFFF, font=FONT_MONT_14, parent=None)
hum_val_label = M5Label('00.00 %', x=100, y=40, color=0x4c8cbf, font=FONT_MONT_14, parent=None)

pres_title = M5Label('Pressure', x=15, y=70, color=0xFFFFFF, font=FONT_MONT_14, parent=None)
pres_val_label = M5Label('00.00 hPa', x=100, y=70, color=0x4c8cbf, font=FONT_MONT_14, parent=None)

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

# infinite loop
while True:
    # get temp, press and humi of locally connected sensor
    temp_value = env3_0.temperature
    press_value = env3_0.pressure
    humi_value = env3_0.humidity

    # display temp, press and humi on screen
    temp_val_label.set_text(str(temp_value) + ' C')
    # set color of temp value label based on temp value
    temp_val_label.set_text_color(temp_to_color(temp_value))

    hum_val_label.set_text(str(humi_value) + ' %')
    pres_val_label.set_text(str(press_value) + ' hPa')

    # wait 10 ms, so the loop runs 100 times per second, prefent the screen from flickering and other issues
    wait_ms(10)


  