#mcp23017 library path
import sys
sys.path.append('/home/pi/Adafruit-Raspberry-Pi-Python-Code-legacy/Adafruit_MCP230xx')
from Adafruit_MCP230XX import Adafruit_MCP230XX
import time

#mcp IC configuration
mcp = Adafruit_MCP230XX(busnum = 1, address = 0x20, num_gpios = 16) # MCP23017

mcp.config(0, mcp.OUTPUT)
mcp.config(1 , mcp.OUTPUT)
mcp.config(2 , mcp.OUTPUT)
mcp.config(3 , mcp.OUTPUT)
mcp.config(4 , mcp.OUTPUT)
mcp.config(5 , mcp.OUTPUT)
mcp.config(6 , mcp.OUTPUT)
mcp.config(7 , mcp.OUTPUT)
mcp.config(8, mcp.OUTPUT)

while True:
           #RGB LED blink
        mcp.output(0, 1)
        time.sleep(1)
        mcp.output(0, 0)
        time.sleep(1)
        
        mcp.output(3,1)
        mcp.output(4,1)
        time.sleep(1)
        mcp.output(3,0)
        mcp.output(4,0)
        time.sleep(1)
        
        mcp.output(7,1)
        time.sleep(1)
        mcp.output(7,0)
        time.sleep(1)

