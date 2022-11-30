"""
  Control DC motor using Maker Drive and CircuitPython on RP2040.
"""

from adafruit_motor import motor
import adafruit_ssd1306
import board
import busio as io
import digitalio
import pwmio
import rotaryio
import time

PWM_M1A = board.GP2  # pick any pwm pins on their own channels
PWM_M1B = board.GP3
PWM_FREQ = 10000  # Custom PWM frequency
SCL = board.GP15
SDA = board.GP14
DECAY_MODE = motor.SLOW_DECAY  # Set controller to Slow Decay (braking) mode
THROTTLE_HOLD = 10  # Hold the throttle (seconds)
MEASUREMENTS = 1
MAX_MEASUREMENTS = 10
LAST_EVAL_TIME = time.monotonic()


# DC motor setup
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=PWM_FREQ)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=PWM_FREQ)
motor1 = motor.DCMotor(pwm_1a, pwm_1b)
 
# set up encoder
encoder = rotaryio.IncrementalEncoder(board.GP16, board.GP17)
motor1.throttle = 0.4
pos1 = -1
START_CYCLE = True
rpm = 0

# set up display
i2c = io.I2C(SCL, SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

def write_on_display(msg):
  oled.fill(0)
  oled.text(msg, 0, 0, 1)
  oled.show()

def calc_rpm_from_ticks(pos1, pos2):
  ticks = abs(pos2-pos1)
  orig_rounds = ticks / 7
  rounds = orig_rounds / 150
  rpm = rounds * (60 / THROTTLE_HOLD)
  return rpm

print(f"Polling motor speed in RPM every {THROTTLE_HOLD} seconds for {MAX_MEASUREMENTS} cycles.")
print(f"Motor is throttled at {motor1.throttle * 100}%.")

while MEASUREMENTS <= MAX_MEASUREMENTS:
  now = time.monotonic()
  if START_CYCLE:
    pos1 = encoder.position
    START_CYCLE = False
  else:
    pos2 = encoder.position
    if now >= LAST_EVAL_TIME + THROTTLE_HOLD:
      rpm = calc_rpm_from_ticks(pos1, pos2)
      START_CYCLE = True
      LAST_EVAL_TIME = now
      msg = f'{MEASUREMENTS:02d} - Rounds per minute: {rpm:.1f}'
      write_on_display(f'RPM: {rpm:.1f}')
      print(msg)
      MEASUREMENTS = MEASUREMENTS + 1
      
motor1.throttle = 0  # Stop motor1
print("Measurement completed.") 