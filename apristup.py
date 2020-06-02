#glavni program
#upravljanje zaslonom i zvukom

import lcddriver
import RPi.GPIO as GPIO

import time
import thread

import os
import sys
import mysql
import tty
import termios
import logging


DEBUG=True
VERNOSE=True

buzzer = 5
relay = 6

def NFCReadAccess():
    pass

def NFCAddCheck():
    pass

def buzzerBeep():
    GPIO.output(buzzer,GPIO.HIGH)
    print("BIIIIP")
    time.sleep(1)
    GPIO.output(buzzer,GPIO.LOW)
    print("KRAJ BIIIIP")
    time.sleep(1)
    pass

def relayOpen():
    GPIO.output(buzzer,GPIO.HIGH)
    print("Otkljucano")
    time.sleep(5)
    GPIO.output(buzzer,GPIO.LOW)
    print("Zakljucano")
    pass

def main():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(buzzer,GPIO.OUT)
        GPIO.setup(relay,GPIO.OUT)

        display = lcddriver.lcd()

        while True:
            display.lcd_clear()
            display.lcd_display_string("Unesite PIN:", 1)
            unos = input()
            if unos == 1 :
                print("Pokusaj dodavanja korisnika")
                NFCAddCheck()
                pass
            elif unos == 1234 :
                print("Unesen tocan PIN")
                NFCReadAccess()
                pass
            else:
                print("Netocan unos")
                display.lcd_clear()
                display.lcd_display_string("Netocan unos!", 1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Kraj rada programa")
        pass    
    GPIO.cleanup()


if __name__ == '__main__':
    main()