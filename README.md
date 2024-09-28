# Radar System with Ultrasonic Sensor and Servo Control

This project implements a radar system using an ultrasonic sensor to measure distances and a servo motor to sweep the sensor. The system can sound a buzzer based on detected distances and serve the data over an HTTP server.

## Demo
You can find a demo of the radar system in action on Instagram: [Radar System Demo](https://www.instagram.com/reel/C-TL1KoA7sr/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)

## Requirements
- Microcontroller with MicroPython support (rasperry pi pico w)
- Ultrasonic sensor (HC-SR04)
- Servo motor
- Buzzer (preferably a piezo buzzer)
- Required libraries for MicroPython

## Pin Configuration
| Component        | Pin Number |
|------------------|------------|
| Ultrasonic TRIG  | 13         |
| Ultrasonic ECHO  | 14         |
| Servo            | 15         |
| Buzzer           | 16         |

## Wi-Fi Configuration
Replace the `ssid` and `password` variables in the code with your Wi-Fi credentials:
```python
ssid = 'Your_SSID'
password = 'Your_Password'
