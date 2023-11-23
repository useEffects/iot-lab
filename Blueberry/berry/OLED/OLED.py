
import time

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Raspberry Pi pin configuration:
RST = 24

# Note you can change the I2C address by passing an i2c_address parameter like:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Initialize library.
disp.begin()
ImageDraw
# Clear display.
disp.clear()
disp.display()



#Create blank image for drawing.
#Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
print(width,height)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
### First define some constants to allow easy resizing of shapes.
padding = 28

top = padding


# Move left to right keeping track of the current x position for drawing shapes.
x = padding

# Load default font.
font = ImageFont.load_default()

#Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
#Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Minecraftia.ttf', 8)

#Write two lines of text.S
a = 'hello'
draw.text((x+10, top), a , font=font,fill=1, )


#Display image.
disp.image(image)
disp.display()
time.sleep(5)




