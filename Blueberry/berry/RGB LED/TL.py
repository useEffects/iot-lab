from gpiozero import LED
red=LED(22)
amber=LED(27)
green=LED(17)

red.blink(1,1)
amber.blink(2,2)
green.blink(3,3)

