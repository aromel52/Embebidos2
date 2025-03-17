import RPi.GPIO as GPIO
import time
a=0
led = 18
led2 = 23
buton = 26
buton2 = 27 
a=0
b=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(buton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buton2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(1)

while True:
    es= GPIO.input(buton)
    if es == GPIO.LOW and es == GPIO.HIGH:
        a += 1
    es1= GPIO.input(buton)
    if es1 == GPIO.LOW and es == GPIO.HIGH:
        b+= 1
    if(a==1):
        GPIO.output(led, 1)
        b=0
    elif(a==1 & b==1):
        GPIO.output(led, 0)
        a=0

        
    