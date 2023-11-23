import httplib, urllib
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Define GPIO to use on Pi
GPIO_TRIGGER = 16 ##connect with RPI16
GPIO_ECHO    = 18 ##connect with RPI18

print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.5)

while True:
      # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()

    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()

# Calculate pulse length
    elapsed = stop-start

# Distance pulse travelled in that time is time
# multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300

# That was the distance there and back so halve the value
    distance = distance / 2

    print "Distance : %.1f" % distance
    time.sleep(1)
# Reset GPIO settings
#GPIO.cleanup()
    params = urllib.urlencode({'field1': distance, 'key':'BVGM6HX6XHZ4TI8J'}) 
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        conn.close()
    except:
        print "connection failed"


