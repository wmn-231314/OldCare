# -*- coding: utf-8 -*-
'''
摄像头舵机
'''

'''
servo brand: SG90  (Micro Servo 99)
camera servo (left right) connects to pwm1
camera servo (up down) connects to pwm2

expectation (need to verify): 
0 degree: (0.5 * 1000 * 50 * 4096)/1000000 = 102.4
30 degree: ((30/90.+0.5) * 1000 * 50 * 4096)/1000000 = 170.6
90 degree: (1.5 * 1000 * 50 * 4096)/1000000 = 307.2
100 degree: (1.61 * 1000 * 50 * 4096)/1000000 = 329.728
180 degree: (2.5 * 1000 * 50 * 4096)/1000000 = 512
'''

import sys  
sys.path.append('adafruit')
from Adafruit_MotorHAT.Adafruit_PWM_Servo_Driver import PWM
import RPi.GPIO as GPIO
import time

# left right rotate camera servo
class LRCameraServo():
    pwm_pin = 1
    last_angle = -1
    
    def __init__(self):
        self.setup()
    
    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.pwm = PWM(0x40,debug = False)
        self.pwm.setPWMFreq(50) # 50 full 'pulses' per second
        
        self.front() # calibration

    def setServoPulse(self, pulse_width):
        # pulse: 1ms, range:[0.5, 2.5]
        pulseLength = 1000000.0 # 1,000,000 us per second
        pulseLength /= 50.0 # 50 Hz
        #print("%d us per period" % pulseLength)
        pulseLength /= 4096.0 # 12 bits of resolution
        #print("%d us per bit" % pulseLength)
        pulse_width *= 1000.0
        pulse_width /= (pulseLength*1.0)
        #print("pluse: %f  " % (pulse_width))
        self.pwm.setPWM(self.pwm_pin, 0, int(pulse_width))
    
    # turn servo
    # angle to pulse width
    def turn_servo(self, angle):
        pulse_width = angle/90.0+0.5
        pulse_width = max(pulse_width,0.5)
        pulse_width = min(pulse_width,2.5)
        self.setServoPulse(pulse_width)
    
    # turn left (angle is based on front)
    def turn_right_servo_test(self, angle):
        angle = 90 - angle
        self.turn_servo(angle)
    
    # turn right ((angle is based on front))
    def turn_left_servo_test(self, angle):
        angle = 90 + angle
        self.turn_servo(angle)
    
    # front
    def front(self):
        self.last_angle = 90
        self.turn_servo(90)
    
    # turn left based on last angle
    def turn_right_servo(self, angle):
        real_angle = self.last_angle - angle
        self.turn_servo(real_angle)
        self.last_angle = real_angle
    
    # turn right based on last angle
    def turn_left_servo(self, angle):
        real_angle = self.last_angle + angle
        self.turn_servo(real_angle)
        self.last_angle = real_angle
        
    def destroy(self):
        self.pwm = None
        GPIO.cleanup()



# up down rotate camera servo
class UDCameraServo():
         
    def destroy(self):
        self.pwm = None
        GPIO.cleanup()

'''       
if __name__ == "__main__":
    lrservo = LRCameraServo()
    time.sleep(1)
    
    for i in range(5, 91, 5):
        print(i)
        lrservo.turn_right_servo_test(i)
        time.sleep(1)
    
'''
if __name__ == "__main__":
    lrservo = LRCameraServo()
    time.sleep(3)
    lrservo.turn_left_servo(30)
    time.sleep(2)
    lrservo.turn_left_servo(10)
    time.sleep(2)
    lrservo.turn_right_servo(40)



    