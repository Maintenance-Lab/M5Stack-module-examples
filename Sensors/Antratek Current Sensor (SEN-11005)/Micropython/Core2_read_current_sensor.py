from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
import machine
import wifiCfg
import _thread

# Connect to WiFi
wifiCfg.autoConnect(lcdShow=True)

# Set the correct time
rtc.settime('ntp', host='de.pool.ntp.org', tzone=2)

# Initialize M5Stack
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

# Initialize ADC
# Pin number (36) is an ADC pin (https://randomnerdtutorials.com/esp32-pinout-reference-gpios/)
# This pin is available on the Bottom2 (https://docs.m5stack.com/en/base/m5go_bottom2)
# Wire the current sensor according to the voltage divider circuit from this tutorial https://learn.sparkfun.com/tutorials/environmental-monitoring-with-the-tessel-2
adc_0 = machine.ADC(36)
adc_0.width(machine.ADC.WIDTH_10BIT)
adc_0.atten(machine.ADC.ATTN_11DB)

# Initialize variables for the current sensor
supply_voltage = 5000 # in mV
number_of_samples = 2000 
ADC_counts = 1<<10 # Left shift by the ADC width
offsetI = ADC_counts>>1 # Right shift by 1 to get the center value
current_sensor_list = [] # List to store the current sensor values

# Create labels
reset_label = M5Label('Reset', x=139, y=218, color=0xff0000, font=FONT_MONT_14, parent=None)
start_label = M5Label('Start', x=52, y=218, color=0x3aff00, font=FONT_MONT_14, parent=None)
stop_label = M5Label('Stop', x=234, y=218, color=0x004cff, font=FONT_MONT_14, parent=None)
title_label = M5Label('Primary Unit', x=18, y=15, color=0x000000, font=FONT_MONT_30, parent=None)
state_label = M5Label('State: Stopped', x=18, y=82, color=0x000, font=FONT_MONT_14, parent=None)
last_observation_label = M5Label('Last observation: None', x=18, y=105, color=0x000, font=FONT_MONT_14, parent=None)
last_observation_current_label = M5Label('Current: A, Power: W', x=18, y=128, color=0x000, font=FONT_MONT_14, parent=None)
error_label = M5Label('Error: None', x=18, y=151, color=0x000, font=FONT_MONT_14, parent=None)

def read_current_sensor():
    global offsetI
    try:
        sumI = 0
        for i in range(number_of_samples):
            if btnB.wasReleased():
                machine.reset()
            sampleI = adc_0.read()
            # Digital low pass filter extracts the 2.5 V offset
            # This is then subtracted to center the signal
            offsetI = offsetI + (sampleI - offsetI) / 1024
            filteredI = sampleI - offsetI
            # Root-mean-square method current
            squareI = filteredI * filteredI
            sumI = sumI + squareI
        
        I_ratio = 35 *((supply_voltage/1000.0) / (ADC_counts))
        I_rms = I_ratio * math.sqrt(sumI / number_of_samples)
        return I_rms
    except Exception as err:
        error_label.set_text(err)

def current_sensor_thread():
    global current_sensor_list
    # Continuously read the current sensor
    try:
        while not btnB.wasReleased():
            if state == 'running':
                current_sensor_list.append(read_current_sensor())
    except Exception as err:
        error_label.set_text(err)

# Start the thread
_thread.start_new_thread(current_sensor_thread, ())

# Initialize variables
state = 'stopped'
last_request = 0
request_time = 1000 # 10 seconds

while not btnB.wasReleased():
    if state == 'stopped':
        if btnA.wasReleased():
            state = 'running'
            state_label.set_text('State: Running')
            continue
    
    if state == 'running':
        if btnC.wasReleased():
            state = 'stopped'
            state_label.set_text('State: Stopped')
            continue

        current_time = time.ticks_ms()
        if current_time - last_request >= request_time:
            # Calculate current and power
            if len(current_sensor_list) > 0:
                current = sum(current_sensor_list) / len(current_sensor_list) # Retrieve the mean of the current sensor values
                power = current * 230
            else:
                current = 0
                power = 0
            
            # Get the current date and time
            dateTime = rtc.datetime() # (year, month, day, weekday, hours, minutes, seconds, subseconds)
            dateTimeString = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(dateTime[0], dateTime[1], dateTime[2], dateTime[4], dateTime[5], dateTime[6])

            # Set labels
            last_observation_label.set_text('Last observation: {}'.format(dateTimeString))
            last_observation_current_label.set_text('Current: {:.1f}A, Power: {:.1f}W'.format(current, power))
            
            # Set variables
            current_sensor_list = [] # Empty the current sensor list
            last_request = current_time

state_label.set_text('State: Resetting')
machine.reset()