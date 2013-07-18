from streamclient import StreamClient
import json
import time
host = '10.1.95.75'
port = 21567

sc = StreamClient(host, port)
## get the calue current stored in key slam/test
value = sc.get('slam/spikes')
print value

## set a new value in the key slam/test, then retrieve to verify
#sc.set('slam/test', 'world')
#for i in range(100):
   #value = sc.get('slam/test')
   #print json.dumps(value)
   #time.sleep(0.1)

## create a dictionary of velocities, then encode as json, store, and retrieve
#data = {'vx': 1, 'vy': 2, 'vr': 0}
#json_value = json.dumps(data)
#print json_value
#sc.set('slam/robot/commands.json', json_value)

#value = sc.get('slam/robot/commands.json')
#new_data = json.loads(value)
#print new_data
