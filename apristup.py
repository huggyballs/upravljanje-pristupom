#glavni program
#upravljanje zaslonom i zvukom

import lcddriver
import RPi.GPIO as GPIO
import nfc

import time
import thread

import os
import sys
import mysql.connector
import tty
import logging
import traceback

db = mysql.connector.connect(
    host="localhost",
    user="emovis",
    passwd="emovis",
    database="kontrolapristupa"
    )
mycursor = db.cursor()

try:
    #kod za dodavanje tablice s korisnicima
    mycursor.execute("CREATE TABLE Users (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Seclev ENUM('1', '2') NOT NULL, role VARCHAR(10) NOT NULL)")
    pass
except:
    print("postoji")
    pass
    #tablica postoji pa se ide dalje
try:
    mycursor.execute("CREATE TABLE Devices (DeviceNum int PRIMARY KEY NOT NULL AUTO_INCREMENT, UserId int NOT NULL, DeviceId VARCHAR(40) NOT NULL)")
    #kod za dodavanje podtablice sa NFC uredjajima
    pass
except:
    print("postoji")
    pass

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

try:
    # Should be defined in Python 3
    x = TimeoutError
except:
    # For Python 2
    class TimeoutError(Exception):
        def __init__(self, value="Timeout"):
            self.value = value

        def __str__(self):
            return repr(self.value)

class ExpectTimeout(object):
    def __init__(self, seconds, print_traceback=True, mute=False):
        self.seconds_before_timeout = seconds
        self.original_trace_function = None
        self.end_time = None
        self.print_traceback = print_traceback
        self.mute = mute

    # Tracing function
    def check_time(self, frame, event, arg):
        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        current_time = time.time()
        if current_time >= self.end_time:
            raise TimeoutError

        return self.check_time

    # Begin of `with` block
    def __enter__(self):
        start_time = time.time()
        self.end_time = start_time + self.seconds_before_timeout

        self.original_trace_function = sys.gettrace()
        sys.settrace(self.check_time)
        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        self.cancel()

        if exc_type is None:
            return

        # An exception occurred
        if self.print_traceback:
            lines = ''.join(
                traceback.format_exception(
                    exc_type,
                    exc_value,
                    tb)).strip()
        else:
            lines = traceback.format_exception_only(
                exc_type, exc_value)[-1].strip()

        if not self.mute:
            print("(expected)")
        return True  # Ignore it

    def cancel(self):
        sys.settrace(self.original_trace_function)

#try:
    #ovo obrisati nakon prvog pokretanja
    #mycursor.execute("INSERT INTO Users (Seclev, role) VALUES (%s, %s)", (2, 'original'))
    #with ExpectTimeout(5, print_traceback=False):
        #try:
            #ID = clf.connect(rdwr={'on-connect': lambda tag: False})
            #print(ID)
            #ID2 = str(ID)
            #print(ID2)
            #print("Uspjesno citanje!")

            #pass
        #except:
            #print("Nesto ne valja!")
            #pass
        #pass
    #red = 1
    #mycursor.execute("INSERT INTO Devices (UserId, DeviceId) VALUES (%s, %s)", (red, ID2))
#except:
    #pass
#finally:
    #db.commit()
    #pass

def UserAdd():
    print("Uspjesno citanje")
    response = 0

    while response != 1 or response != 3:
        display.lcd_clear()
        display.lcd_display_string("Dodati korisnika", 1)
        display.lcd_display_string("1-DA 3-NE", 2)
        time.sleep(1)
        response = input()
        #provjera zeli li se dodati korisnika
        NewSecLevel = 0
        deviceID = ''

        if response == 1 :
            print("Odabrana opcija DA")

            while NewSecLevel != 1 or NewSecLevel != 2:
                #trazi definiranje nove sigurnosne razine
                display.lcd_clear()
                display.lcd_display_string("Sigurnosna razina", 1)
                display.lcd_display_string("1 ili 2?", 2)
                NewSecLevel = input()

                if NewSecLevel == 1 :
                    print("Sig. razina 1")
                    #Dodati sigurnosnu razinu u bazu
                    mycursor.execute("INSERT INTO Users (Seclev, role) VALUES (%s, %s)", (1, "korisnik"))
                    last_id = mycursor.lastrowid
                    last_id = int(last_id)
                    pass
                elif NewSecLevel == 2 :
                    print("Sig. razina 2")
                    #Dodati sigurnosnu razinu u bazu
                    mycursor.execute("INSERT INTO Users (Seclev, role) VALUES (%s, %s)", (2, "admin"))
                    last_id = mycursor.lastrowid
                    last_id = int(last_id)
                    pass
                else:
                    #Neispravan unos!
                    print("Neispravan unos!")
                    display.lcd_clear()
                    display.lcd_display_string("Neispravan", 1)
                    display.lcd_display_string("unos!", 2)
                    time.sleep(1)
                    pass

            #upit za broj uredjaja vezanih uz novododanog korisnika
            display.lcd_clear()
            display.lcd_display_string("Broj NFC", 1)
            display.lcd_display_string("uredjaja?", 2)
            i = 0
            DeviceNum = input()
            deviceID = ''

            while i < DeviceNum:
                print("Citanje novog NFC uredjaja")

                with ExpectTimeout(5, print_traceback=False):
                    try:
                        deviceID = clf.connect(rdwr={'on-connect': lambda tag: False})
                        deviceID = str(deviceID)
                        print(deviceID)
                        print("Uspjesno citanje!")
                        buzzerBeep()

                        #Ako je citanje uspjesno vezati ID uredjaja uz korisnika u bazi podataka

                        mycursor.execute("INSERT INTO Devices (UserId, DeviceId) VALUES (%s,%s)", (last_id, deviceID))

                        pass
                    except:
                        #isteklo vrijeme
                        print("Neuspjesno citanje")
                        display.lcd_clear()
                        display.lcd_display_string("Neuspjesno", 1)
                        display.lcd_display_string("Citanje!", 2)
                        buzzerBeep()
                        time.sleep(1)
                        i = i - 1
                        pass

                i = i + 1
            pass
        elif response == 3 :
            #Ukoliko se korisnik predomisli vraca se na pocetak
            print("Negativan odgovor!")
            pass
        else:
            #Unos nijedne od dvije odgovarajuce opcije
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
    secLevel = ''
    UserID = ''

    #program provjerava do pet sekundi nalazi li se u dometu valjani NFC uredjaj
    #provjera ovlasti za dodavanje

    with ExpectTimeout(5, print_traceback=False):
            try:
                UserID = clf.connect(rdwr={'on-connect': lambda tag: False})
                UserID = str(UserID)
                print(UserID)
                print("Uspjesno citanje!")
                buzzerBeep()
                #secLevel = 2
                #ovdje zapravo ide provjera sigurnosne razine u bazi podataka

                mycursor.execute("SELECT UserId FROM Devices WHERE DeviceId = %s", (UserID,))
                usid_int = mycursor.fetchone()
                usid_int = int(''.join(map(str, usid_int)))
                print(usid_int)
                mycursor.execute("SELECT Seclev FROM Users WHERE id = %s", (usid_int,))
                secLevel = mycursor.fetchone()
                secLevel = int(''.join(map(str, secLevel)))

                if secLevel == 2 :
                    print("Prelazak na dodavanje")
                    UserAdd()
                    #Ako korisnik ima odgovarajucu razinu prelazi se na dodavanje korisnika
                    pass
                else:
                    #baza je vratila da korisnik ne moze dodavati nove korisnike
                    print("Ne postoje ovlasti")
                    display.lcd_clear()
                    display.lcd_display_string("Nemate ovlasti", 1)
                    display.lcd_display_string("Za akciju!", 2)
                    time.sleep(1)
                    pass
                pass
            except:
                #isteklo vrijeme
                print("Neuspjesno citanje")
                display.lcd_clear()
                display.lcd_display_string("Neuspjesno", 1)
                display.lcd_display_string("Citanje!", 2)
                buzzerBeep()
                time.sleep(1)
                pass

def NFCReadAccess():
    print("Citanje uredjaja")
    display.lcd_clear()
    display.lcd_display_string("Prislonite NFC", 1)
    display.lcd_display_string("uredjaj!", 2)
    userID = ''

    #slijedi pokusaj citanja NFC-a u trajanju od 5 sekundi
    
    with ExpectTimeout(5, print_traceback=False):
        try:
            userID = clf.connect(rdwr={'on-connect': lambda tag: False})
            userID = str(userID)
            print(userID)
            print("Uspjesno citanje!")
            buzzerBeep()

            #ovdje ide provjera postojanja korisnika u bazi
            #ako korisnik postoji u bazi pozvat ce se funkcija za otvaranje vrata
            mycursor.execute("SELECT UserId FROM Devices WHERE DeviceId = %s", (userID,))
            usid_int = mycursor.fetchone()
            usid_int = int(''.join(map(str, usid_int)))
            print(usid_int)
            relayOpen()

            pass
        except:
            print("Nesto ne valja!")
            display.lcd_clear()
            display.lcd_display_string("Neuspjesno", 1)
            display.lcd_display_string("Citanje!", 2)
            buzzerBeep()
            time.sleep(1)
            pass

def buzzerBeep():
    #HIGH odgovara jedinci i zvuku a LOW nuli i tisini
    GPIO.output(buzzer,GPIO.HIGH)
    print("BIIIIP")
    time.sleep(0.5)
    GPIO.output(buzzer,GPIO.LOW)
    print("KRAJ BIIIIP")
    time.sleep(0.5)
    pass

def relayOpen():
    #HIGH odgovara jedinci i otkljucanim vratima a LOW nuli i ponovnom zakljucavanju
    GPIO.output(buzzer,GPIO.HIGH)
    print("Otkljucano")
    buzzerBeep()
    display.lcd_clear()
    display.lcd_display_string("Vrata su ", 1)
    display.lcd_display_string("otkljucana!", 2)
    time.sleep(1)
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

            #ovo ispod samo za provjeru pravilnog rada baze. Poslije ukloniti
            mycursor.execute("SELECT * FROM Users")
            for x in mycursor:
                print(x)
            
            mycursor.execute("SELECT * FROM Devices")
            for x in mycursor:
                print(x)

            unos = input()
            if unos == 1 :
                #kod za pristup funkciji za unos korisnika. Moze biti bilo koji
                print("Pokusaj dodavanja korisnika")
                NFCAddCheck()
                pass
            elif unos == 1234 :
                #unosom pina potvrdjujemo pokusaj pristupa vratima
                print("Unesen tocan PIN")
                NFCReadAccess()
                pass
            else:
                #u slucaju pogresnog unosa logirati pokusaj i slati upozorenje
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