# -*- coding: utf-8 -*-

class Dialog:
    def __init__(self, sprecher, angesprochener):
        self.sprecher = sprecher
        self.angesprochener = angesprochener
        self.kette = False
        
    def sprechen(self, text):#aussage ohne wahl
        print self.sprecher, " : ", text
    
    def antworten(self, text):#angesprochener spricht
        print self.angesprochener, ":", text
        
    def wahl(self, text, w1, w2, w3, w4):#aussage mit anschließender wahl
        self.sprechen(text)
        
        if w1 != None:
            print "1: ", w1[0]
        if w2 != None:
            print "2: ", w2[0]
        if w3 != None:
            print "3: ", w3[0]
        if w4 != None:
            print "4: ", w4[0]
        
        wahl = raw_input("Antwort:")
        
        if wahl == "1" and w1 != None:
            self.wahl_antwort(w1)
        elif wahl == "2" and w2 != None:
            self.wahl_antwort(w2)
        elif wahl == "3" and w3 != None:
            self.wahl_antwort(w3)
        elif wahl == "4" and w4 != None:
            self.wahl_antwort(w4)
            
    def wahl_antwort(self, wahl):
        self.antworten(wahl[0])
        self.sprechen(wahl[1])
        self.kette = wahl[2]
            
    def auswirkungen(self):
        pass
        
    def ciao(self):#gesprächsende
        pass
        
        
if __name__ == "__main__":
    NPC = "Hans"
    Held = "Franz"
    gespraech = Dialog(NPC, Held)
    
    ansprechen = "Hallo " + Held + "!"
    gespraech.sprechen(ansprechen)
    
    frage = "Wie geht es dir, " + Held + "?"
    antwort1 = ["Gut", "Das freut mich", False]
    antwort2 = ["Schlecht", "Oh!", True]
    antwort3 = None
    antwort4 = None
    gespraech.wahl(frage, antwort1, antwort2, antwort3, antwort4)
    
    print gespraech.kette
    if gespraech.kette == True:
        frage = "Was ist denn los?"
        antwort1 = ["Nichts", "REAKTION", False]
        antwort2 = ["Antwort", "REAKTION", False]
        antwort3 = ["Antwort", "REAKTION", False]
        antwort4 = ["Antwort", "REAKTION", False]
        gespraech.wahl(frage, antwort1, antwort2, antwort3, antwort4)
        
    else:
        gespraech.sprechen("Dann ist ja alles gut!")

        
    