#glavni program

import lcddriver
import RPi.GPIO as GPIO
import nfc

import time
from datetime import datetime
import thread

import os
import sys
import mysql.connector
import tty
import logging
from logging.handlers import RotatingFileHandler
import traceback

import smtplib
import ssl

db = mysql.connector.connect(
    host="localhost",
    user="emovis",
    passwd="emovis",
    database="kontrolapristupa",
    autocommit=True
    )
mycursor = db.cursor(buffered=True)

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
    pass
except:
    print("postoji")
    pass
try:
    mycursor.execute("CREATE TABLE Logs (LogNum int PRIMARY KEY NOT NULL AUTO_INCREMENT, dt DATETIME NOT NULL, logType VARCHAR(15) NOT NULL, logMsg VARCHAR(100) NOT NULL)")
    pass
except:
    print("postoji")
    pass
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

handlerinfo = RotatingFileHandler('info.log', maxBytes=100000, backupCount=2)
handlerinfo.setFormatter(formatter)
handlerinfo.setLevel(logging.DEBUG)
handleraction = RotatingFileHandler('interactions.log', maxBytes=100000, backupCount=2)
handleraction.setFormatter(formatter)
handleraction.setLevel(logging.INFO)
handlerwarning = RotatingFileHandler('warnings.log', maxBytes=100000, backupCount=2)
handlerwarning.setFormatter(formatter)
handlerwarning.setLevel(logging.WARNING)

logger.addHandler(handlerwarning)
logger.addHandler(handlerinfo)
logger.addHandler(handleraction)

display = lcddriver.lcd()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
clf = nfc.ContactlessFrontend()
clf.open('ttyAMA0')
buzzer = 5
relay = 6
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(relay,GPIO.OUT)

port = 587
smtp_server = "smtp.gmail.com"
sender_email = "upravljanjepristupom@gmail.com"
receiver_email = "mraic00@fesb.hr"
password = "emovis123"
mg1 = """\
Subject: Upozorenje!

Sustav je zabiljezio neovlasten pokusaj pristupa!"""
mg2 = """\
Subject: Upozorenje!

Sustav je zabiljezio neovlasten pokusaj brisanja/dodavanja korisnika!"""

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

def UserAdd():
    print("Uspjesno citanje")
    response = ''

    while True:
        display.lcd_clear()
        display.lcd_display_string("Dodati korisnika", 1)
        display.lcd_display_string("1-DA 3-NE", 2)
        time.sleep(1)
        print("Dodati korisnika? 1-da 3-ne")
        response = input()
        #provjera zeli li se dodati korisnika
        NewSecLevel = 0
        deviceID = ''

        if response == 1 :
            print("Odabrana opcija DA")

            while True:
                #trazi definiranje nove sigurnosne razine
                display.lcd_clear()
                display.lcd_display_string("Sigurnosna razina", 1)
                display.lcd_display_string("1 ili 2?", 2)
                print("Sigurnosna razina 1 ili 2?")
                logger.debug('Zatrazen unos sigurnosne razine novog korisnika.')
                NewSecLevel = input()

                if NewSecLevel == 1 :
                    print("Sig. razina 1")
                    logger.debug('Potvrdjena sigurnosna razina 1')
                    #Dodati sigurnosnu razinu u bazu
                    mycursor.execute("INSERT INTO Users (Seclev, role) VALUES (%s, %s)", (1, "korisnik"))
                    logger.info('Dodan novi korisnik')
                    now = datetime.now()
                    now = now.strftime('%Y-%m-%d %H:%M:%S')      
                    mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Informacija', 'Dodan novi korisnik'))
                    last_id = mycursor.lastrowid
                    last_id = int(last_id)
                    break
                elif NewSecLevel == 2 :
                    print("Sig. razina 2")
                    logger.debug('potvrdjena sigurnosna razina 2')
                    #Dodati sigurnosnu razinu u bazu
                    mycursor.execute("INSERT INTO Users (Seclev, role) VALUES (%s, %s)", (2, "admin"))
                    logger.info('Dodan novi korisnik')
                    now = datetime.now()
                    now = now.strftime('%Y-%m-%d %H:%M:%S')      
                    mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Informacija', 'Dodan novi korisnik'))
                    last_id = mycursor.lastrowid
                    last_id = int(last_id)
                    break
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
            print("Broj uredjaja?")
            DeviceNum = input()
            logger.debug('Novom korisniku dodijeljeno {} uredjaja'.format(DeviceNum))
            deviceID = ''

            while i < DeviceNum:
                print("Citanje novog NFC uredjaja")

                with ExpectTimeout(10, print_traceback=False):
                    try:
                        deviceID = clf.connect(rdwr={'on-connect': lambda tag: False})
                        deviceID = str(deviceID)
                        print(deviceID)
                        print("Uspjesno citanje!")
                        buzzerBeep()

                        mycursor.execute("INSERT INTO Devices (UserId, DeviceId) VALUES (%s,%s)", (last_id, deviceID))
                        logger.info('Korisniku dodijeljen novi uredjaj')
                        now = datetime.now()
                        now = now.strftime('%Y-%m-%d %H:%M:%S')      
                        mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Informacija', 'Dodijeljen novi uredjaj korisniku'))
                        pass
                    except:
                        #isteklo vrijeme
                        print("Neuspjesno citanje")
                        logger.warning('Neuspjesno dodavanja novog uredjaja')
                        now = datetime.now()
                        now = now.strftime('%Y-%m-%d %H:%M:%S')      
                        mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Upozorenje', 'Neuspjesan pokusaj dodavanje uredjaja'))
                        display.lcd_clear()
                        display.lcd_display_string("Neuspjesno", 1)
                        display.lcd_display_string("Citanje!", 2)
                        buzzerBeepAlarm()
                        time.sleep(1)
                        i = i - 1
                        pass
                i = i + 1
            return False
        elif response == 3 :
            #Ukoliko se korisnik predomisli vraca se na pocetak
            print("Negativan odgovor!")
            return False
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
    logger.debug('Pokusaj dodavanja novog korisnika')
    display.lcd_clear()
    display.lcd_display_string("Prislonite NFC", 1)
    display.lcd_display_string("uredjaj", 2)
    secLevel = ''
    UserID = ''

    #program provjerava do pet sekundi nalazi li se u dometu valjani NFC uredjaj
    #provjera ovlasti za dodavanje

    try:
        UserID = clf.connect(rdwr={'on-connect': lambda tag: False})
        UserID = str(UserID)
        print(UserID)
        print("Uspjesno citanje!")
        buzzerBeep()
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
            logger.info('Uspjesna provjera sigurnosnih ovlasti korisnika {}'.format(usid_int))
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')      
            mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Informacija', 'Uspjesna provjera sigurnosnih ovlasti za dodavanje novog korisnika'))
            UserAdd()
            pass
        else:
            #baza je vratila da korisnik ne moze dodavati nove korisnike
            print("Ne postoje ovlasti")
            logger.warning('Korisnik {} je pokusao dodati nove korisnike a nema ovlasti za to'.format(usid_int))
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')      
            mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Upozorenje', 'Korisnik neovlasteno pokusao dodati nove korisnike'))
            display.lcd_clear()
            sendEmail(2)
            display.lcd_display_string("Nemate ovlasti", 1)
            display.lcd_display_string("Za akciju!", 2)
            buzzerBeepAlarm()
            time.sleep(1)
            pass
        pass
    except:
        print("Neuspjesno citanje")
        logger.warning('Neuspjesna provjera sigurnosnih ovlasti')
        now = datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')      
        mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Upozorenje', 'Neuspjesna provjera ovlasti'))
        sendEmail(2)
        display.lcd_clear()
        display.lcd_display_string("Neuspjesno", 1)
        display.lcd_display_string("Citanje!", 2)
        buzzerBeepAlarm()
        time.sleep(1)
        pass

def NFCReadAccess():
    print("Citanje uredjaja")
    logger.debug('Pokusaj ulaska')
    display.lcd_clear()
    display.lcd_display_string("Prislonite NFC", 1)
    display.lcd_display_string("uredjaj!", 2)
    userID = ''

    #slijedi pokusaj citanja NFC-a u trajanju od 5 sekundi
    
    with ExpectTimeout(10, print_traceback=False):
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
            logger.info('Uspjesno ostvaren pristup od strane korisnika {}'.format(usid_int))
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')      
            mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Informacija', 'Uspjesan ulazak'))
            relayOpen()

            pass
        except:
            print("Nesto ne valja!")
            logger.warning('Neuspjesan pokusaj ulaska')
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')      
            mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Upozorenje', 'Neuspjesan pokusaj ulaska'))
            sendEmail(1)

            display.lcd_clear()
            display.lcd_display_string("Neuspjesno", 1)
            display.lcd_display_string("Citanje!", 2)
            buzzerBeepAlarm()
            time.sleep(1)
            pass

def resetFunction():
    display.lcd_clear()
    display.lcd_display_string("Potvrditi akciju", 1)
    display.lcd_display_string("PIN-om!", 2)

    unos = input("Unesi pin: ")

    if unos == 1234:

        display.lcd_clear()
        display.lcd_display_string("Prislonite NFC", 1)
        display.lcd_display_string("uredjaj!", 2)
        UserID = ''

        try:
            UserID = clf.connect(rdwr={'on-connect': lambda tag: False})
            UserID = str(UserID)
            print(UserID)
            print("Uspjesno citanje!")
            buzzerBeep()

            mycursor.execute("SELECT UserId FROM Devices WHERE DeviceId = %s", (UserID,))
            usid_int = mycursor.fetchone()
            usid_int = int(''.join(map(str, usid_int)))
            print(usid_int)
            mycursor.execute("SELECT Seclev FROM Users WHERE id = %s", (usid_int,))
            secLevel = mycursor.fetchone()
            secLevel = int(''.join(map(str, secLevel)))

            if secLevel == 2 :
                print("Prelazak na dodavanje")
                logger.info('Uspjesna provjera sigurnosnih ovlasti korisnika {}'.format(usid_int))
                now = datetime.now()
                now = now.strftime('%Y-%m-%d %H:%M:%S')      
                mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Informacija', 'Uspjesna provjera sigurnosnih ovlasti za dodavanje novog korisnika'))

                mycursor.execute("TRUNCATE TABLE Users")
                mycursor.execute("TRUNCATE TABLE Devices")
                print("Izbrisane tablice")
                logger.debug("Reset tablica")

                try:
                    mycursor.execute("INSERT INTO Users (Seclev, role) VALUES (%s, %s)", (2, 'original'))
                    lastrow = mycursor.lastrowid
                    lastrow = int(lastrow)
                    try:
                        deviceID = clf.connect(rdwr={'on-connect': lambda tag: False})
                        deviceID = str(deviceID)
                        print(deviceID)
                        print("Uspjesno citanje!")
                        buzzerBeep()

                        mycursor.execute("INSERT INTO Devices (UserId, DeviceId) VALUES (%s,%s)", (lastrow, deviceID))
                        logger.info('Adminu dodijeljen novi uredjaj')
                        now = datetime.now()
                        now = now.strftime('%Y-%m-%d %H:%M:%S')      
                        mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Informacija', 'Dodijeljen novi admin'))
                        pass
                    except:
                        print("Neuspjesno citanje")
                        logger.warning('Neuspjesno dodavanje novog uredjaja adminu')
                        now = datetime.now()
                        now = now.strftime('%Y-%m-%d %H:%M:%S')      
                        mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Upozorenje', 'Neuspjesno dodavanje novog admina'))
                        display.lcd_clear()
                        display.lcd_display_string("Neuspjesno", 1)
                        display.lcd_display_string("Citanje!", 2)
                        buzzerBeep()
                        time.sleep(1)
                        pass
                except:
                    print("Neuspjesno dodavanje admina")
                    pass      
            else:
                logger.warning('Neovlasten pokusaj reseta sustava!')
                now = datetime.now()
                now = now.strftime('%Y-%m-%d %H:%M:%S')      
                mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Upozorenje', 'Neovlasten pokusaj reseta sustava!'))
                sendEmail(2)
                display.lcd_clear()
                display.lcd_display_string("Nemate ovlasti", 1)
                display.lcd_display_string("Za ovu funkciju", 2)
                buzzerBeepAlarm()
                time.sleep(2)
                pass
        except:
            print("Ne valja")
            logger.warning('Neovlasten pokusaj reseta sustava!')
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')      
            mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Upozorenje', 'Neovlasten pokusaj reseta sustava!'))
            sendEmail(2)
            display.lcd_clear()
            display.lcd_display_string("Neuspjesno", 1)
            display.lcd_display_string("Citanje!", 2)
            buzzerBeepAlarm()
            time.sleep(1)
            pass
    else:
        logger.warning('Neovlasten pokusaj reseta sustava!')
        now = datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')      
        mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Upozorenje', 'Neovlasten pokusaj reseta sustava!'))
        sendEmail(2)
        display.lcd_clear()
        display.lcd_display_string("Netocan PIN!", 1)
        buzzerBeepAlarm()
        time.sleep(2)
        pass
    pass
pass

def sendEmail(msg):
    server = smtplib.SMTP('smtp.gmail.com', port)
    try:
        server.ehlo()
        server.starttls()
        server.login(sender_email, password)
        if msg == 1:
            server.sendmail(sender_email, receiver_email, mg1)
        else:
            server.sendmail(sender_email, receiver_email, mg2)
    except Exception as e:
        print(e)
    finally:
        server.quit()

def lockStatus():
    logger.info('Provjera stanja brave')
    now = datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')      
    mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Informacija', 'Prvojera stanja brave'))
    if GPIO.input(relay):
        print("Relej u HIGH")
        display.lcd_clear()
        display.lcd_display_string("Brava je", 1)
        display.lcd_display_string("otkljucana!", 2)
        time.sleep(3)
        pass
    else:
        print("Relej u LOW")
        display.lcd_clear()
        display.lcd_display_string("Brava je", 1)
        display.lcd_display_string("zakljucana!", 2)
        time.sleep(3)
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

def buzzerBeepAlarm():
    i = 0
    while i < 6:
        GPIO.output(buzzer,GPIO.HIGH)
        print("BIIIIP")
        time.sleep(0.3)
        GPIO.output(buzzer,GPIO.LOW)
        print("KRAJ BIIIIP")
        time.sleep(0.1)
        i = i + 1
    pass

def relayOpen():
    #HIGH odgovara jedinci i otkljucanim vratima a LOW nuli i ponovnom zakljucavanju
    GPIO.output(buzzer,GPIO.HIGH)
    print("Otkljucano")
    buzzerBeep()
    display.lcd_clear()
    display.lcd_display_string("Vrata su ", 1)
    display.lcd_display_string("otkljucana!", 2)
    time.sleep(5)
    GPIO.output(buzzer,GPIO.LOW)
    print("Zakljucano")
    pass

def main():
    try:

        while True:
            print("Vrti se pocetni ekran")
            #mycursor.execute("DELETE FROM Logs WHERE")
            display.lcd_clear()
            display.lcd_display_string("Unesite PIN:", 1)
            logger.debug('Program je na pocetnom ekranu')

            #ovo ispod samo za provjeru pravilnog rada baze. Poslije ukloniti
            mycursor.execute("SELECT * FROM Users")
            for x in mycursor:
                print(x)
            mycursor.execute("SELECT * FROM Devices")
            for x in mycursor:
                print(x)
            mycursor.execute("SELECT * FROM Logs")
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
            elif unos == 3:
                print("Provjera stanja brave")
                lockStatus()
                pass
            elif unos == 7:
                print("Resetiranje cijele tablice")
                resetFunction()
                pass
            else:
                #u slucaju pogresnog unosa logirati pokusaj i slati upozorenje
                print("Netocan unos")
                display.lcd_clear()
                display.lcd_display_string("Netocan unos!", 1)
                time.sleep(2)
                logger.warning('Netocan unos na tipkovnici!')
                now = datetime.now()
                now = now.strftime('%Y-%m-%d %H:%M:%S')      
                mycursor.execute("INSERT INTO Logs (dt, logType, logMsg) VALUES (%s, %s, %s)", (now, 'Upozorenje', 'Netocan unos na tipkovnici!'))
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Kraj rada programa")
        clf.close()
        pass    
    GPIO.cleanup()

if __name__ == '__main__':
    main()