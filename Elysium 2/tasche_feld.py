# -*- coding: utf-8 -*-

class Feld:
    def __init__(self, x, y):
        self.zeile = y        
        self.spalte = x
        self.belegt = False
        self.belegt_item = "Leer"
        self.anzahl = 0
        
    def belegung_manipulieren(self, item):
        if self.belegt == False:
            self.belegt = True
            self.belegt_item = item.name
            
        else:
            self.belegt = False
            self.belegt_item = "Leer"
            self.anzahl = 0
    