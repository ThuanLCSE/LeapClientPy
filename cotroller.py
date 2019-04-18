import redis
import time
import traceback
import json
import IMTThalesLeap as Leap

REDIS_CHANNEL = 'leapthuan'
REDIS_HOST='127.0.0.1'
REDIS_PORT = 6379

            
def Subscriber():
    try:
        r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
        p = r.pubsub()                                                              
        p.subscribe(REDIS_CHANNEL)                                                 
        TRACKING = True
        print("---START OF SUBSCRIBING---")
        while TRACKING:
            
            message = p.get_message()
            if message:
                json_str = message['data']  
#To stop listening to Redis channel, send PUBLISH leapthuan stop via redis-cli,
#or halt the program with Ctrl+C
                if message['data'] == b'stop':                                             
                    TRACKING = False 
                elif isinstance(json_str, int):
                    print('int received ',json_str)
                else:
                    try :
                        multiLeap_data = json.loads(json_str)
                        i = 1
                        for sensor_dict in multiLeap_data['sensors']:
                            sensor = Leap.SensorFrame(sensor_dict) 
                            print('sensor ',i,' :')
                            i+=1
                            logHands(sensor)
                    except Exception as e:  
                        print(e) 
            time.sleep(0.2) #in second

        print("---END OF SUBSCRIBING---")

    except Exception as e: 
        print(str(e))
        print(traceback.format_exc())
 
def logBones(finger):
    print('logBones(finger)')
    for b in finger.getBones():
        print(b.width)
def logFingers(hand):
    print('logFingers(hand)')
    for f in hand.getFingers():
        print(f.length)
def logPointables(hand):
    print('logPointables(hand)')
    for p in hand.getPointables():
        print(p.width)
        
def logHands(sensor):
    print('logHands(sensor)') 
    for hand in sensor.getHands():
        print(hand)
        logFingers(hand)
        logPointables(hand)
        for finger in hand.getFingers():
            logBones(finger)
        
Subscriber()
 

