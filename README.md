# MQTT Server to communicate with Arduino

This server allow to send command to [Fujitsu AC Remote for Arduino](https://github.com/william57m/fujitsu-ac-arduino)

## Regular installation

Clone the repository
```bash
git clone git@github.com:william57m/fujitsu-ac-mqtt-server.git
cd fujitsu-ac-mqtt-server
```

Install the requirements
```
pip install -r requirements.txt
```

Run it as a service
```bash
sudo sh ./setup.sh
sudo systemctl start fujiac.service
```

Run it manually
```bash
python3 src/server.py
```

## Installation with docker

Run with docker
```
docker run \
  --device /dev/gpiomem \
  -e MQTT_HOST='192.168.2.110' \
  william57m/fujiac-mqtt-server:latest
```

## Build and publish

Build
```
docker build --tag william57m/fujiac-mqtt-server .
```

Deploy
```
docker push william57m/fujiac-mqtt-server
```

## MQTT Commands

Here is the list of command to publish to set the state of the AC.

| topic                  | payload                        | description                |
|------------------------|--------------------------------|-----------------------------
| fujiac/mode/set        | auto, cool, dry, fan, off      | Set the master mode        |
| fujiac/fan/set         | auto, high, medium, low, quiet | Set the fan mode           |
| fujiac/temperature/set | 18 to 30                       | Set the temperature        |
| fujiac/airclean/set    | (Empty)                        | Toggle airclean mode       |
| fujiac/swing/set       | (Empty)                        | Toggle swing mode          |
| fujiac/wing/set        | (Empty)                        | Set the wing position      |
| fujiac/reset/set       | (Empty)                        | Reset the state of the AC  |

On each of these commands, the server publish `fujiac/state/get` to return the state of the AC, the message contains a JSON object.

Example of status payload
```json
{"temperature": 25, "mode": "off", "fan_mode": "quiet", "swing": "off", "air_clean": false}
```
