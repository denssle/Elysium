# -*- coding: utf-8 -*-

import pygame, sys, time
from tasche_feld import *
from tasche_item import *

class Tasche:
    def __init__(self, zeile, spalte):
        self.zeile = zeile
        self.spalte = spalte
        self.tasche = []
        
        if self.__groessen_test__(self.zeile, self.spalte) == False:
            return False
            
        for i in range(0,self.spalte):
            zeilenliste = []
            for j in range(0, self.zeile):
                zeilenliste.append(Feld(i,j))
            self.tasche.append(zeilenliste)
            
    def __groessen_test__(self, zeile, spalte):
        if zeile > 32 or spalte > 32:
            print "Zu gross!"
            return False
        elif zeile < 1 or spalte < 1:
            print "Zu klein!"
            return False
        else:
            return True
            
    def gib_gegenstand(self):#Listet die Gegenstände auf
        for i in range(0, self.spalte):
            zeile = []
            for j in range(0, self.zeile):
                zelle = self.tasche[i][j].belegt_item + " " + str(self.tasche[i][j].anzahl)
                zeile.append(zelle)
            print zeile
            
    def herausnehmen(self, gegenstand):#herausnehmen und/oder anheben eines Gegenstandes
        for i in range(0, self.spalte):
            for j in range(0, self.zeile):
                if self.tasche[i][j].belegt_item == gegenstand:
                    self.feld_belegen(i, j, "Leer")
                    print "Item entfernt!"
        
    def hineinlegen(self, gegenstand): #das hinzufügen eines Items in die Tasche
        stapelung = True
        zeilen_platz = gegenstand.z_platz
        spalten_platz = gegenstand.s_platz        
        if self.zeile < zeilen_platz or self.spalte < spalten_platz or zeilen_platz <1 or spalten_platz <1:
            return
        #wenn item schon vorhanden: 
        for i in range(0, self.spalte):
            for j in range(0, self.zeile):
                if self.tasche[i][j].belegt_item == gegenstand.name:
                    self.tasche[i][j].anzahl += gegenstand.stapel
                    stapelung = False
        if stapelung == False:
            return
        #belegbare felder suchen
        try:
            for i in range(0, self.spalte):
                for j in range(0, self.zeile):
                    if self.test_feld_belegt(j, i) == False:#leeres Feld gefunden
                        if self.grosse_items_test(gegenstand, i, j) != False:
                            for k in range(j, gegenstand.s_platz+j):
                                for l in range(i, gegenstand.z_platz+i):
                                    self.feld_belegen(k, l, gegenstand)
                            return
        except:
            print "Kein Platz!"
            
    def grosse_items_test(self, gegenstand, zeile, spalte):
        zeilenplatz = gegenstand.z_platz + zeile -1
        spaltenplatz = gegenstand.s_platz + spalte -1
        
        if zeilenplatz > self.zeile or spaltenplatz > self.spalte:
            return False
        
        for i in range(spalte, spaltenplatz):
            if self.test_feld_belegt(spalte + i, zeile) == True:
                    return False
            zeile += 1
            
    def feld_belegen(self, position_x, position_y, item):#verändert die Belegung eines Feldes
        spalte = int(position_y)
        zeile = int(position_x)
        if spalte < 0 or zeile < 0:
            spalte, zeile = None, None
        try:
            manipulator = self.tasche[spalte][zeile]
            manipulator.belegung_manipulieren(item)
            manipulator.anzahl += item.stapel
        except:
            pass
            
    def test_feld_belegt(self, position_x, position_y):# gibt an ob das Feld belegt ist
        spalte = position_y
        zeile = position_x

        if spalte < 0 or zeile < 0:
            spalte, zeile = None, None
        try:
            feedback = self.tasche[spalte][zeile]
            return feedback.belegt
        except:
            pass
            
def eingabe_zeile():
    zeile_1 = int(raw_input("Spaltenzahl:\n")) -1
    return zeile_1

def eingabe_spalte():
    spalte_1 = int(raw_input("Zeilenzahl:\n")) -1
    return spalte_1
        
if __name__ == "__main__":
    while True:
        try:
            zeile_1 = int(raw_input("Spaltenzahl:\n"))
            spalte_1 = int(raw_input("Zeilenzahl:\n"))
            if Tasche(zeile_1, spalte_1) != False:
                fuu = Tasche(zeile_1, spalte_1)
                fuu.gib_gegenstand()
                break
        except TypeError:
            pass
            
    while True:
        print "1: Feldbelegungstest \n2: Feldbelegungsbefehl \n3: Item hinzufügen \n4: Item herausnehmen \n5: Grosse Items hinzufügen"
        eingabe = raw_input("Ihre Eingabe, bitte:\n")
        if eingabe == "q":
            print "Cya!"
            break
        
        elif eingabe == "1":
            print "Test auf Feldbelegung!"
            ergebnis = fuu.test_feld_belegt(eingabe_zeile(), eingabe_spalte())
            print ergebnis
            
        elif eingabe == "2":
            print "Felder belegen!"
            fuu.feld_belegen(eingabe_zeile(), eingabe_spalte(), Item("ITEM",1,1,1))
        
        elif eingabe == "3":
            print "Item hinzufügen"
            name = raw_input("Name?\n")
            item = Item(name,1,1,1)
            fuu.hineinlegen(item)
            
        elif eingabe == "4":
            print "Gegenstand herrausnehmen!"
            name = raw_input("Name?\n")
            fuu.herausnehmen(name)
        
        elif eingabe == "5":
            print "Grosse Items!"
            wahl = raw_input("Name?\n")
            zeilen = int(raw_input("Zeilen?"))
            spalten = int(raw_input("Spalten?"))
            item = Item(wahl ,spalten,zeilen,1)
            fuu.hineinlegen(item)
            
        fuu.gib_gegenstand()
