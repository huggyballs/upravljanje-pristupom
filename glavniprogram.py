#glavni program
#upravljanje zaslonom i zvukom

import lcddriver
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

buzzer = 5
relay = 6
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(relay,GPIO.OUT)

pin = ""
odgovor = ""
level = ""

ekran = lcddriver.lcd()

def NFCread():
    print("placeholder")

def TagNumberNFC():
    print("Odabir broja tagova i dodavanje u bazu")
    ekran.lcd_clear()
    ekran.lcd_display_string("Broj tagova", 1)
    ekran.lcd_display_string("korisnika?", 2)
    b = input()
    i = 0
    while i < b:
        print("Dodavanje taga")
        ekran.lcd_clear()
        ekran.lcd_display_string("Prislonite NFC", 1)
        ekran.lcd_display_string("uredjaj!", 2)
        NFCread()


def SecurityLevel():
    print("Odabir sigurnosne razine")
    ekran.lcd_clear()
    ekran.lcd_display_string("Sigurnosna razina", 1)
    ekran.lcd_display_string("1, 2, 3?", 2)
    level = input()
    if level == 1 or level == 2 or level == 3:
        odgovorstr = str(level)
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        ekran.lcd_clear()
        ekran.lcd_display_string("Razina " + odgovorstr, 1)
        ekran.lcd_display_string("Odabrana!", 2)
        time.sleep(2)
        pass
    else:
        ekran.lcd_clear()
        ekran.lcd_display_string("Pogresan", 1)
        ekran.lcd_display_string("unos!", 2)
        time.sleep(2)
        SecurityLevel()
        pass   

def NFCadd():
    print("upit za NFC uredjaj")
    SecurityLevel()
    TagNumberNFC()
    ekran.lcd_clear()
    ekran.lcd_display_string("Prislonite NFC", 1)
    ekran.lcd_display_string("uredjaj:", 2)
    time.sleep(3)

def pristup():
    ekran.lcd_clear()
    print("tocan PIN")
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(buzzer,GPIO.LOW)
    ekran.lcd_display_string("PIN je tocan!", 1)
    time.sleep(2)

def dodavanje():
    ekran.lcd_clear()
    print("dodavanje")
    ekran.lcd_display_string("Dodati korisnika?", 1)
    ekran.lcd_display_string("1-DA 3-NE", 2)
    odgovor = input()
    if odgovor == 1:
        print("potvrda dodavanja")
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        NFCadd()
    elif odgovor == 3:
        main()
    else:
        print("netocan odgovor!")
        ekran.lcd_clear()
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
        ekran.lcd_clear()
        ekran.lcd_display_string("Netocan unoS!", 1)
        time.sleep(3)
        main()
        pass 

def main():
    ekran.lcd_clear()
    print("pocetak rada sustava")
    ekran.lcd_display_string("Unesite PIN", 1)
    unos()
    GPIO.output(buzzer,GPIO.LOW)
    ekran.lcd_clear()
    print("uspjesan kraj!")

if __name__ == "__main__":
    main()