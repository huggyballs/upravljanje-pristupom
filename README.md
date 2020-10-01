# upravljanje pristupom
 Repozitorij za sve što je vezano uz diplomski rad na temu izrade sustava za kontrolu pristupa. Sustav se izrađuje pomoću Raspberry Pi 3 B računala i PN532 NFC čitača.

 U ovoj se mapi nalaze sve potrebne datoteke za pravilan rad sustava. To ne uključuje posebne module za čitač i GPIO funkcije RPi-a koji se moraju instalirati putem terminala

 Modul za čitač: https://nfcpy.readthedocs.io/en/latest/index.html
 Svi preduvjeti i dokumentacija na koji se način ova biblioteka općenito koristi nalaze se na ovoj stranici. Kako čitač koristi serijsku UART komunikaciju potrebno ju je prethodno osloboditi u Raspberry Pi-u na način da se zabrani korištenje serijske komunikacije za komunikaciju s kernelom.

 Modul za LCD ekran nalazi se uključen u datotekama. Za njihov pravilan rad potrebno je samo da se nalaze u istom direktoriju kao i kod programa.

 Modul za standardni GPIO: https://pypi.org/project/RPi.GPIO/
 Instalirati i uvesti u kod za upravljanje radom buzzera i releja.

Podešavanje MySQL baze podataka na Pi-u: https://pimylifeup.com/raspberry-pi-mysql/
Sve potrebne upute. Ukoliko se postavi neko drugo korisničko ime i lozinka za korisnika od one koja je navedena u kodu programa, potrebno ju je promijeniti unutar koda kako bi se veza uspješno ostvarila.

NFCASSERT.PY: Jednostavno provjerava da li je čitač pravilno spojen i da li se može uspostaviti veza sa njim preko UART-a. Dobro pokrenuti prije prvog pokretanja glavnog programa. Ukoliko se kod uspješno izvrši uređaj je spreman za korištenje. Ukoliko se vrati greška, treba provjeriti kako je čitač spojen, jesu li postavke pravilno postavljene, i da li se otvara dobar port. Potom pokrenuti ponovno Pi i provjeriti još jednom.

PRVO_DODAVANJE.PY: Baza podataka je u početku prazna. Da bi se se sa sustavom mogla vršiti uspješna interakcija ova skripta dodaje jednog korisnika koji se smatra administratorom sustava. Pokrenuti prije pokretanja glavnog programa.

APRISTUP.PY: Kod glavnog programa sa svim funkcijama

NAPOMENE: Čitač može pravilno raditi samo koristeći python 2.7. Na Pythonu 3 bar meni nikako nije mogao raditi. Funkcija za slanje e-mailova traži da se u kodu definira adresa pošiljatelja i primatelja. Adresa pošiljatelja je već definirana, a adresu primatelja je potrebno još definirati ovisno o kome se upozorenja šalju.
