import RPi.GPIO as GPIO
import time
from datetime import datetime
import json
import os 




class DateTimeEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, datetime):
      return o.isoformat()
    return json.JSONEncoder.default(self,o)




i = 0

while(1==1):
  try:

    time.sleep(1)
    GPIO.setmode(GPIO.BCM)

    TRIG = 23 
    ECHO = 24

    print "Distance Measurement In Progress"

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)
    print "Waiting For Sensor To Settle"
    #time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)


    GPIO.setmode(GPIO.BCM)
    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    time_distance = datetime.now()
    print "Time:", time_distance, "Distance:",distance,"cm"

    #dump json file
    dic = {'time':time_distance, 'distance':distance}

    while os.path.exists("Dis_log%s.json" % i):
      i = i+1

    fh = open("Dis_log%s.json" % i, "w")

    json.dump(dic, fh, cls=DateTimeEncoder)

    print "i=",i,dic
    
    GPIO.cleanup()

  except ValueError:
    
    print "Error"
