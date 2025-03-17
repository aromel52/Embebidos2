import RPi.GPIO as GPIO
import time
a=0
led = 18
buton = 24
a=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT) 
GPIO.setup(buton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(1)
while True:
    es= GPIO.input(buton)
    if es == GPIO.LOW and es == GPIO.HIGH:
        GPIO.output(led, 1)
    else
        GPIO.output(led, 0)