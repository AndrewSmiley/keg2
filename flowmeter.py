import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
pouring = False
lastPinState = False
pinState = 0
lastPinChange = int(time.time() * 1000)
pourStart = 0
pinChange = lastPinChange
pinDelta = 0
hertz = 0
flow = 0
litersPoured = 0
pintsPoured = 0
# main loop
while True:
  currentTime = int(time.time() * 1000)
  if GPIO.input(23):
    pinState = True
    print "well we're reading something.."
  else:
    pinState = False
# If we have changed pin states low to high...
  if(pinState != lastPinState and pinState == True):
    print "we are pouring"
    if(pouring == False):
      pourStart = currentTime
    pouring = True
    # get the current time
    pinChange = currentTime
    pinDelta = pinChange - lastPinChange
    if (pinDelta < 1000):
      # calculate the instantaneous speed
      hertz = 1000.0000 / pinDelta
      flow = hertz / (60 * 7.5) # L/s
      litersPoured += flow * (pinDelta / 1000.0000)
      print "liters poured: %s" %(litersPoured)
      pintsPoured = litersPoured * 2.11338
    if (pouring == True and pinState == lastPinState and (currentTime - lastPinChange) > 3000):
        # set pouring back to false, tweet the current amt poured, and reset everything
        pouring = False
        if (pintsPoured > 0.1):

            pourTime = int((currentTime - pourStart)/1000) - 3
            print 'Someone just poured ' + str(round(pintsPoured,2)) + ' pints of root beer in ' + str(pourTime) + ' seconds'
            litersPoured = 0
            pintsPoured = 0
