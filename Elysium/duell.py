# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# dominik.enssle@web.de schrieb diese Datei. Solange Sie diesen Vermerk nicht entfernen, können
# Sie mit dem Material machen, was Sie möchten. Wenn wir uns eines Tages treffen und Sie
# denken, das Material ist es wert, können Sie mir dafür ein Bier ausgeben. Dominik Enßle
# http://de.wikipedia.org/wiki/Beerware
# ----------------------------------------------------------------------------------------------

import socket, time, json, random
from zauber import *
from waffen import *

class Duell:
    def __init__(self, hero):
        self.hero = hero
        self.port = 62531 #port, ab 49152 verwendbar, max ist 65.535
        self.rnd = 0
    
    def lauschen_join(self):
        while True:
            try:
                data = join_verbindung.recv(15360)#maximal 15360 bytes
                try:
                    data2 = json.loads(data)
                    return data2
                except:
                    return data
            except:
                print "Fehler: Keine Verbindung!"
            
    def lauschen_host(self):
        while True:
            try:
                data = host_conn.recv(2048)#maximal 2048 Bytes
                try:
                    data = json.loads(data)
                    return data
                except:
                    return data
            except:
                pass
                
    def senden(self, nachricht):
        try:
            self.nachricht = nachricht
            join_verbindung.send(self.nachricht)
        except:
            print "Sendefehler!"
        time.sleep(0.5)
    
    def senden_host(self, nachricht):
        try:
            self.nachricht = nachricht
            host_conn.send(self.nachricht)
        except:
            print "Host: Sendefehler!"
        time.sleep(0.5)
            
        
    def duellmenue(self):
        while True:
            dwahl = raw_input("Wollen Sie ein Spiel [h]osten oder in ein bestehendes [e]insteigen?\n[A]bbrechen\n")
            if dwahl == "h" or dwahl == "H":
                self.hosten()
                break
            elif dwahl == "e" or dwahl == "e":
                self.join()
                break
            elif dwahl == "a" or dwahl == "A":
                break
            
    def hosten(self):
        global verbindung, host_conn, addr
        verbindung = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET für das IPv4-Protokoll, SOCK_STREAM für die Verwendung von TCP
        verbindung.bind(("", self.port))
        hname = socket.gethostname()#eigener name
        pi = socket.gethostbyname(hname) #eigene ip
        print hname, pi, "READY!"
        verbindung.listen(1)
        host_conn, addr = verbindung.accept() #host_conn ist connection-Objekt / addr = IP-Adresse und Port des verbundenen Sockets
        print "Verbindung wird hergestellt"
        self.hostmenue()
            
    def hostmenue(self):
        while self.hero.ktp > 0:
            print "Sie haben noch", self.hero.ktp, "Trefferpunkte!" 
            print "[A]ngriff, [I]tem oder [F]lucht"
            dkwahl = raw_input("Was wollen Sie tun?\n")
            if dkwahl == "A" or dkwahl == "a":
                self.host_aktionswahl()
            elif dkwahl == "I" or dkwahl == "i":
                pass
            elif dkwahl == "F" or dkwahl == "f":
                verbindung.close()
                break
        
    def host_aktionswahl(self):
        while self.hero.ktp > 0:
            print "[A]ngriff, [M]agieangriff, [Ab]bruch."
            angr = raw_input("Wählen Sie einen Angriff:\n")
            if angr == "Angriff" or angr == "A" or angr == "a":
                self.host_warten()
                self.ablauf("Angriff", self.gwahl)#ob es ein angriff ist / schaden /manakosten/item parameter
                break
            elif angr == "Magie" or angr == "M" or angr == "m":
                Trank_Zauber(self.hero.angriff1)
                z1 =   "\nAngriff [1]:\t" + str(self.hero.angriff1)
                Trank_Zauber(self.hero.angriff2)
                z2 =   "\nAngriff [2]:\t" + str(self.hero.angriff2)
                Trank_Zauber(self.hero.angriff3)
                z3 =   "\nAngriff [3]:\t" + str(self.hero.angriff3)
                print "Wählen Sie einen Zauber:\n", z1, z2, z3, "\n[A]bbrechen."
                magiewahl = raw_input("Welchen Angriff?\n")
                if magiewahl == "1":
                    self.host_warten()
                    self.ablauf(self.hero.angriff1, self.gwahl)
                elif magiewahl == "2":
                    self.host_warten()
                    self.ablauf(self.hero.angriff2, self.gwahl)
                elif magiewahl == "3":
                    self.host_warten()
                    self.ablauf(self.hero.angriff3, self.gwahl)
                elif magiewahl == "Abbrechen" or magiewahl == "A" or magiewahl == "a":
                    break
                break
            elif angr == "Abbruch" or angr == "Ab" or angr == "ab":
                break
            
    def host_warten(self):
        print "Warten auf anderen Spieler."
        self.senden_host("ready")
        self.gwahl = self.lauschen_host()
        
    def join(self):
        global join_verbindung
        join_verbindung = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while self.hero.ktp > 0:
            try:
                ip = raw_input("IP-Adresse:\n[A]bbrechen\n")
                join_verbindung.connect((ip, self.port))
                self.joinmenue()
                break
            except:
                print "IP nicht gefunden"
            if ip == "A" or ip == "a":
                break
            
    def joinmenue(self):
        while self.hero.ktp > 0:
            print "Warten auf anderen Spieler."
            bereitschaft = self.lauschen_join()
            if bereitschaft == "ready":
                print "Sie haben noch", self.hero.ktp, "Trefferpunkte!"
                dkwahl = raw_input("[A]ngriff, [I]tem oder [F]lucht\n")
                if dkwahl == "A" or dkwahl == "a":
                    self.join_aktionswahl()
                elif dkwahl == "I" or dkwahl == "i":
                    pass
                elif dkwahl == "F" or dkwahl == "f":
                    join_verbindung.close
                    break
                        
    def join_aktionswahl(self):
        while True:
            print "[A]ngriff, [M]agieangriff, [Ab]bruch."
            angr = raw_input("Wählen Sie einen Angriff:\n")
            if angr == "Angriff" or angr == "A" or angr == "a":
                zauber = "Angriff"#ob es ein angriff ist / schaden /manakosten/item parameter
                break
            elif angr == "Abbruch" or angr == "Ab" or angr == "ab":
                break
            elif angr == "Magie" or angr == "M" or angr == "m":
                Trank_Zauber(self.hero.angriff1)
                z1 =   "\nAngriff [1]:\t" + str(self.hero.angriff1)
                Trank_Zauber(self.hero.angriff2)
                z2 =   "\nAngriff [2]:\t" + str(self.hero.angriff2)
                Trank_Zauber(self.hero.angriff3)
                z3 =   "\nAngriff [3]:\t" + str(self.hero.angriff3)
                print "Wählen Sie einen Zauber:\n", z1, z2, z3, "\n[A]bbrechen."
                magiewahl = raw_input("Welchen Angriff?\n")
                if magiewahl == "1":
                    zauber = self.hero.angriff1
                    break
                elif magiewahl == "2":
                    zauber = self.hero.angriff2
                    break
                elif magiewahl == "3":
                    zauber = self.hero.angriff3
                    break
                elif magiewahl == "Abbrechen" or magiewahl == "A" or magiewahl == "a":
                    break
        try:
            nachricht = {
                            "zauber":zauber, 
                            "gktp":self.hero.ktp, 
                            "git":self.hero.it,
                            "gkit":self.hero.kit, 
                            "gst":self.hero.st,
                            "gge":self.hero.ge,
                            "grk":self.hero.rk,
                            "git":self.hero.it,
                            "gwaffe":self.hero.waffe,
                        }
            join_verbindung.send(json.dumps(nachricht))
            
        except:
            print "Sendefehler"
        self.join_ablauf()
                
    def join_ablauf(self):
        antwort = None
        while antwort != "Sieg!" or antwort != "Niederlage!":
            antwort = self.lauschen_join()
            if type(antwort) is dict:
                self.hero.ktp = antwort["ktp"]
                self.hero.kit = antwort["kit"]
                break
            elif antwort == "Sieg!" or antwort == "Niederlage!":
                print antwort
                break
            else:
                print antwort
        self.joinmenue()
                    
    def ablauf(self, angriff0, wahl):
        self.angriff0   =   angriff0
        self.itemname   =   Trank_Zauber(self.angriff0).name()
        self.wirkung    =   Trank_Zauber(self.angriff0).wirkung()
        self.ziel       =   Trank_Zauber(self.angriff0).ziel()
        self.nutzbar    =   Trank_Zauber(self.angriff0).nutzbar()
        self.wert       =   Trank_Zauber(self.angriff0).wert()
        self.rnd        += 1
        self.wahl       =   wahl
        self.gst        =   self.wahl["gst"]
        self.gangriff   =   self.wahl["zauber"]
        self.grk        =   self.wahl["grk"]
        self.gge        =   self.wahl["gge"]
        self.gkit       =   self.wahl["gkit"]
        self.gktp       =   self.wahl["gktp"]
        self.git        =   self.wahl["git"]
        self.gwaffe     =   self.wahl["gwaffe"]
        
        self.itemnameg  =   Trank_Zauber(self.gangriff).name()
        self.wirkungg   =   Trank_Zauber(self.gangriff).wirkung()
        self.zielg      =   Trank_Zauber(self.gangriff).ziel()
        self.nutzbarg   =   Trank_Zauber(self.gangriff).nutzbar()
        self.wertg      =   Trank_Zauber(self.gangriff).wert()
        rndtext = "\nRunde #" + str(self.rnd)
        print rndtext
        self.senden_host(rndtext)
        wurfel = random.randint(1, 20)
        gwurfel = random.randint(1, 20)
        wurfel2 = random.randint(1, 20)
        gwurfel2 = random.randint(1, 20)
        if self.hero.ge + wurfel > self.gge + gwurfel:#spieler schneller
            self.spieleraktion(wurfel2, gwurfel2)
            self.gegneraktion(wurfel2, gwurfel2)
        elif self.hero.ge + wurfel < self.gge + gwurfel:#gegner schneller
            self.gegneraktion(wurfel2, gwurfel2)
            self.spieleraktion(wurfel2, gwurfel2)
        else:#gleichstand
            if self.hero.ge >= self.gge:#spielr schneller
                self.spieleraktion(wurfel2, gwurfel2)
                self.gegneraktion(wurfel2, gwurfel2)
            else:#gegner schneller
                self.gegneraktion(wurfel2, gwurfel2)
                self.spieleraktion(wurfel2, gwurfel2)
        nachricht = {"ktp":self.gktp, "kit":self.gkit}
        host_conn.send(json.dumps(nachricht))
        
        
    def gegneraktion(self, wurfel2, gwurfel2):
        if self.gktp >= 1:
            text = "Sie sind am Zug!"
            self.senden_host(text)
            print "Der Gegner ist am Zug!"
            self.wurfel2 = wurfel2
            self.gwurfel2 = gwurfel2
            if (self.wert == None):#angriff
                if (self.hero.ge + self.wurfel2 < self.gge + self.gwurfel2) and (self.gkit >= self.zielg) and self.nutzbarg == False: #treffer, spieler physischer angriff
                    self.physischer_angriff_client()
                elif (self.hero.ge + self.wurfel2 < self.gge + self.gwurfel2) and (self.gkit >= self.zielg) and self.nutzbarg == True: #treffer, spieler magieangriff
                    self.magischer_angriff_client()
                elif self.gkit < self.zielg:#kein Mana 
                    text = "Zu wenig Mana, der Zauber wurde ein Rohrkrepierer!"
                    print "Dein Gegner wollte zaubern, scheiterte aber!"
                    self.senden_host(text)
                else: #daneben, spieler    
                    text = "Sie haben den Gegner verfehlt!"
                    self.senden_host(text)
                    print "Der Gegner schlug daneben!"
                    self.gkit -= self.zielg
            elif (self.wertg != None) and (self.zielg == 1) and (self.nutzbarg == True):#item benutzen: heiltrank
                self.hero.heilung(self.wirkung)
            elif (self.wertg != None) and (self.zielg == 2) and (self.nutzbarg == True):#item: Manatrank
                self.hero.heilung(self.wirkung)
            elif (self.wertg != None) and (self.nutzbarg != True):
                print "Dieses Item ist im Kampf nicht nutzbar."
                text = "Gegner Item Fail!"
                self.senden_host(text)
        self.kampfende_check(self.hero.kit, self.gktp, self.gkit)

    def spieleraktion(self, wurfel2, gwurfel2):
        if self.hero.ktp >= 1:
            print "Sie sind am Zug!"
            text = "Der Gegner ist dran"
            self.senden_host(text)
            self.wurfel2 = wurfel2
            self.gwurfel2 = gwurfel2
            if (self.wert == None):#angriff
                if (self.hero.ge + self.wurfel2 > self.gge + self.gwurfel2) and (self.hero.kit >= self.ziel) and self.nutzbar == False: #treffer, spieler physischer angriff
                    self.physischer_angriff()
                elif (self.hero.ge + self.wurfel2 > self.gge + self.gwurfel2) and (self.hero.kit >= self.ziel) and self.nutzbar == True: #treffer, spieler magieangriff
                    self.magischer_angriff()
                elif self.hero.kit < self.ziel:#kein Mana 
                    print "Zu wenig Mana, der Zauber wurde ein Rohrkrepierer!"
                    text = "Der Zauber des Gegners scheitert"
                    self.senden_host(text)
                else: #daneben, spieler    
                    print "Sie haben den Gegner verfehlt!"
                    text = "Der Gegner schlug daneben!"
                    self.senden_host(text)
                    self.hero.kit -= self.ziel
            elif (self.wert != None) and (self.ziel == 1) and (self.nutzbar == True):#item benutzen: heiltrank
                self.hero.heilung(self.wirkung)
            elif (self.wert != None) and (self.ziel == 2) and (self.nutzbar == True):#item: Manatrank
                self.hero.heilung(self.wirkung)
            elif (self.wert != None) and (self.nutzbar != True):
                print "Dieses Item ist im Kampf nicht nutzbar."
                text = "Item nutzen gescheitert"
                self.senden_host(text)
        self.kampfende_check(self.hero.kit, self.gktp, self.gkit)

    def kampfende_check(self, gktp, ktp, gkit):
        self.gkit = gkit
        self.gktp = gktp
        self.ktp = ktp
        
        if self.gktp <= 0:
            print "Sie haben gewonnen!"
            text = "Niederlage!"
            self.senden_host(text)
        elif self.ktp <= 0:
            print "Sie haben verloren!"
            text = "Sieg!"
            self.senden_host(text)

    def physischer_angriff(self):
        print "Ihr", self.itemname, "trifft den Gegner!"
        text = "Der Genger trifft Sie mit seinem" + self.itemname + "!"
        self.senden_host(text)
        try:
            schaden = random.randint(1, self.wirkung + self.hero.st + Ausruestung(self.hero.waffe).bonus())
            self.gktp -= (schaden * self.grk) / self.grk
        except:
            waffenlos = random.randint(1, self.wirkung + self.hero.st)
            self.gktp -= (waffenlos * self.grk) / self.grk                     
        self.hero.kit -= self.ziel

    def magischer_angriff(self):
        print "Mit einer Handbewegung entfesseln Sie einen", self.itemname, "!"
        text = "Der Gegner entfesselte einen" + self.itemname + "!"
        self.senden_host(text)
        schaden = self.wirkung + self.hero.it
        self.gktp -= (random.randint(1, schaden))
        self.hero.kit -= self.ziel

    def physischer_angriff_client(self):
        text = "Ihr" + str(self.gangriff) + "trifft den Gegner!"
        print "Der Genger trifft Sie mit seinem", self.gangriff,"!"
        self.senden_host(text)
        try:
            schaden = random.randint(1, self.wirkungg + self.gst + Ausruestung(self.gwaffe).bonus())
            self.hero.ktp -= (schaden * self.hero.rk) / self.hero.rk
        except:
            waffenlos = random.randint(1, self.wirkungg + self.gst)
            self.hero.ktp -= (waffenlos * self.grk) / self.grk                     
        self.hero.kit -= self.ziel

    def magischer_angriff_client(self):
        text = "Mit einer Handbewegung entfesseln Sie einen " + str(self.gangriff) + "!"
        print "Der Gegner entfesselte einen ", self.gangriff, "!"
        self.senden_host(text)
        schaden = self.wirkungg + self.git
        self.hero.ktp -= (random.randint(1, schaden))
        self.gkit -= self.ziel