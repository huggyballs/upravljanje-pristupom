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

display = lcddriver.lcd()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
buzzer = 5
relay = 6
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(relay,GPIO.OUT)

def UserAdd():
    print("Uspjesno citanje")
    response = 0

    while response != 1 or response != 3:
        display.lcd_clear()
        display.lcd_display_string("Dodati korisnika", 1)
        display.lcd_display_string("1-DA 3-NE", 2)
        time.sleep(1)
        response = input()
        NewSecLevel = 0

        if response == 1 :
            #dodati korisnika u bazu kao novi unos

            while NewSecLevel != 1 or NewSecLevel != 2:
                display.lcd_clear()
                display.lcd_display_string("Sigurnosna razina", 1)
                display.lcd_display_string("1 ili 2?", 2)
                NewSecLevel = input()

                if NewSecLevel == 1 :
                    #Dodati sigurnosnu razinu u bazu
                    pass
                elif NewSecLevel == 2 :
                    #Dodati sigurnosnu razinu u bazu
                    pass
                else:
                    display.lcd_clear()
                    display.lcd_display_string("Neispravan", 1)
                    display.lcd_display_string("unos!", 2)
                    time.sleep(1)
                    pass

            display.lcd_clear()
            display.lcd_display_string("Broj NFC", 1)
            display.lcd_display_string("uredjaja?", 2)
            i = 0
            DeviceNum = input()

            while i < DeviceNum:
                print("Citanje novog NFC uredjaja")
                #Čitanje
                #Dodavanje uređaja u bazu
                i = i + 1
            pass
        elif response == 3 :
            print("Negativan odgovor!")
            pass
        else:
            display.lcd_clear()
            display.lcd_display_string("Neispravan", 1)
            display.lcd_display_string("odgovor!", 2)
            time.sleep(1)
            pass
        pass
    pass

def NFCAddCheck():
    print("Provjera sigurnosne razine NFC tagom")
    display.lcd_clear()
    display.lcd_display_string("Prislonite NFC", 1)
    display.lcd_display_string("uredjaj", 2)
    starttime = time.time()
    readflag = 0
    secLevel = ''

    #program provjerava pet sekundi nalazi li se u dometu valjani NFC uređaj

    while True:
        currenttime = time.time()
        elapsedtime = currenttime - starttime
        print("Citanje")
        #Dodati kod za čitanje uređaja/kartice
        if elapsedtime > 5 :
            print("Neuspjesno citanje")
            display.lcd_clear()
            display.lcd_display_string("Neuspjesno", 1)
            display.lcd_display_string("Citanje!", 2)
            buzzerBeep()
            time.sleep(1)
            break
        elif elapsedtime > 6:
            #uvjet iznad je tu samo privremeno
            #Nakon potpune implementacije citanja uvjet ce biti da zastavica koja oznacava uspjesno citanje bude u jedinici
            #Nakon toga slijedit ce provjera
            #Napomena sebi da ne zaboravim zastavicu
            break

    if readflag == 1 :
        if secLevel == 2 :
            print("Prelazak na dodavanje")
            UserAdd()
            #Ako korisnik ima odgovarajuću razinu prelazi se na dodavanje korisnika
        else:
            print("Ne postoje ovlasti")
            display.lcd_clear()
            display.lcd_display_string("Nemate ovlasti", 1)
            display.lcd_display_string("Za akciju!", 2)
            time.sleep(1)
            pass 
    pass

def NFCReadAccess():
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