#glavni program
#upravljanje zaslonom i zvukom

import lcddriver
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

buzzer = 29
GPIO.setup(buzzer,GPIO.OUT)

pin = ""
odgovor = ""

ekran = lcddriver.lcd()

def pristup():
    print("tocan PIN")
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(buzzer,GPIO.LOW)
    ekran.lcd_display_string("PIN je tocan!", 1)
    time.sleep(2)

def dodavanje():
    print("dodavanje")
    ekran.lcd_display_string("Dodati novog korisnika?", 1)
    ekran.lcd_display_string("1-DA 3-NE", 2)
    odgovor = input()
    if odgovor == 1:
        print("potvrda dodavanja")
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        ekran.lcd_display_string("Prislonite NFC", 1)
        ekran.lcd_display_string("uredjaj:", 2)
        time.sleep(3)
    elif odgovor == 3:
        main()
    else:
        print("netocan odgovor!")
        ekran.lcd_display_string("Netocan odgovor!", 1)
        time.sleep(2)
        dodavanje()



def unos():
    
    print("unos zaporke")
    pin = input()
    if pin == 7 :
        print("Dodavanje novog korisnika")
        dodavanje()
        pass  
    elif pin == 1234:
        pristup()
        pass 
    else:
        print("netocan unos")
        ekran.lcd_display_string("Netocan unoS!", 1)
        time.sleep(3)
        main()
        pass 

def main():
    print("pocetak rada sustava")
    ekran.lcd_display_string("Unesite PIN", 1)
    unos()
    print("uspjesan kraj!")


if __name__ == "__main__":
    main()