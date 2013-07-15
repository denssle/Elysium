# -*- coding: utf-8 -*-

class Trank_Zauber:
    def __init__(self, wahl):
        self.wahl = wahl
        alleItems = [
                    #Zielattibut: (1 = tp, 2 = mana, 3 = st, 4 = ge, 5 = rk)
                    #heilmittel; Name, Wirkungsstärke, Zielattribut, im kampf nutzbar, preis
                    "Trank", 10, 1, True, 10,
                    "Supertrank", 20, 1, True, 17,
                    "Manatrank", 5, 2, True, 10,
                    "Heilsalbe", 15, 1, False, 10,
                    #angriffe; Name, Schaden, Manakosten, physisch(false) oder zauber(true), None bedeutet nicht verkaufbar
                    "Angriff", 1, 0, False, None,
                    "Feuerball", 4, 4, True, None,
                    "Eisstrahl", 8, 5, True, None,
                    "Kettenblitz", 16, 9, True, None,
                    #gegnerangriffe; Name, Schaden, ungenutzt, ungenutzt, None da nicht verkaufbar
                    "Feuerodem", 52, 0, True, None
                    ]
        self.position    =   alleItems.index(self.wahl)
        self.schaden     =   alleItems[self.position + 1]# oder wirkung bei tränken
        self.manakosten  =   alleItems[self.position + 2]# oder ob mana / tp heilung
        self.zauber      =   alleItems[self.position + 3]# order ob im kampf nurzbar
        self.preis       =   alleItems[self.position + 4]
        
    def name(self):
        return self.wahl
    
    def wirkung(self):
        return self.schaden
    
    def ziel(self):
        return self.manakosten
    
    def nutzbar(self):
        return self.zauber
    
    def wert(self):
        return self.preis