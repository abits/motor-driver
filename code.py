"""
  Control DC motor using Maker Drive and CircuitPython on RP2040.
"""

import time
import board
import digitalio
import pwmio
from adafruit_motor import motor
import rotaryio

PWM_M1A = board.GP2  # pick any pwm pins on their own channels
PWM_M1B = board.GP3
PWM_M2A = board.GP4  # pick any pwm pins on their own channels
PWM_M2B = board.GP5
PWM_FREQ = 10000  # Custom PWM frequency
DECAY_MODE = motor.SLOW_DECAY  # Set controller to Slow Decay (braking) mode
THROTTLE_HOLD = 5  # Hold the throttle (seconds)

# DC motor setup
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=PWM_FREQ)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=PWM_FREQ)
motor1 = motor.DCMotor(pwm_1a, pwm_1b)
# pwm_2a = pwmio.PWMOut(PWM_M2A, frequency=PWM_FREQ)
# pwm_2b = pwmio.PWMOut(PWM_M2B, frequency=PWM_FREQ)
# motor2 = motor.DCMotor(pwm_2a, pwm_2b)
 
# set up encoder
encoder = rotaryio.IncrementalEncoder(board.GP16, board.GP17)
motor1.throttle = 0.5
LAST_EVAL_TIME = -1
pos1 = -1
start_cycle = True
rpm = 0
measurements = 1
max_measurements = 10
LAST_EVAL_TIME = time.monotonic()

print(f"Polling motor speed in RPM every {THROTTLE_HOLD} seconds for {max_measurements} cycles.")
print(f"Motor is throttled at {motor1.throttle * 100}%.")

while measurements <= max_measurements:
  now = time.monotonic()
  if start_cycle:
    pos1 = encoder.position
    start_cycle = False
  else:
    pos2 = encoder.position
    if now >= LAST_EVAL_TIME + THROTTLE_HOLD:
      ticks = abs(pos2-pos1)
      orig_rounds = ticks / 7
      rounds = orig_rounds / 150
      rpm = rounds * (60 / THROTTLE_HOLD)
      start_cycle = True
      LAST_EVAL_TIME = now
      print(f'{measurements:02d} - Rounds per minute: {rpm:.1f}')
      measurements = measurements + 1
      
motor1.throttle = 0  # Stop motor1
print("Measurement completed") 