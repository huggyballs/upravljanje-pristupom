#ova skripta se pokrece prije pokretanja glavnog programa
#sluzi za provjeru pravilne podesenosti citaca

import nfc

clf = nfc.ContactlessFrontend()
try:
    assert clf.open('tty:AMA0') is True
    print("Obavljeno!")
    pass
except:
    print("Citac nije pravilno spojen!")
    pass
finally:
    clf.close()
    pass
