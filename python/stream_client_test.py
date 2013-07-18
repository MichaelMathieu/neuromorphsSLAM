from streamclient import StreamClient
import json
import time
host = '10.1.95.75'
port = 21567
print "going to start client"
sc = StreamClient(host, port)
print "started"
## get the calue current stored in key slam/test
#value = sc.get('slam/spikes')
#print value

## set a new value in the key slam/test, then retrieve to verify
sc.set('slam/velocity', 'will set this')
print "set velocity"
for i in range(1000):
   value = sc.get('slam/velocity')
   print value
   time.sleep(0.1)
   t = i % 10 + 1
   spikes = json.dumps([int(j % t == 0) for j in range(100)])
   print spikes
   sc.set('slam/spikes', spikes)
## create a dictionary of velocities, then encode as json, store, and retrieve
#data = {'vx': 1, 'vy': 2, 'vr': 0}
#json_value = json.dumps(data)
#print json_value
#sc.set('slam/robot/commands.json', json_value)

#value = sc.get('slam/robot/commands.json')
#new_data = json.loads(value)
#print new_data
