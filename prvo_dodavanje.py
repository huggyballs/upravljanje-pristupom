#ovu skriptu izvrsiti prije pokretanja glavnog programa ukoliko ne postoji nijedan dodani korisnik i uredjaj u bazi podataka
#novi ce korisnik imati administratorske ovlasti i preko njega ce se moci dodavati ostali

import nfc
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="emovis",
    passwd="emovis",
    database="kontrolapristupa",
    autocommit=True
    )
mycursor = db.cursor(buffered=True)

try:
    mycursor.execute("CREATE TABLE Users (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Seclev ENUM('1', '2') NOT NULL, role VARCHAR(10) NOT NULL)")
    pass
except:
    print("postoji")
    pass
try:
    mycursor.execute("CREATE TABLE Devices (DeviceNum int PRIMARY KEY NOT NULL AUTO_INCREMENT, UserId int NOT NULL, DeviceId VARCHAR(40) NOT NULL)")
    pass
except:
    print("postoji")
    pass

clf = nfc.ContactlessFrontend()
clf.open('ttyAMA0')

try:
    mycursor.execute("INSERT INTO Users (Seclev, role) VALUES (%s, %s)", (2, 'original'))
    lstrow = mycursor.lastrowid
    lstrow = int(lstrow)
    try:
        devID = clf.connect(rdwr={'on-connect': lambda tag: False})
        devID = str(devID)
        print(devID)
        print("Uspjesno citanje!")

        mycursor.execute("INSERT INTO Devices (UserId, DeviceId) VALUES (%s,%s)", (lstrow, devID))
        pass
    except:
        print("Neuspjesno citanje")
        pass
except:
    print("Neuspjesno dodavanje admina")
    pass

clf.close()