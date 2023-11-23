#RPi GPIO configuration
import RPi.GPIO as GPIO
import time

#RPi input/output configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

while True:


        #Relay1 ON
        GPIO.output(38, 1)
        GPIO.output(36, 1)
        GPIO.output(40, 1)
        time.sleep(3)

        #Relay1 OFF
        GPIO.output(38, 0)
        GPIO.output(36, 0)
        GPIO.output(40, 0)
        time.sleep(3)

