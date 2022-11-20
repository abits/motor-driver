"""
  Control DC motor using Maker Drive and CircuitPython on RP2040.
  
  Items:
  – Maker Nano RP2040
    https://my.cytron.io/maker-nano-rp2040-simplifying-projects-with-raspberry-pi-rp2040
  – Maker Drive
    https://my.cytron.io/p-maker-drive-simplifying-h-bridge-motor-driver-for-beginner
  – Shield for Arduino Nano
    https://my.cytron.io/p-io-expansion-shield-for-arduino-nano
  – TT Gear Motor
    https://my.cytron.io/p-3v-6v-dual-axis-tt-gear-motor
  – LiPo Battery 7.4V 450mAH
    https://my.cytron.io/p-lipo-battery-7.4v-450mah
  – JST RCY Receptacle
    https://my.cytron.io/p-jst-rcy-receptacle-with-wire-15cm
  – 3D Printing products
    https://my.cytron.io/c-3d-modeling
    
  Libraries required from bundle (https://circuitpython.org/libraries):
  – adafruit_motor
  
  References:
  – https://learn.adafruit.com/circuitpython-essentials/circuitpython-pwm
  
  Last update: 15 Feb 2022
"""

import time
import board
import digitalio
import pwmio
from adafruit_motor import motor

PWM_M1A = board.GP2  # pick any pwm pins on their own channels
PWM_M1B = board.GP3
PWM_M2A = board.GP4  # pick any pwm pins on their own channels
PWM_M2B = board.GP5
PWM_FREQ = 10000  # Custom PWM frequency; Crickit min/max 3Hz/720Hz, default is 50Hz
DECAY_MODE = motor.SLOW_DECAY  # Set controller to Slow Decay (braking) mode
THROTTLE_HOLD = 1  # Hold the throttle (seconds)

# DC motor setup
# DC Motors generate electrical noise when running that can reset the microcontroller in extreme
# cases. A capacitor can be used to help prevent this.
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=PWM_FREQ)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=PWM_FREQ)
motor1 = motor.DCMotor(pwm_1a, pwm_1b)
pwm_2a = pwmio.PWMOut(PWM_M2A, frequency=PWM_FREQ)
pwm_2b = pwmio.PWMOut(PWM_M2B, frequency=PWM_FREQ)
motor2 = motor.DCMotor(pwm_2a, pwm_2b)
 
for duty_cycle in range(0, 101, 2):
    throttle = duty_cycle / 100  # Convert to throttle value (0 to 1.0)
    motor1.throttle = throttle
    motor2.throttle = throttle
    print('Motor speed: {}%'.format(throttle*100))
    time.sleep(THROTTLE_HOLD)  # Hold at current throttle value

motor1.throttle = 0  # Stop motor1
motor2.throttle = 0  # Stop motor2
print('Motor speed: {}%'.format(throttle*100))
time.sleep(THROTTLE_HOLD)  # Hold at current throttle value
 
 
# while True:
#     while speed < 1:
#         print("Motor speed: {}".format(speed))
#         motor1.throttle = speed
#         speed += 0.01
#         time.sleep(0.05)

#     speed = 1
#     while speed > –1:
#         print("Motor speed: {}".format(speed))
#         motor1.throttle = speed
#         speed -= 0.01
#         time.sleep(0.05)

#     speed = –1
#     while speed < 0:
#         print("Motor speed: {}".format(speed))
#         motor1.throttle = speed
#         speed += 0.01
#         time.sleep(0.05)

#     motor1.throttle = 0
    