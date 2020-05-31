import json
import paho.mqtt.client as mqtt
import re
import syslog

from fuji import FujiAC

# MQTT Settings
mqtt_host = 'localhost'
mqtt_port = 1883


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('fujiac/#')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

  print(f'Received: {msg.topic} / Message: {msg.payload.decode("utf-8")}')
  syslog.syslog(f'Received: {msg.topic} / Message: {msg.payload.decode("utf-8")}')

  # Command to trigger publish update
  if msg.topic == 'fujiac/state/send':
    state = ac.get_state()
    client.publish('fujiac/state/get', json.dumps(state))

  # Update settings
  if msg.topic == 'fujiac/mode/set':
    ac.set_mode(msg.payload.decode('utf-8'))
  elif msg.topic == 'fujiac/fan/set':
    ac.set_fan_mode(msg.payload.decode('utf-8'))
  elif msg.topic == 'fujiac/temperature/set':
    ac.set_temperature(int(float(msg.payload)))
  elif msg.topic == 'fujiac/swing/set':
    ac.toggle_swing()
  elif msg.topic == 'fujiac/airclean/set':
    ac.toggle_airclean()
  elif msg.topic == 'fujiac/wing/set':
    ac.set_wing()
  elif msg.topic == 'fujiac/reset/set':
    ac.reset()

  # Publish update
  if re.match(r'fujiac/.*/set', msg.topic):
    state = ac.get_state()
    client.publish('fujiac/state/get', json.dumps(state))

# Init AC
ac = FujiAC()

# Init MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_host, mqtt_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
