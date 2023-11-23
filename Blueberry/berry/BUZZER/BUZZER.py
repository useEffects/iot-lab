#1541245mcp23017 library path
import sys
sys.path.append('/home/pi/Adafruit-Raspberry-Pi-Python-Code-legacy/Adafruit_MCP230xx')
from Adafruit_MCP230XX import Adafruit_MCP230XX
import time

#mcp IC configuration
mcp = Adafruit_MCP230XX(busnum = 1, address = 0x20, num_gpios = 16) # MCP23017

#mcp input/output configuration
mcp.config(11, mcp.OUTPUT)


while True:
    n = input("Enter the number : ")
    while(n>0):
        mcp.output(11, 1)
        time.sleep(0.1)
        print("Beep sound");
        mcp.output(11, 0)
        time.sleep(0.1)
        n = n-1
    break;
   
  

   
