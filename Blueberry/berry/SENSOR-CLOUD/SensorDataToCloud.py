# ----------------------------------------------
# Application example developed by
# Enthu Technology solutions india Pvt Ltd
#-----------------------------------------------

# SensorDataToCloud
# This application updates environmental datas(Pressure,Humidity,Temperature to cloud)

#OLED Display configuration
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
RST = 24

import smbus
import time
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte
import httplib, urllib

DEVICE = 0x76 # Default device I2C address


bus = smbus.SMBus(1) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
                     # Rev 1 Pi uses bus 0

# Note you can change the I2C address by passing an i2c_address parameter like:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Initialize library.
disp.begin()
disp.clear()
disp.display()

#Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
### First define some constants to allow easy resizing of shapes.
padding = 2
shape_width = 20
top = padding
bottom = height-padding

# Move left to right keeping track of the current x position for drawing shapes.
x = padding

# Load default font.
#font = ImageFont.load_default()
font = ImageFont.truetype('FreeSans.ttf', 13)

#Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
#Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Minecraftia.ttf', 8)

#Write two lines of text.
draw.text((1, 1), str(datetime.now().strftime('%a  %b  %d  %H:%M:%S')), font=font, fill=1)
font = ImageFont.truetype('FreeSans.ttf', 11)
draw.text((x, top+20),    'Enthu',  font=font, fill=255)
draw.text((x, top+40), 'Technology!', font=font, fill=255)

#Display image.
disp.image(image)
disp.display()

def getShort(data, index):
  # return two bytes from data as a signed 16-bit value
  return c_short((data[index+1] << 8) + data[index]).value

def getUShort(data, index):
  # return two bytes from data as an unsigned 16-bit value
  return (data[index+1] << 8) + data[index]

def getChar(data,index):
  # return one byte from data as a signed char
  result = data[index]
  if result > 127:
    result -= 256
  return result

def getUChar(data,index):
  # return one byte from data as an unsigned char
  result =  data[index] & 0xFF
  return result

def readBME280ID(addr=DEVICE):
  # Chip ID Register Address
  REG_ID     = 0xD0
  (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
  return (chip_id, chip_version)

def readBME280All(addr=DEVICE):
  # Register Addresses
  REG_DATA = 0xF7
  REG_CONTROL = 0xF4
  REG_CONFIG  = 0xF5

  REG_CONTROL_HUM = 0xF2
  REG_HUM_MSB = 0xFD
  REG_HUM_LSB = 0xFE

  # Oversample setting - page 27
  OVERSAMPLE_TEMP = 2
  OVERSAMPLE_PRES = 2
  MODE = 1

  # Oversample setting for humidity register - page 26
  OVERSAMPLE_HUM = 2
  bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)

  control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
  bus.write_byte_data(addr, REG_CONTROL, control)

  # Read blocks of calibration data from EEPROM
  # See Page 22 data sheet
  cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
  cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
  cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)

  # Convert byte data to word values
  dig_T1 = getUShort(cal1, 0)
  dig_T2 = getShort(cal1, 2)
  dig_T3 = getShort(cal1, 4)

  dig_P1 = getUShort(cal1, 6)
  dig_P2 = getShort(cal1, 8)
  dig_P3 = getShort(cal1, 10)
  dig_P4 = getShort(cal1, 12)
  dig_P5 = getShort(cal1, 14)
  dig_P6 = getShort(cal1, 16)
  dig_P7 = getShort(cal1, 18)
  dig_P8 = getShort(cal1, 20)
  dig_P9 = getShort(cal1, 22)

  dig_H1 = getUChar(cal2, 0)
  dig_H2 = getShort(cal3, 0)
  dig_H3 = getUChar(cal3, 2)

  dig_H4 = getChar(cal3, 3)
  dig_H4 = (dig_H4 << 24) >> 20
  dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)

  dig_H5 = getChar(cal3, 5)
  dig_H5 = (dig_H5 << 24) >> 20
  dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)

  dig_H6 = getChar(cal3, 6)

  # Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
  wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
  time.sleep(wait_time/1000)  # Wait the required time  

  # Read temperature/pressure/humidity
  data = bus.read_i2c_block_data(addr, REG_DATA, 8)
  pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
  temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
  hum_raw = (data[6] << 8) | data[7]

  #Refine temperature
  var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
  var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
  t_fine = var1+var2
  temperature = float(((t_fine * 5) + 128) >> 8);

  # Refine pressure and adjust for temperature
  var1 = t_fine / 2.0 - 64000.0
  var2 = var1 * var1 * dig_P6 / 32768.0
  var2 = var2 + var1 * dig_P5 * 2.0
  var2 = var2 / 4.0 + dig_P4 * 65536.0
  var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
  var1 = (1.0 + var1 / 32768.0) * dig_P1
  if var1 == 0:
    pressure=0
  else:
    pressure = 1048576.0 - pres_raw
    pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
    var1 = dig_P9 * pressure * pressure / 2147483648.0
    var2 = pressure * dig_P8 / 32768.0
    pressure = pressure + (var1 + var2 + dig_P7) / 16.0

  # Refine humidity
  humidity = t_fine - 76800.0
  humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
  humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
  if humidity > 100:
    humidity = 100
  elif humidity < 0:
    humidity = 0

  return temperature/100.0,pressure/100.0,humidity

def main():

  (chip_id, chip_version) = readBME280ID()
  temperature,pressure,humidity = readBME280All()

if __name__=="__main__":
   main()
while True:
  
    #read sensor data
    (chip_id, chip_version) = readBME280ID()
    print "Chip ID     :", chip_id
    print "Version     :", chip_version

    temperature,pressure,humidity = readBME280All()
    print "Temperature : ", temperature, "C"
    print "Pressure : ", pressure, "hPa"
    print "Humidity : ", humidity, "%"

    #Print OLED display
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    font = ImageFont.truetype('FreeSans.ttf', 13)
    draw.text((1, 1), str(datetime.now().strftime('%a  %b  %d  %H:%M:%S')), font=font, fill=1)
    font = ImageFont.truetype('FreeSans.ttf', 11)
    draw.text((x, top+15),    'Temperature: %.2f C'%temperature,  font=font, fill=1)
    draw.text((x, top+30), 'pressure: %.2f hpa'%pressure, font=font, fill=1)
    draw.text((x, top+45), 'humidity: %.2f%%'%humidity, font=font, fill=1)
    disp.image(image)
    disp.display()
    time.sleep(3)


    #upload to cloud
    params = urllib.urlencode({'field1': temperature, 'field2': pressure, 'field3': humidity, 'key':'VHC1XELRVWSR1OXF'}) 
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")

    #Print OLED display
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    font = ImageFont.truetype('FreeSans.ttf', 13)
    draw.text((1, 1), str(datetime.now().strftime('%a  %b  %d  %H:%M:%S')), font=font, fill=1)
    font = ImageFont.truetype('FreeSans.ttf', 11)
    draw.text((x, top+15),    'Connecting...',  font=font, fill=1)
    draw.text((x, top+30), '       To...', font=font, fill=1)
    draw.text((x, top+45), 'Cloud...', font=font, fill=1)
    disp.image(image)
    disp.display()
    time.sleep(3)
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        conn.close()
    except:
        print "connection failed"
  

