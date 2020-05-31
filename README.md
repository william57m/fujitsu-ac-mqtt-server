# MQTT Server to communicate with Arduino

This server allow to send command to [Fujitsu AC Remote for Arduino](https://github.com/william57m/fujitsu-ac-arduino)

## MQTT Commands

Here is the list of command to publish to set the state of the AC.

| topic                  | payload                        | description
|------------------------|--------------------------------|---------------
| fujiac/mode/set        | auto, cool, dry, fan, off      | Set the master mode
| fujiac/fan/set         | auto, high, medium, low, quiet | Set the fan mode
| fujiac/temperature/set | 18 to 30                       | Set the temperature
| fujiac/airclean/set    | (Empty)                        | Toggle airclean mode
| fujiac/swing/set       | (Empty)                        | Toggle swing mode
| fujiac/wing/set        | (Empty)                        | Set the wing position

On each of these commands, the server publish `fujiac/state/get` to return the state of the AC, the message contains a JSON object.

Example of status payload
```json
{"temperature": 25, "mode": "off", "fan_mode": "quiet", "swing": "off", "air_clean": false}
```
