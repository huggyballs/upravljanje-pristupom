#glavni program
#upravljanje zaslonom i zvukom

import lcddriver
import RPi.GPIO as GPIO
import nfc

import time
import thread

import os
import sys
import mysql
import tty
import termios
import logging


DEBUG=True
VERBOSE=True

display = lcddriver.lcd()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
clf = nfc.ContactlessFrontend()
clf.open('ttyAMA0')
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
        #provjera želi li se dodati korisnika
        NewSecLevel = 0
        deviceID = ''

        if response == 1 :
            print("Odabrana opcija DA")
            #dodati korisnika u bazu kao novi unos

            while NewSecLevel != 1 or NewSecLevel != 2:
                #traži definiranje nove sigurnosne razine
                display.lcd_clear()
                display.lcd_display_string("Sigurnosna razina", 1)
                display.lcd_display_string("1 ili 2?", 2)
                NewSecLevel = input()

                if NewSecLevel == 1 :
                    print("Sig. razina 1")
                    #Dodati sigurnosnu razinu u bazu
                    pass
                elif NewSecLevel == 2 :
                    print("Sig. razina 2")
                    #Dodati sigurnosnu razinu u bazu
                    pass
                else:
                    #Neispravan unos!
                    print("Neispravan unos!")
                    display.lcd_clear()
                    display.lcd_display_string("Neispravan", 1)
                    display.lcd_display_string("unos!", 2)
                    time.sleep(1)
                    pass

            #upit za broj uređaja vezanih uz novododanog korisnika
            display.lcd_clear()
            display.lcd_display_string("Broj NFC", 1)
            display.lcd_display_string("uredjaja?", 2)
            i = 0
            DeviceNum = input()
            starttime = time.time()
            deviceID = ''

            while i < DeviceNum:
                print("Citanje novog NFC uredjaja")
                while True:
                    #čitanje uređaja
                    currenttime = time.time()
                    elapsedtime = currenttime - starttime
                    deviceID = clf.connect(rdwr={'on-connect': lambda tag: False})

                    if elapsedtime > 5 :
                        #isteklo vrijeme
                        print("Neuspjesno citanje")
                        display.lcd_clear()
                        display.lcd_display_string("Neuspjesno", 1)
                        display.lcd_display_string("Citanje!", 2)
                        buzzerBeep()
                        time.sleep(1)
                        break
                    elif deviceID != '':
                        #uspješno čitanje
                        print("Uspjesno citanje!")
                        print(deviceID)
                        #Ako je čitanje uspješno vezati ID uređaja uz korisnika u bazi podataka
                        buzzerBeep()
                        break
                buzzerBeep()
                i = i + 1
            pass
        elif response == 3 :
            #Ukoliko se korisnik predomisli vraća se na početak
            print("Negativan odgovor!")
            pass
        else:
            #Unos nijedne od dvije odgovarajuće opcije
            print("Neispravan odgovor!")
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
    UserID = ''

    #program provjerava do pet sekundi nalazi li se u dometu valjani NFC uređaj
    while True:
        currenttime = time.time()
        elapsedtime = currenttime - starttime
        UserID = clf.connect(rdwr={'on-connect': lambda tag: False})
        #provjeravanje ovlasti za dodavanje

        if elapsedtime > 5 :
            #isteklo vrijeme
            print("Neuspjesno citanje")
            display.lcd_clear()
            display.lcd_display_string("Neuspjesno", 1)
            display.lcd_display_string("Citanje!", 2)
            buzzerBeep()
            time.sleep(1)
            break
        elif UserID != '':
            print("Uspjesno citanje!")
            buzzerBeep()
            print(UserID)
            readflag = 1
            #Nakon toga slijedit ce provjera ima li korisnik ovlasti za unos u bazi podataka
            #secLevel = 2
            if readflag == 1 :
                if secLevel == 2 :
                    print("Prelazak na dodavanje")
                    UserAdd()
                    #Ako korisnik ima odgovarajuću razinu prelazi se na dodavanje korisnika
                    pass
                else:
                    #baza je vratila da korisnik ne može dodavati nove korisnike
                    print("Ne postoje ovlasti")
                    display.lcd_clear()
                    display.lcd_display_string("Nemate ovlasti", 1)
                    display.lcd_display_string("Za akciju!", 2)
                    time.sleep(1)
                    pass
            break
    pass

def NFCReadAccess():
    print("Čitanje uređaja")
    display.lcd_clear()
    display.lcd_display_string("Prislonite NFC", 1)
    display.lcd_display_string("uredjaj!", 2)
    starttime = time.time()
    userID = ''

    #slijedi pokušaj čitanja NFC-a u trajanju od 5 sekundi
    while True:
        currenttime = time.time()
        elapsedtime = currenttime - starttime

        userID = clf.connect(rdwr={'on-connect': lambda tag: False})

        if elapsedtime > 5 :
            #vrijeme isteklo, izlaz iz petlje
            print("Neuspjesno citanje")
            display.lcd_clear()
            display.lcd_display_string("Neuspjesno", 1)
            display.lcd_display_string("Citanje!", 2)
            buzzerBeep()
            time.sleep(1)
            break
        elif userID != '' :
            print("uspjesno citanje!")
            print(userID)
            #uvjet da je čitanje uspješno
            #slijedi kod za provjeru postojanja korisnika
            #ako korisnik postoji u bazi slijedi otvaranje vrata
            buzzerBeep()
            #provjera postojanja i dodavanje u if petlji
            break

def buzzerBeep():
    #HIGH odgovara jedinci i zvuku a LOW nuli i tišini
    GPIO.output(buzzer,GPIO.HIGH)
    print("BIIIIP")
    time.sleep(0.5)
    GPIO.output(buzzer,GPIO.LOW)
    print("KRAJ BIIIIP")
    time.sleep(0.5)
    pass

def relayOpen():
    #HIGH odgovara jedinci i otključanikm vratima a LOW nuli i ponovnom zaključavanju
    GPIO.output(buzzer,GPIO.HIGH)
    print("Otkljucano")
    buzzerBeep()
    time.sleep(5)
    GPIO.output(buzzer,GPIO.LOW)
    print("Zakljucano")
    pass

def main():
    try:

        while True:
            print("Vrti se pocetni ekran")
            display.lcd_clear()
            display.lcd_display_string("Unesite PIN:", 1)
            unos = input()
            if unos == 1 :
                #kod za pristup funkciji za unos korisnika. Može biti bilo koji
                print("Pokusaj dodavanja korisnika")
                NFCAddCheck()
                pass
            elif unos == 1234 :
                #unosom pina potvrđujemo pokušaj pristupa vratima
                print("Unesen tocan PIN")
                NFCReadAccess()
                pass
            else:
                #u slučaju pogrešnog unosa logirati pokušaj i slati upozorenje
                print("Netocan unos")
                display.lcd_clear()
                display.lcd_display_string("Netocan unos!", 1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Kraj rada programa")
        clf.close()
        pass    
    GPIO.cleanup()

if __name__ == '__main__':
    main()