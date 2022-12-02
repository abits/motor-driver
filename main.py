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

PWM_M1A = board.GP4 
PWM_M1B = board.GP5
PWM_M2A = board.GP2 
PWM_M2B = board.GP3
PWM_FREQ = 10000
SCL = board.GP15
SDA = board.GP14

DECAY_MODE = motor.SLOW_DECAY 
INTERVAL = 10  # Hold the throttle (seconds)
MEASUREMENTS = 1
MAX_MEASUREMENTS = 10
LAST_EVAL_TIME = time.monotonic()
START_CYCLE = True


# DC motor setup
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=PWM_FREQ)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=PWM_FREQ)
motor1 = motor.DCMotor(pwm_1a, pwm_1b)
pwm_2a = pwmio.PWMOut(PWM_M2A, frequency=PWM_FREQ)
pwm_2b = pwmio.PWMOut(PWM_M2B, frequency=PWM_FREQ)
motor2 = motor.DCMotor(pwm_2a, pwm_2b)
 
# set up encoder
encoder1 = rotaryio.IncrementalEncoder(board.GP16, board.GP17)
pos11 = -1
encoder2 = rotaryio.IncrementalEncoder(board.GP18, board.GP19)
pos12 = -1
rpm = 0

# set up display
i2c = io.I2C(SCL, SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

def write_on_display(msg, line):
  oled.fill(0)
  oled.text(msg, 0, 0, line)
  oled.show()

def calc_rpm_from_ticks(pos1, pos2):
  ticks = abs(pos2-pos1)
  orig_rounds = ticks / 7
  rounds = orig_rounds / 150
  rpm = rounds * (60 / INTERVAL)
  return rpm

motor1.throttle = 0.6
motor2.throttle = 0.6
print(f"Polling motor speed in RPM every {INTERVAL} seconds for {MAX_MEASUREMENTS} cycles.")
print(f"Motor 1 is throttled at {motor1.throttle * 100}%.")
print(f"Motor 2 is throttled at {motor2.throttle * 100}%.")

while MEASUREMENTS <= MAX_MEASUREMENTS:
  now = time.monotonic()
  if START_CYCLE:
    pos11 = encoder1.position
    pos12 = encoder2.position
    START_CYCLE = False
  else:
    pos21 = encoder1.position
    pos22 = encoder1.position
    if now >= LAST_EVAL_TIME + INTERVAL:
      rpm1 = calc_rpm_from_ticks(pos11, pos21)
      rpm2 = calc_rpm_from_ticks(pos12, pos22)
      START_CYCLE = True
      LAST_EVAL_TIME = now
      msg = f'{MEASUREMENTS:02d}: 1 {rpm1:.1f} - 2 {rpm2:.1f}'
      write_on_display(msg, 1)
      print(msg)
      MEASUREMENTS = MEASUREMENTS + 1
      
motor1.throttle = 0  # Stop motor1
print("Measurement completed.") 