import RPi.GPIO as GPIO
import time
a=0
led = 18
led2 = 23
buton = 24
a=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)  
GPIO.setup(buton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(1)
while True:
    es= GPIO.input(buton)
    if es == GPIO.LOW and es == GPIO.HIGH:
        a += 1
    if(a==0):
        GPIO.output(led, 0)
        GPIO.output(led2, 0)
    elif(a==1):
        GPIO.output(led, 1)
        GPIO.output(led2, 0)
        time.sleep(1)
        GPIO.output(led, 0)
        GPIO.output(led2, 1)
        time.sleep(1)
    elif(a==2):
        GPIO.output(led, 1)
        GPIO.output(led2, 1)
        time.sleep(2)
        GPIO.output(led, 0)
        GPIO.output(led2, 0)
        time.sleep(2)
    elif(a==3):
        GPIO.output(led, 1)
        GPIO.output(led2, 1)
    elif(a==4):
        a=0