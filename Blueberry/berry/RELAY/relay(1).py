#RPi GPIO configuration
import RPi.GPIO as GPIO
import time

#RPi input/output configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT)
while True:


        #Relay1 ON
        GPIO.output(36, 1)
        time.sleep(4)

        #Relay1 OFF
        GPIO.output(36, 0)
        time.sleep(4)
