# -*- coding: utf-8 -*-

class Ausruestung:
    def __init__(self, wahl):
        self.wahl = wahl
        alleausruestung = [
                            #Zielattibut: (1 = tp, 2 = mana, 3 = st, 4 = ge, 5 = rk)
                            #typ: (1 = Waffe, 2 = rüstung, 3 = accessoire)
                            #Waffe; Name, Schaden, zielattribut, typ = 1, preis
                            "Dolch",            2,  3,   1,  25,
                            "Morgenstern",      3,  3,   1,  50,
                            "Axt",              4,  3,   1,  75,
                            "Kurzschwert",      5,  3,   1,  100,
                            "Kampfstab",        6,  3,   1,  125,
                            "Rapier",           7,  3,   1,  150,
                            "Streitkolben",     8,  3,   1,  175,
                            "Pike",             9,  3,   1,  200,
                            "Langschwert",      10, 3,   1,  225,
                            "Streithammer",     11, 3,   1,  250,
                            "Streitaxt",        12, 3,   1,  275,
                            "Bastardschwert",   13, 3,   1,  300,
                            "Krummschwert",     14, 3,   1,  325,
                            #Rüstung; Name, Schutzwert, zielattribut, typ = 2, preis
                            "Waffenrock",       2,  5,  2,  25, 
                            "Lederpanzer",      3,  5,  2,  50,
                            "Fellweste",        4,  5,  2,  75,
                            "Kettenhemd",       5,  5,  2,  100,
                            "Ringpanzer",       6,  5,  2,  125,
                            "Schuppenpanzer",   7,  5,  2,  150,
                            "Schienenpanzer",   8,  5,  2,  175,
                            "Feldharnisch",     9,  5,  2,  200,
                            "Vollharnisch",     10, 5,  2,  225,
                            "Mithrilpanzer",    11, 5,  2,  250,
                            "Drachenharnisch",  12, 5,  2,  275,
                            "Adamantiumpanzer", 13, 5,  2,  300,
                            #accessoires; Name, Bonus, zielattribut, typ = 3, preis
                            "TPRing", 5, 1, 3, 100,
                            "Manaring", 5, 2, 3, 100
                            
                            ]
        #die 0 im namen dient zur abgrenzung zu den methodennamen
        self.position     =   alleausruestung.index(self.wahl)
        self.bonus0       =   alleausruestung[self.position + 1]
        self.ziel0        =   alleausruestung[self.position + 2]
        self.typ0         =   alleausruestung[self.position + 3]
        self.preis0       =   alleausruestung[self.position + 4]
        
    def name(self):
        return self.wahl
    
    def bonus(self):
        return self.bonus0
    
    def ziel(self):
        return self.ziel0
    
    def typ(self):
        return self.typ0
    
    def preis(self):
        return self.preis0