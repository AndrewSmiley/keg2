import RPi.GPIO as GPIO
import time
from time import sleep

FLOW_PIN=4

pulse_count = 0
calibrationFactor = 4.5
litersPoured = 0.0
flowMilliLitres = 0.0
hertz = 0.0

import RPi.GPIO as GPIO  

GPIO.setmode(GPIO.BCM)  

GPIO.setup(14, GPIO.OUT)
GPIO.setup(FLOW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

old_time = 0.0

def increment_count(channel):  
	global pulse_count
	pulse_count = pulse_count + 1
	print pulse_count	  
  
GPIO.add_event_detect(FLOW_PIN, GPIO.FALLING, callback=increment_count, bouncetime=300)    
  
try:  
	while True:

		if((time.time()*1000)-old_time) > 2000:
			#flow_rate = ((1000.0 / (time.time()*1000) - old_time) * pulse_count) / calibrationFactor
			
			if pulse_count != 0:
				hertz = 1000.0000 / pulse_count
			else:
				hertz = 0
			flow_rate = hertz / (60 * 7.5)
			litersPoured += flow_rate * (pulse_count / 1000.0000)
			print litersPoured

			global pulse_count
			pulse_count = 0

			old_time = time.time() * 1000

			#flowMilliLitres = (flow_rate / 60) * 1000
			#totalMilliLitres = totalMilliLitres + flowMilliLitres
						
			
					

		GPIO.output(14, GPIO.LOW)
  
except KeyboardInterrupt:  
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

GPIO.cleanup()           # clean up GPIO on normal exit  
