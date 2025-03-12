import RPi.GPIO as GPIO
import time
a=0
led = 18
led2 = 23
led3 = 24
led4 = 25
buton = 26
buton2 = 27 
a=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)  
GPIO.setup(buton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buton2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(1)

while True:
    es= GPIO.input(buton)
    if es == GPIO.LOW and es == GPIO.HIGH:
        a += 1
    es1= GPIO.input(buton)
    if es1 == GPIO.LOW and es == GPIO.HIGH:
        a -= 1
    print("Decimal",a,"Hexadecimal",hex(a),"Binary",bin(a))   
    if(a==(-1)):
            a=0
    elif(a==0):
        GPIO.output(led, 0)
        GPIO.output(led2, 0)
        GPIO.output(led3, 0)
        GPIO.output(led4, 0)  
    elif(a==1):
        GPIO.output(led, 0)
        GPIO.output(led2, 0)
        GPIO.output(led3, 0)
        GPIO.output(led4, 1)
    elif(a==2):
         GPIO.output(led, 0)
         GPIO.output(led2, 0)
         GPIO.output(led3, 1)
         GPIO.output(led4, 0)  
    elif(a==3):
         GPIO.output(led, 0)
         GPIO.output(led2, 0)
         GPIO.output(led3, 1)
         GPIO.output(led4, 1)  
    elif(a==4):
            GPIO.output(led, 0)
            GPIO.output(led2, 1)
            GPIO.output(led3, 0)
            GPIO.output(led4, 0) 
    elif(a==5):
            GPIO.output(led, 0)
            GPIO.output(led2, 1)
            GPIO.output(led3, 0)
            GPIO.output(led4, 1)  
    elif(a==6):
            GPIO.output(led, 0)
            GPIO.output(led2, 1)
            GPIO.output(led3, 1)
            GPIO.output(led4, 0)    
    elif(a==7): 
            GPIO.output(led, 0)
            GPIO.output(led2, 1)
            GPIO.output(led3, 1)
            GPIO.output(led4, 1)
    elif(a==8):
            GPIO.output(led, 1)
            GPIO.output(led2, 0)
            GPIO.output(led3, 0)
            GPIO.output(led4, 0)
    elif(a==9): 
            GPIO.output(led, 1)
            GPIO.output(led2, 0)
            GPIO.output(led3, 0)
            GPIO.output(led4, 1)
    elif(a==10):
            GPIO.output(led, 1)
            GPIO.output(led2, 0)
            GPIO.output(led3, 1)
            GPIO.output(led4, 0)
    elif(a==11):
            GPIO.output(led, 1)
            GPIO.output(led2, 0)
            GPIO.output(led3, 1)
            GPIO.output(led4, 1)
    elif(a==12):
            GPIO.output(led, 1)
            GPIO.output(led2, 1)
            GPIO.output(led3, 0)
            GPIO.output(led4, 0)
    elif(a==13):
            GPIO.output(led, 1)
            GPIO.output(led2, 1)
            GPIO.output(led3, 0)
            GPIO.output(led4, 1)
    elif(a==14):
            GPIO.output(led, 1)
            GPIO.output(led2, 1)
            GPIO.output(led3, 1)
            GPIO.output(led4, 0)
    elif(a==15):
            GPIO.output(led, 1)
            GPIO.output(led2, 1)
            GPIO.output(led3, 1)
            GPIO.output(led4, 1) 
    elif(a==16):
            a= 0