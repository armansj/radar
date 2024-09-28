import network
import socket
import time
from machine import Pin, PWM, time_pulse_us
import _thread

TRIG_PIN = 13
ECHO_PIN = 14
SERVO_PIN = 15
BUZZER_PIN = 16

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
servo = PWM(Pin(SERVO_PIN))
buzzer = PWM(Pin(BUZZER_PIN))

servo.freq(50)

ssid = 'Vodafone-820C'
password = 'xc5dadQYrqpo2J2sd2q2'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    time.sleep(1)

ip_address = wlan.ifconfig()[0]
print('Connected to Wi-Fi. IP Address:', ip_address)


def get_distance():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    duration = time_pulse_us(echo, 1)
    distance = (duration / 2) / 29.1
    return distance


def set_servo_angle(angle):
    duty = int((angle / 180 * 2000) + 500)
    servo.duty_u16(duty)


def sound_buzzer(frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty_u16(32767)
    time.sleep(duration)
    buzzer.duty_u16(0)


def handle_request(request):
    angle = float(request.get('angle', 0))
    distance = get_distance()

    response = f'{{"angle": {angle}, "distance": {distance:.2f}}}'
    return response


def run_server():
    addr = socket.getaddrinfo('0.0.0.0', 12345)[0][-1]  # Use port 12345
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('Listening on', addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        if request:
            request = str(request)
            print("Request:", request)
            angle = 0
            response = handle_request({'angle': angle})
            cl.send('HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n')
            cl.send(response)
        cl.close()


def radar_system():
    beep_interval = 1
    last_beep_time = time.time()

    while True:
        for angle in range(0, 181, 5):
            set_servo_angle(angle)
            time.sleep(0.1)

            distance = get_distance()

            if distance < 30:
                sound_buzzer(1000, 0.1)
            else:
                current_time = time.time()
                if current_time - last_beep_time >= beep_interval:
                    sound_buzzer(1000, 0.05)
                    last_beep_time = current_time

        for angle in range(180, -1, -5):
            set_servo_angle(angle)
            time.sleep(0.1)

            distance = get_distance()

            if distance < 30:
                sound_buzzer(1000, 0.1)
            else:
                current_time = time.time()
                if current_time - last_beep_time >= beep_interval:
                    sound_buzzer(1000, 0.05)
                    last_beep_time = current_time


_thread.start_new_thread(radar_system, ())

run_server()


