import RPi.GPIO as GPIO
import time

# Pin setting
LED_PIN = 16
BUZZER_PIN = 18

# Buzzer frequency
freq = 523

# Morse code time
unit = 0.3

GPIO.setmode(GPIO.BOARD)

# LED
GPIO.setup(LED_PIN, GPIO.OUT)

# Buzzer
GPIO.setup(BUZZER_PIN, GPIO.OUT)
voice = GPIO.PWM(BUZZER_PIN, freq)


# LED and buzzer ON
def signal_on():
    GPIO.output(LED_PIN, True)
    voice.start(50)


# LED and buzzer OFF
def signal_off():
    GPIO.output(LED_PIN, False)
    voice.stop()


# Short signal "."
def dot():
    signal_on()
    time.sleep(unit)
    signal_off()
    time.sleep(unit)


# Long signal "-"
def dash():
    signal_on()
    time.sleep(unit * 3)
    signal_off()
    time.sleep(unit)


try:
    # S = ...
    dot()
    dot()
    dot()

    time.sleep(unit * 2)

    # O = ---
    dash()
    dash()
    dash()

    time.sleep(unit * 2)

    # S = ...
    dot()
    dot()
    dot()

finally:
    signal_off()
    GPIO.cleanup()