import RPi.GPIO as GPIO
import time
from datetime import datetime
import json
import os
from pytz import timezone 


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

from kafka import KafkaProducer
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),bootstrap_servers='54.229.182.18:9092')

elevator_id = 's-1'

#i = 0
while (1==1):
  try:

    time.sleep(3)
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

    time_1 = datetime.now(timezone('Europe/Amsterdam')).strftime('%Y-%m-%d %H:%M:%S %Z')

    dic = {'rec_time': time_1, 'distance': distance }

    producer.send('distances', {'elevator_id':elevator_id,'rec_time': time_1, 'distance': distance })


    print dic
    
    GPIO.cleanup()

  except ValueError:
    
    print "Error"




    # while os.path.exists("Dis_log%s.json" % i):
		# i += 1
    #
    # fh = open("Dis_log%s.json" % i, "w")
    #
    # json.dump(dic,fh, cls=DateTimeEncoder)
    # print "i:",i
    # print "dic:",dic





#
# from kafka import KafkaProducer
# producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),bootstrap_servers='uniutrecht01.nine.ch:9092')
# producer.send('fizzbuzz', {'foo': 'bar'})
#
# from kafka import KafkaConsumer
# consumer = KafkaConsumer('fizzbuzz', bootstrap_servers='uniutrecht01.nine.ch:9092')
# for msg in consumer:
# 	print (msg)
