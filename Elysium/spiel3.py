# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# dominik.enssle@web.de schrieb diese Datei. Solange Sie diesen Vermerk nicht entfernen, können
# Sie mit dem Material machen, was Sie möchten. Wenn wir uns eines Tages treffen und Sie
# denken, das Material ist es wert, können Sie mir dafür ein Bier ausgeben. Dominik Enßle
# http://de.wikipedia.org/wiki/Beerware
# ----------------------------------------------------------------------------------------------

import random, time, pickle
from duell import *
from zauber import *
from waffen import *

class Held:
    def __init__(self, spielstand):
        self.spielstand  =   spielstand
        self.attribute   =   self.spielstand["attribute"]
        self.angriffe    =   self.spielstand["angriffe"]
        self.ausruestung =   self.spielstand["ausruestung"]

        self.name        =   self.attribute["name"]
        self.st          =   self.attribute["st"]#st ärke
        self.ge          =   self.attribute["ge"]#ge schick
        self.rk          =   self.attribute["rk"]#rüstungsklasse
        self.tp          =   self.attribute["tp"]#trefferpunkte
        self.ktp         =   self.attribute["ktp"]#reduzierbare kampftrefferpunkte
        self.it          =   self.attribute["it"]#intelligenz
        self.kit         =   self.attribute["kit"]#aka mana
        self.geld        =   self.ausruestung["geld"]#money, money, money
        self.ep          =   self.attribute["ep"]#erfahrungspunkte
        self.dep         =   self.attribute["dep"]#differenz bis zum nächsten lvl up
        self.level       =   self.attribute["level"]
        self.angriff1    =   self.angriffe["angriff1"]
        self.angriff2    =   self.angriffe["angriff2"]
        self.angriff3    =   self.angriffe["angriff3"]
        self.zauber      =   self.angriffe["zauber"]
        self.inventar    =   self.ausruestung["inventar"]
        self.waffe       =   self.ausruestung["waffe"]
        self.panzer      =   self.ausruestung["panzer"]
        self.accessoire  =   self.ausruestung["accessoire"]

        self.ruck        =   Item(self.st)#das inventar des helden
        self.arsenal     =   Item(self.st)#seine zaubersammlung/ attackensammlung

        self.ruck.rucksack = self.inventar.copy()
        self.arsenal.rucksack = self.zauber.copy()

        self.arsenal.hinzufuegen(self.angriff1, 1)#angriffe werden ins inventar geladen
        self.arsenal.hinzufuegen(self.angriff2, 1)
        self.arsenal.hinzufuegen(self.angriff3, 1)

    def __str__(self):  # überschrift von Status sowie Name
        output = "\nStatus \nName:\t\t\t" + self.name
        return output

    def levelup(self):
        self.level += 1#spielerlvl wird angehoben
        self.dep = self.dep * self.level#neue differenz zum nächsten lvl up
        print "Sie sind um ein Level gestiegen!"
        self.plus = 2#bonus um den ein attribut angehoben werden darf
        print "Jetzt dürfen Sie eins ihrer Attribute erhöhen. \nZur Wahl stehen: [St]ärke, [Ge]schicklichkeit, [In]telligenz, [T]refferpunkte oder [R]üstungsklasse."
        attributplus = raw_input("Welches Attribut wollen Sie verbessern?\n")
        if attributplus == "St" or attributplus == "st":
            self.st += self.plus
            self.levelup_zauber("Stärke")
        elif attributplus == "Ge" or attributplus == "ge":
            self.ge += self.plus
            self.levelup_zauber("Geschick")
        elif attributplus == "In" or attributplus == "in":
            self.it += self.plus
            self.levelup_zauber("Intelligenz")
        elif attributplus == "T" or attributplus == "t":
            self.tp += self.plus
            self.levelup_zauber("Trefferpunkte")
        elif attributplus == "R" or attributplus == "r":
            self.rk += self.plus
            self.levelup_zauber("Rüstungsklasse")
        else:
            print "Bitte was?"

    def levelup_zauber(self, verbessertes):
        self.verbessertes = verbessertes
        print "Deine", self.verbessertes, "wurde um", self.plus, "erhöht."

    def itemnutzen(self):
        while True:
            item = self.ruck.item_waehlen()
            try:
                self.itemnutzen_trank(item)
                break
            except:
                try:
                    self.itemnutzen_ausruestung(item)
                    break
                except ValueError:
                    pass

    def itemnutzen_trank(self, item):
        self.item = item
        wirkung = Trank_Zauber(self.item).wirkung()
        ziel = Trank_Zauber(self.item).ziel()
        if ziel == 1:#item benutzen: heiltrank
            self.heilung(wirkung)
        elif ziel == 2:#mana
            self.manaheilung(wirkung)

    def itemnutzen_ausruestung(self, item):
        self.item = item
        name = Ausruestung(self.item).name()
        bonus = Ausruestung(self.item).bonus()
        ziel = Ausruestung(self.item).ziel()
        typ = Ausruestung(self.item).typ()
        if (typ == 1) and (self.waffe == None):#keine waffe aktiv, neue waffe anlegen
            self.waffe = name
        elif (typ == 1) and (self.waffe != None):#waffe aktiv, alte ablegen und neue anlegen
            self.ruck.hinzufuegen(self.waffe, 1)
            self.waffe = name
        elif (typ == 2) and self.panzer == None:#kein panzer an; neuen panzer anlegen
            self.panzer = name
            self.rk += bonus
        elif (typ == 2) and self.panzer != None:#panzer angelegt, alten panzer ablegen und neuen anziehen
            self.ruck.hinzufuegen(self.panzer, 1)
            self.rk -= Ausruestung(self.panzer).bonus()
            self.panzer = name
            self.rk += bonus
        elif (typ == 3) and self.accessoire == None:#kein accessoire angelegt, neues wird angezogen
            pass
        elif (typ == 3) and self.accessoire != None:#accessoire angelegt, wir ausgezogen und neues angelegt
            self.ruck.hinzufuegen(self.accessoire, 1)
        print name, "wurde angelegt."

    def heilung(self, wirkung):
        self.wirkung = wirkung
        heil = self.tp - self.ktp
        if self.wirkung > heil:
            self.ktp += heil
            print "Das Item heilt dir:",heil,"TP."
        else:
            self.ktp += wirkung
            print "Das Item heilt dir ", self.wirkung, "TP."

    def manaheilung(self, wirkung):
        self.wirkung = wirkung
        heil = self.it - self.kit
        if self.wirkung > heil:
            self.kit += heil
            print "Das Item stellte dir", heil, "Mana wieder her."
        else:
            self.kit += wirkung
            print "Das Item stellte dir", self.wirkung, "Mana wieder her."


class Item:
    def __init__(self, st):
        self.st = st
        self.rucksack = {}
        self.rucksackgrosse = self.st - 6 #plus stärke
        self.platz = self.rucksackgrosse - len(self.rucksack)

    def anzeigen(self):
        for x in self.rucksack.items():
            print x
        print "Sie haben noch", self.platz, "von", self.rucksackgrosse, "Plätzen frei."

    def hinzufuegen(self, add, anzahl):
        self.add = add
        self.anzahl = anzahl
        if self.add in self.rucksack:
            plus = self.rucksack[self.add]
            plus += self.anzahl
            self.rucksack[self.add] = plus
        else:
            self.rucksack[self.add] = self.anzahl
        self.platz = self.rucksackgrosse - len(self.rucksack)

    def entfernen(self, ent, anzahl):
        self.ent = ent
        self.anzahl = anzahl
        if self.ent in self.rucksack:
            minus = self.rucksack[self.ent]
            minus -= self.anzahl
            self.rucksack[self.ent] = minus
            if self.rucksack[self.ent] == 0:
                del self.rucksack[self.ent]
        self.platz = self.rucksackgrosse - len(self.rucksack)

    def item_waehlen(self):
        self.anzeigen()
        while True:
            rwahl = raw_input("Welches Item wollen Sie benutzen?\n[A]bbrechen\n")
            if (rwahl in self.rucksack) and (rwahl != "Abbrechen") and (rwahl != "A") and (rwahl != "a"):
                self.entfernen(rwahl, 1)
                return rwahl
            elif rwahl == "Abbrechen" or rwahl == "A" or rwahl == "a":
                break
            else:
                print "Entweder Sie haben das Item verbraucht oder eine Fee hat es geklaut oder Sie hatten es nie."
                return None

    def ausruestung_waehlen(self):
        print self.rucksack
        while True:
            awahl = raw_input("Welche Ausrüstung wollen Sie anlegen?\n[A]bbrechen\n")
            if (awahl in self.rucksack) and (awahl != "Abbrechen") and (awahl != "A") and (awahl != "a"):
                self.entfernen(awahl, 1)
                return awahl
            elif awahl == "Abbrechen" or awahl == "A" or awahl == "a":
                break

class Gegner:
    def __init__(self, name, von, bis, gangriff1, gangriff2, gangriff3):#die grenzen der Werte des Gegners; seine 3 Angriffe
        self.gname  =   name
        self.gst    =   random.randint(von, bis)
        self.gge    =   random.randint(von, bis)
        self.grk    =   random.randint(von, bis)
        self.gtp    =   random.randint(von, bis)
        self.gktp   =   random.randint(von, bis)
        self.gkit   =   random.randint(von, bis)
        self.gangriff1 = gangriff1
        self.gangriff2 = gangriff2
        self.gangriff3 = gangriff3

class Kampf:
    def __init__(self, hero, gegn):
        self.hero = hero
        self.gegn = gegn
        self.rnd = 0

    def kampfmenue(self):
        geldauswirkung = random.randint(1, self.gegn.gst)#geldgewinn bei sieg oder geldverlust bei niederlage
        epplus = random.randint(1, self.gegn.gge + self.rnd)#ep gewinn bei sieg
        while (self.hero.ktp > 0) and (self.gegn.gktp > 0):#solange noch einer der beiden tp hat gehts weiter
            print "\nKampfmenue!\nSie haben noch", self.hero.ktp, "von", self.hero.tp, "Trefferpunkte."
            print "Und", self.hero.kit, "von", self.hero.it, "Manapunkte."
            awahl = raw_input("Was wollen Sie tun?\n[A]ngriff, [I]tems oder [F]lucht.\n")
            if awahl == "Angriff" or awahl == "a" or awahl == "A":
                self.aktionswahl()
            elif awahl == "Items" or awahl == "i" or awahl == "I":
                try:
                    item = self.hero.ruck.item_waehlen()
                    print item
                    if item != None:
                        self.ablauf(item)
                except:
                    pass
            elif awahl == "Flucht" or awahl == "f" or awahl == "F":
                break

        if self.hero.ktp <= 0 and self.gegn.gktp > 0:#bedingung: niederlagen
            print "\nVerloren!"
            self.hero.geld -= geldauswirkung
            print "Sie haben ", geldauswirkung, "Münzen verloren!"
        elif self.hero.ktp > 0 and self.gegn.gktp <= 0:#bedingung: sieg
            print "\nGewonnen!"
            self.hero.geld += geldauswirkung
            self.hero.ep += epplus
            print "Sie haben", geldauswirkung, "Münzen und",epplus, "EP gewonnen!"
            if self.hero.ep >= self.hero.dep:
                self.hero.levelup()#test auf levelaustieg und durchführung

    def aktionswahl(self):
        while True:
            print "[A]ngriff, [M]agieangriff, [Ab]bruch."
            angr = raw_input("Wählen Sie einen Angriff:\n")
            if angr == "Angriff" or angr == "A" or angr == "a":
                self.ablauf("Angriff")#ob es ein angriff ist / schaden /manakosten/item parameter
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
                    self.ablauf(self.hero.angriff1)
                elif magiewahl == "2":
                    self.ablauf(self.hero.angriff2)
                elif magiewahl == "3":
                    self.ablauf(self.hero.angriff3)
                elif magiewahl == "Abbrechen" or magiewahl == "A" or magiewahl == "a":
                    break
                break

            elif angr == "Abbruch" or angr == "Ab" or angr == "ab":
                break

    def ablauf(self, angriff0):
        self.angriff0   =   angriff0
        self.itemname   =   Trank_Zauber(self.angriff0).name()
        self.wirkung    =   Trank_Zauber(self.angriff0).wirkung()
        self.ziel       =   Trank_Zauber(self.angriff0).ziel()
        self.nutzbar    =   Trank_Zauber(self.angriff0).nutzbar()
        self.wert       =   Trank_Zauber(self.angriff0).wert()
        self.rnd += 1
        print "\nRunde #", self.rnd
        wurfel = random.randint(1, 20)
        gwurfel = random.randint(1, 20)
        wurfel2 = random.randint(1, 20)
        gwurfel2 = random.randint(1, 20)
        if self.hero.ge + wurfel > self.gegn.gge + gwurfel:#spieler schneller
            self.spieleraktion(wurfel2, gwurfel2)
            self.gegneraktion(wurfel2, gwurfel2)
        elif self.hero.ge + wurfel < self.gegn.gge + gwurfel:#gegner schneller
            self.gegneraktion(wurfel2, gwurfel2)
            self.spieleraktion(wurfel2, gwurfel2)
        else:#gleichstand
            if self.hero.ge >= self.gegn.gge:#spielr schneller
                self.spieleraktion(wurfel2, gwurfel2)
                self.gegneraktion(wurfel2, gwurfel2)
            else:#gegner schneller
                self.gegneraktion(wurfel2, gwurfel2)
                self.spieleraktion(wurfel2, gwurfel2)

    def gegneraktion(self, wurfel2, gwurfel2):
        if self.gegn.gktp >= 1:
            print "Der Gegner ist am Zug:"
            self.wurfel2 = wurfel2
            self.gwurfel2 = gwurfel2
            if (self.gegn.gge + self.gwurfel2 > self.hero.ge + self.wurfel2): #treffer gegner
                gangriffwahl = random.randint(1, 3)
                if gangriffwahl == 1:
                    gangriff = Trank_Zauber(self.gegn.gangriff1).name()
                elif gangriffwahl == 2:
                    gangriff = Trank_Zauber(self.gegn.gangriff2).name()
                else:
                    gangriff = Trank_Zauber(self.gegn.gangriff3).name()
                print "Der", self.gegn.gname, "trifft Sie mit seinem", Trank_Zauber(gangriff).name(), "."
                schaden = random.randint(1, Trank_Zauber(gangriff).wirkung() + self.gegn.gst)
                self.hero.ktp -= (schaden * self.hero.rk) / self.hero.rk
            else: #daneben, gegner
                print "Der", self.gegn.gname, "schlug daneben!"

    def spieleraktion(self, wurfel2, gwurfel2):
        if self.hero.ktp >= 1:
            print "Sie sind am Zug:"
            self.wurfel2 = wurfel2
            self.gwurfel2 = gwurfel2
            if (self.wert == None):#angriff
                if (self.hero.ge + self.wurfel2 > self.gegn.gge + self.gwurfel2) and (self.hero.kit >= self.ziel) and self.nutzbar == False: #treffer, spieler physischer angriff
                    self.physischer_angriff()
                elif (self.hero.ge + self.wurfel2 > self.gegn.gge + self.gwurfel2) and (self.hero.kit >= self.ziel) and self.nutzbar == True: #treffer, spieler magieangriff
                    self.magischer_angriff()
                elif self.hero.kit < self.ziel:#kein Mana
                    print "Zu wenig Mana, der Zauber wurde ein Rohrkrepierer!"
                else: #daneben, spieler
                    print "Sie haben den Gegner verfehlt!"
                    self.hero.kit -= self.ziel
            elif (self.wert != None) and (self.ziel == 1) and (self.nutzbar == True):#item benutzen: heiltrank
                self.hero.heilung(self.wirkung)
            elif (self.wert != None) and (self.ziel == 2) and (self.nutzbar == True):#item: Manatrank
                self.hero.heilung(self.wirkung)
            elif (self.wert != None) and (self.nutzbar != True):
                print "Dieses Item ist im Kampf nicht nutzbar."

    def physischer_angriff(self):
        print "Ihr", self.itemname, "trifft den Gegner!"
        try:
            schaden = random.randint(1, self.wirkung + self.hero.st + Ausruestung(self.hero.waffe).bonus())
            self.gegn.gktp -= (schaden * self.gegn.grk) / self.gegn.grk
        except:
            waffenlos = random.randint(1, self.wirkung + self.hero.st)
            self.gegn.gktp -= (waffenlos * self.gegn.grk) / self.gegn.grk
        self.hero.kit -= self.ziel

    def magischer_angriff(self):
        print "Mit einer Handbewegung entfesseln Sie einen", self.itemname, "!"
        schaden = self.wirkung + self.hero.it
        self.gegn.gktp -= (random.randint(1, schaden))
        self.hero.kit -= self.ziel

class Handel:
    def __init__(self, hero):
        self.hero = hero

    def handelsmenue(self):
        while True:
            ver_kauf = raw_input("Wollen Sie [k]aufen oder [v]erkaufen?\n[A]bbrechen\n")
            if ver_kauf == "kaufen" or ver_kauf == "k" or ver_kauf == "K":
                self.kaufen()
                break
            elif ver_kauf == "verkaufen" or ver_kauf == "v" or ver_kauf == "V":
                self.verkaufen()
                break
            elif ver_kauf == "Abbrechen" or ver_kauf == "A" or ver_kauf == "a":
                break

    def kaufen(self):
        self.preisliste()
        while True:
            k_wahl = raw_input("Was wollen Sie kaufen?\n[A]bbrechen\n")
            try:
                self.kaufen_trank(k_wahl)
                break
            except ValueError:
                try:
                    self.kaufen_ausruestung(k_wahl)
                    break
                except ValueError:
                    pass

            if k_wahl == "Abbrechen" or k_wahl == "A" or k_wahl == "a":
                print "Bis zum nächsten mal!"
                break

    def preisliste(self):
        liste = {
                    #Tränke
                    "Trank":Trank_Zauber("Trank").wert(),
                    "Supertrank":Trank_Zauber("Supertrank").wert(),
                    "Manatrank":Trank_Zauber("Manatrank").wert(),
                    "Heilsalbe":Trank_Zauber("Heilsalbe").wert(),
                    #Waffen
                    "Dolch":Ausruestung("Dolch").preis(),
                    "Morgenstern":Ausruestung("Morgenstern").preis(),
                    "Axt":Ausruestung("Axt").preis(),
                    "Kurzschwert":Ausruestung("Kurzschwert").preis(),
                    "Kampfstab":Ausruestung("Kampfstab").preis(),
                    "Rapier":Ausruestung("Rapier").preis(),
                    "Streitkolben":Ausruestung("Streitkolben").preis(),
                    "Pike":Ausruestung("Pike").preis(),
                    "Langschwert":Ausruestung("Langschwert").preis(),
                    "Streithammer":Ausruestung("Streithammer").preis(),
                    "Streitaxt":Ausruestung("Streitaxt").preis(),
                    "Bastardschwert":Ausruestung("Bastardschwert").preis(),
                    "Krummschwert":Ausruestung("Krummschwert").preis(),
                    #Rüstung
                    "Waffenrock":Ausruestung("Waffenrock").preis(),
                    "Lederpanzer":Ausruestung("Lederpanzer").preis(),
                    "Fellweste":Ausruestung("Fellweste").preis(),
                    "Kettenhemd":Ausruestung("Kettenhemd").preis(),
                    "Ringpanzer":Ausruestung("Ringpanzer").preis(),
                    "Schuppenpanzer":Ausruestung("Schuppenpanzer").preis(),
                    "Schienenpanzer":Ausruestung("Schienenpanzer").preis(),
                    "Feldharnisch":Ausruestung("Feldharnisch").preis(),
                    "Vollharnisch":Ausruestung("Vollharnisch").preis(),
                    "Mithrilpanzer":Ausruestung("Mithrilpanzer").preis(),
                    "Drachenharnisch":Ausruestung("Drachenharnisch").preis(),
                    "Adamantiumpanzer":Ausruestung("Adamantiumpanzer").preis(),
                    #accessoires
                    "TPRing":Ausruestung("TPRing").preis(),
                    "Manaring":Ausruestung("Manaring").preis()
                    }

        for x in liste.items():
            print x

    def kaufen_trank(self, k_wahl):
        self.k_wahl = k_wahl
        wert = Trank_Zauber(self.k_wahl).wert()
        menge = int(raw_input("Wie viele?\n"))
        preis = wert * menge
        print "Das würde", preis, "kosten."
        while True:
            preis_antwort = raw_input("Ok? [J]a / [N]ein\n")
            if preis_antwort == "J" or preis_antwort == "j":
                if self.hero.geld >= preis and (self.hero.ruck.platz >= 1 or k_wahl in self.hero.ruck.rucksack):
                    self.hero.ruck.hinzufuegen(self.k_wahl, menge)
                    self.hero.geld -= preis
                    print menge, self.k_wahl, "wurde für", preis, "gekauft."
                    break
                elif self.hero.geld < preis and self.hero.ruck.platz >= 1:
                    print "Das würde", preis, "kosten, Sie haben aber nur noch", self.hero.geld, "."
                else:
                    print "Kein Platz."
                    break
            elif preis_antwort == "N" or preis_antwort == "n":
                break

    def kaufen_ausruestung(self, k_wahl):
        self.k_wahl = k_wahl
        preis = Ausruestung(self.k_wahl).preis()
        if self.hero.geld >= preis and (self.hero.ruck.platz >= 1 or k_wahl in self.hero.ruck.rucksack):
            self.hero.ruck.hinzufuegen(self.k_wahl, 1)
            self.hero.geld -= preis
            print "Ein", k_wahl, "wurde für", preis, "gekauft."
        elif self.hero.geld < preis and self.hero.ruck.platz >= 1:
            print "Das würde", preis, "kosten, Sie haben aber nur noch", self.hero.geld, "."
        else:
            print "Kein Platz."

    def verkaufen(self):
        while True:
            print "Sie haben folgenden Besitz:\n", self.hero.ruck.anzeigen()
            v_kauf = raw_input("Was wollen Sie verkaufen?\n")
            if v_kauf in self.hero.ruck.rucksack:
                menge = int(raw_input("Wie viel wollen Sie verkaufen?\n"))
                try:
                    wert = Trank_Zauber(v_kauf).wert()
                    preis = (wert / 2) * menge
                    if self.hero.ruck.rucksack[v_kauf] >= menge:
                        self.hero.ruck.entfernen(v_kauf, menge)
                        self.hero.geld += preis
                        print "Dafür bekommen Sie", preis, "Münzen."
                        break
                    else:
                        print "Ungültige Eingabe."
                except:
                    try:
                        wert = Ausruestung(v_kauf).preis()
                        preis = (wert / 2) * menge
                        if self.hero.ruck.rucksack[v_kauf] >= menge:
                            self.hero.ruck.entfernen(v_kauf, menge)
                            self.hero.geld += preis
                            print "Dafür bekommen Sie", preis, "Münzen."
                            break
                        else:
                            print "Ungültige Eingabe."
                    except:
                        pass
            else:
                print "Nichts mit diesem Namen gefunden."
                break

class Elysium:
    def start(self):#speichern oder laden, das ist hier die Frage.
        print "\nELYSIUM 1.5"
        hero = None
        while hero == None:
            laden_oder_neu = raw_input("Wollen Sie ein [n]eues Spiel beginnen oder einen alten Spielstand [l]aden?\n")
            if laden_oder_neu == "laden" or laden_oder_neu == "l":
                try:
                    hero = Held(self.laden())
                except:
                    print "Oh dear, Spielstand nicht gefunden."
            elif laden_oder_neu == "neu" or laden_oder_neu == "n" or laden_oder_neu == "neues":
                try:
                    hero = Held(self.neu())
                except:
                    pass
        self.mainloop(hero)

    def laden(self):
        laden = raw_input("Welchen Spielstand möchten Sie laden?\n")
        ladename    =   laden + ".pkmn"
        ladestand   =   open(ladename, "r")#r für read
        ladeliste   =   pickle.load(ladestand)
        attribute   =   ladeliste["attribute"]
        angriffe    =   ladeliste["angriffe"]
        ausruestung =   ladeliste["ausruestung"]
        spielstand  =   {"attribute":attribute, "angriffe":angriffe, "ausruestung":ausruestung}
        ladestand.close()
        print "Spielstand erfolgreich geladen."
        return spielstand


    def neu(self):
        name = raw_input("\nName, bitte:\n")
        if name != "":
            spielstand = {
                            "attribute":{
                                        "tp": 15,
                                        "ktp": 15,
                                        "st": 10,
                                        "ge": 10,
                                        "rk": 10,
                                        "it": 10,
                                        "kit": 10,
                                        "name": name,
                                        "ep": 0,
                                        "dep": 25,
                                        "level": 1
                                        },
                            "angriffe":{"zauber": {},
                                        "angriff1": "Feuerball",
                                        "angriff2": "Angriff",
                                        "angriff3": "Angriff"
                                        },
                            "ausruestung":{"geld": 35,
                                        "inventar": {},
                                        "waffe": None,
                                        "panzer": None,
                                        "accessoire": None
                                        }
                        }

            return spielstand
        else:
            print "Leere Eingabe!"
            return None

    def mainloop(self, hero):
        self.hero = hero
        while True:
            print "\nMenue\n[S]tatus, [I]tems, [K]ampf, [D]uell, [Sp]eichern, [H]ändler oder [Q]uit."
            antwort = raw_input("Was wollen Sie tun?\n")
            if antwort == "Status"      or antwort == "S"   or antwort == "s":
                self.status()
            elif antwort == "Items"     or antwort == "I"   or antwort == "i":
                self.hero.itemnutzen()
            elif antwort == "Kampf"     or antwort == "K"   or antwort == "k":
                self.gegnerwahl()
            elif antwort == "Duell"     or antwort == "D"   or antwort == "d":
                Duell(hero).duellmenue()
            elif antwort == "Speichern" or antwort == "Sp"  or antwort == "sp":
                self.speichern()
            elif antwort == "Händler"   or antwort == "H"   or antwort == "h":
                Handel(hero).handelsmenue()
            elif antwort == "Quit"      or antwort == "Q"   or antwort == "q":
                print "\nGood Bye\n"
                break

    def gegnerwahl(self):
        print "Mögliche Gegner sind: [G]obblin, [O]rk, [D]rache"
        gwahl = raw_input("Welchen wollen Sie?\n")
        if gwahl == "Gobblin"   or gwahl == "G"     or gwahl == "g":
            gegn = Gegner("Gobblin", 1, 10, "Angriff", "Angriff", "Angriff")
        elif gwahl == "Ork"     or gwahl == "O"     or gwahl == "o":
            gegn = Gegner("Ork", 8, 18, "Angriff", "Angriff", "Angriff")
        elif gwahl == "Drache" or gwahl =="D" or gwahl == "d":
            gegn = Gegner("Drache", 30, 42, "Feuerodem", "Feuerodem", "Angriff")
        else:
            print "Dann ein Überraschungsgegner!"
            gegn = Gegner("Rätselhafter Feind(TM)", 1, self.hero.ktp + 1, "Angriff", "Angriff", "Angriff")
        while True:
            print "Ihr amtierender Gegner ist ein", gegn.gname, "!"
            wahl = raw_input("Ok? [J]a / [N]ein\n")
            if wahl == "J" or wahl == "j":
                Kampf(self.hero, gegn).kampfmenue()
                break
            elif wahl == "N" or wahl == "n":
                break

    def status(self):
        print self.hero
        print "Level:\t\t\t", self.hero.level
        print "Stärke:\t\t\t", self.hero.st, "\nIntelligenz:\t\t", self.hero.it
        print "Geschicklichkeit:\t", self.hero.ge,  "\nRüstungsklasse:\t\t", self.hero.rk
        print "\nSie haben noch", self.hero.ktp, "von", self.hero.tp, "Trefferpunkten."
        print "Und noch", self.hero.kit, "von", self.hero.it, "Manapunkten.\n"

        if self.hero.waffe is None:
            wtext = "Keine Waffe!"
        else:
            wtext = self.hero.waffe

        if self.hero.panzer == None:
            ptext = "Keine Rüstung!"
        else:
            ptext = self.hero.panzer

        if self.hero.accessoire == None:
            atext = "Kein Accessoire!"
        else:
            atext = self.hero.accessoire

        print "Waffe:\t\t\t", wtext, "\nRüstung:\t\t", ptext, "\nAccessoire:\t\t", atext, "\n"
        print "In ihrer Geldbörse befinden sich", self.hero.geld, "Münzen."
        print "Sie haben", self.hero.ep, "EP und benötigen weitere", self.hero.dep - self.hero.ep, "um aufzusteigen.\n"
        print "Stärke verbessert pysische Angriffe und vergrösserte die Tragekapazität, \
        \nGeschick lässt Sie besser treffen und ausweichen und erhöht Ihre Erstschlagchance, \
        \ndie Rüstungsklasse schützt vor Schaden und \nIntelligenz erhöht die Effektivität Ihrer Magie."

    def speichern(self):
        spielstand = {
        "attribute":{
                    "tp":self.hero.tp,
                    "ktp":self.hero.ktp,
                    "st":self.hero.st,
                    "ge":self.hero.ge,
                    "rk":self.hero.rk,
                    "it":self.hero.it,
                    "kit":self.hero.kit,
                    "name":self.hero.name,
                    "ep":self.hero.ep,
                    "dep":self.hero.dep,
                    "level":self.hero.level
                    },
        "angriffe":{
                    "zauber":self.hero.arsenal.rucksack,
                    "angriff1": self.hero.angriff1,
                    "angriff2": self.hero.angriff2,
                    "angriff3": self.hero.angriff3
                    },
        "ausruestung":{
                    "geld": self.hero.geld,
                    "inventar":self.hero.ruck.rucksack,
                    "waffe": self.hero.waffe,
                    "panzer": self.hero.panzer,
                    "accessoire": self.hero.accessoire
                    }
                }
        speicherstandname = self.hero.name + ".pkmn"
        speicherstand = open(speicherstandname, "w") #w für write
        pickle.dump(spielstand, speicherstand)
        speicherstand.close()
        print "Spielstand gespeichert"

# die START Sequenz
if __name__ == "__main__": 
    Elysium().start()