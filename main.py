import network
import socket
import select
import ujson
from picozero import RGBLED
from time import sleep, time
from machine import Pin, PWM
from servo import Servo

sg90_servo = Servo(pin=10)
pos_servo = 90
sg90_servo.move(pos_servo)

# 1---3  1---2
# |   |  |   |
# 7---5  4---3  

in1 = Pin(15, Pin.OUT)
in2 = Pin(14, Pin.OUT)
in3 = Pin(4, Pin.OUT)
in4 = Pin(5, Pin.OUT)
in5 = Pin(7, Pin.OUT)
in6 = Pin(6, Pin.OUT)
in7 = Pin(8, Pin.OUT)
in8 = Pin(9, Pin.OUT)

Vmoteur1 = Pin(17, Pin.OUT)
Vmoteur2 = Pin(19, Pin.OUT)
Vmoteur3 = Pin(20, Pin.OUT)
Vmoteur4 = Pin(21, Pin.OUT)

ledR = Pin(1, Pin.OUT)
ledG = Pin(2, Pin.OUT)
ledB = Pin(3, Pin.OUT)

pwm_motor1 = PWM(Vmoteur1)
pwm_motor2 = PWM(Vmoteur2)
pwm_motor3 = PWM(Vmoteur3)
pwm_motor4 = PWM(Vmoteur4)




def VitesseMoteur(duty_cycle_motor1,duty_cycle_motor2,duty_cycle_motor3,duty_cycle_motor4):
    pwm_motor1.freq(1000)
    pwm_motor2.freq(1000)
    pwm_motor3.freq(1000)
    pwm_motor4.freq(1000)
    
    pwm_motor1.duty_u16(int(duty_cycle_motor1 * 65535 / 255))
    pwm_motor2.duty_u16(int(duty_cycle_motor2 * 65535 / 255))
    pwm_motor3.duty_u16(int(duty_cycle_motor3 * 65535 / 255))
    pwm_motor4.duty_u16(int(duty_cycle_motor4 * 65535 / 255))
    
VitesseMoteur(220,220,220,220)

button = Pin(18, Pin.IN, Pin.PULL_UP)

ledG.value(1)

ssid = 'Livebox-3E91'
password = 'DtfcVx43NzvZh6L5Hv'

box = 0
gu = 1

sleep(0.5)
ledG.value(0)
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        ledB.value(1)
        sleep(0.1)
        ledB.value(0)
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    ledB.value(0)
    ledG.value(1)
    sleep(1)
    ledG.value(0)
    sleep(1)
    ledG.value(1)
    sleep(1)
    ledG.value(0)
    return ip

def server():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 5000))
    print("starting")
    
    while True:
        
        data, addr = udp_socket.recvfrom(1024)
        command = ujson.loads(data.decode())
       
        
        for motor_name, motor_details in command.items():
            direction = motor_details['direction']
            speed = motor_details['speed']
            
            
            #speed_str1 = f"{speed}"
            #speed_numeric1 = int(speed_str1)
            #vmo = speed_numeric1
            #VitesseMoteur(vmo,vmo,vmo,vmo)
                       
            if (f"{motor_name}") == "motor1" and (f"{direction}") == '1':
                in1.value(1)
                
            elif (f"{motor_name}") == "motor1" and (f"{direction}") == '2':
                in2.value(1)
             
            elif (f"{motor_name}") == "motor1" and (f"{direction}") == '0':
                in1.value(0)
                in2.value(0)
              
                
                
            if (f"{motor_name}") == "motor2" and (f"{direction}") == '1':
                in3.value(1)
          
            elif (f"{motor_name}") == "motor2" and (f"{direction}") == '2':
                in4.value(1)
               
                
            elif (f"{motor_name}") == "motor2" and (f"{direction}") == '0':
                in3.value(0)
                in4.value(0)
              
                
                
                
            if (f"{motor_name}") == "motor3" and (f"{direction}") == '1':
                in5.value(1)
                
            elif (f"{motor_name}") == "motor3" and (f"{direction}") == '2':
                in6.value(1)
              
            elif (f"{motor_name}") == "motor3" and (f"{direction}") == '0':
                in5.value(0)
                in6.value(0)
        
                
                
            if (f"{motor_name}") == "motor4" and (f"{direction}") == '1':
                in7.value(1)
         
            elif (f"{motor_name}") == "motor4" and (f"{direction}") == '2':
                in8.value(1)
              
            elif (f"{motor_name}") == "motor4" and (f"{direction}") == '0':
                in7.value(0)
                in8.value(0)

              



ip = connect()
server()





