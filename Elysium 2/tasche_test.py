# -*- coding: utf-8 -*-

import unittest
from tasche import *
from tasche_item import *

class Taschentest_init(unittest.TestCase):
    def test_einfache_tasche(self):
        #Arrange
        test = Tasche(7, 7)
        #Act
        for i in range(0, 7):
            for j in range(0, 7):
                #Assert
                self.assertEqual(test.test_feld_belegt(i, j), False) 
                
    def test_hat_tasche_die_angegebene_groesse_quadadratisch(self):
        #Arrange
        test = Tasche(3, 7)
        #Act
        for i in range(0, 3):
            for j in range(0, 7):
                #Assert
                self.assertEqual(test.test_feld_belegt(i, j), False) 
                
    def test_hat_tasche_die_angegebene_groesse_rechteckig(self):
        #Arrange
        test = Tasche(7, 3)
        #Act
        for i in range(0, 7):
            for j in range(0, 3):
                #Assert
                self.assertEqual(test.test_feld_belegt(i, j), False) 
                
    def test_zu_grosse_tasche(self):
        try:
            #Arrange
            #Act
            test = Tasche(50, 50)
            #Assert
            self.fail()
        except TypeError:
           pass
          
    def test_zu_kleine_tasche(self):
        try:
            #Arrange
            #Act
            test = Tasche(0, 0)
            #Assert
            self.fail()
        except TypeError:
           pass
            
    def test_negative_tasche(self):
        try:
            #Arrange
            #Act
            test = Tasche(-5, -5)
            #Assert
            self.fail()
        except TypeError:
           pass
        
    def test_zu_viele_spalten(self):
        try:
            #Arrange
            #Act
            test = Tasche(5, 50)
            #Assert
            self.fail()
        except TypeError:
           pass
        
    def test_zu_viele_zeilen(self):
        try:
            #Arrange
            #Act
            test = Tasche(50, 5)
            #Assert
            self.fail()
        except TypeError:
           pass
        
    def test_zu_wenig_zeilen(self):
        try:
            #Arrange
            #Act
            test = test = Tasche(0, 5)
            #Assert
            self.fail()
        except TypeError:
           pass
        
    def test_zu_wenig_spalten(self):
        try:
            #Arrange
            #Act
            test = test = Tasche(5, -5)
            #Assert
            self.fail()
        except TypeError:
           pass
        
    def test_ausserhalb_der_Tasche_positiver_bereich(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        for i in range(5, 10):
            for j in range(5, 10):
                #Assert
                self.assertEqual(test.test_feld_belegt(i, j), None)
                
    def test_ausserhalb_der_Tasche_negativer_bereich(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        for i in range(-10, -1):
            for j in range(-10, -1):
                #Assert
                self.assertEqual(test.test_feld_belegt(i, j), None)
                
    def test_buchstaben_als_parameter(self):
        try:
            #Arrange
            #Act
            test = Tasche("Hans", "im_Glueck")
            #Assert
            self.fail()
        except TypeError:
           pass
        
    def test_buchstaben_als_zeile(self):
        try:
            #Arrange
            #Act
            test = Tasche("Hans", 5)
            #Assert
            self.fail()
            
        except TypeError:
           pass
        
    def test_buchstaben_als_spalte(self):
        try:
            #Arrange
            #Act
            test = Tasche(5, "Hans")
            #Assert
            self.fail()
        except TypeError:
           pass
        
    def test_leere_eingabe(self):
        try:
            #Arrange
            #Act
            test = Tasche("", "")
            #Assert
            self.fail()
            
        except TypeError:
           pass
        
    def test_leere_eingabe_als_zeile(self):
        try:
            #Arrange
            #Act
            test = Tasche("", 5)
            self.fail()
        except TypeError:
           pass
        
    def test_leere_eingabe_als_spalte(self):
        try:
            #Arrange
            #Act
            test = Tasche(5, "")
            #Assert
            self.fail()
        except TypeError:
           pass
        
class Taschentest_feld_belegen(unittest.TestCase):        
    def test_feld_wird_belegt(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        for i in range(0, 5):
            for j in range(0, 5):
                test.feld_belegen(i, j, Item("ITEM",1,1,1))
                #Assert
                self.assertEqual(test.test_feld_belegt(i, j), True)
                
    def test_einzelnes_feld_belegen(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        test.feld_belegen(2, 2, Item("ITEM",1,1,1))
        test.feld_belegen(4, 4, Item("ITEM",1,1,1))
        test.feld_belegen(1, 2, Item("ITEM",1,1,1))
        test.feld_belegen(3, 0, Item("ITEM",1,1,1))
        test.feld_belegen(0, 4, Item("ITEM",1,1,1))
        #Assert
        self.assertEqual(test.test_feld_belegt(2, 2), True)
        self.assertEqual(test.test_feld_belegt(4, 4), True)
        self.assertEqual(test.test_feld_belegt(1, 2), True)
        self.assertEqual(test.test_feld_belegt(3, 0), True)
        self.assertEqual(test.test_feld_belegt(0, 4), True)
        
    def test_feld_ausserhalb_der_Tasche_belegen(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        for i in range(5, 20):
            for j in range(5, 20):
                test.feld_belegen(i, j, Item("ITEM",1,1,1))
                #Assert
                self.assertEqual(test.test_feld_belegt(i, j), None)
                
        #Act        
        for i in range(0, 5):
            for j in range(0, 5):
                #Assert
                self.assertEqual(test.test_feld_belegt(i, j), False)
    
    def test_feld_belegen_korrupt(self):
        try:
            #Arrange
            test = Tasche(5, 5)
            #Act
            test.feld_belegen("Hans", "items", "ITEM")
            #Assert
            self.fail()
        except ValueError:
            pass
    
    def test_feld_belegen_z_korrupt(self):
        try:
            #Arrange
            test = Tasche(5, 5)
            #Act
            test.feld_belegen("Hans", 5, "ITEM")
            #Assert
            self.fail()
        except ValueError:
            pass

    def test_feld_belegen_s_korrupt(self):
        try:
            #Arrange
            test = Tasche(5, 5)
            #Act
            test.feld_belegen(5, "Georg", "ITEM")
            #Assert
            self.fail()
        except ValueError:
            pass
            
class Taschentest_hineinlegen(unittest.TestCase):
    def test_tasche_item_hinzu_(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        test.hineinlegen(Item("HANS",1,1,1))
        zu_testen = test.tasche[0][0].belegt_item
        #Assert
        self.assertEqual(zu_testen, "HANS")
        
        
    def test_tasche_item_hinzu_das_zu_gross_ist(self):
         #Arrange
        test = Tasche(5, 5)
        #Act
        test.hineinlegen(Item("HANS",10,10,1))
        #Assert
        for i in range(0, 5):
            for j in range(0, 5):
                self.failIfEqual(test.tasche[i][j].belegt_item, "HANS")
                
                
    def test_tasche_item_hinzu_das_zu_klein_ist(self):
         #Arrange
        test = Tasche(5, 5)
        #Act
        test.hineinlegen(Item("HANS",0,0,1))
        #Assert
        for i in range(0, 5):
            for j in range(0, 5):
                self.failIfEqual(test.tasche[i][j].belegt_item, "HANS")
                
    def test_item_hinzu_mit_negativer_groesse(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        test.hineinlegen(Item("ITEM",-3,-3,1))
        #Assert
        for i in range(0, 5):
            for j in range(0, 5):
                self.failIfEqual(test.tasche[i][j].belegt_item, "ITEM")
                
    def test_item_hinzu_bei_voller_tasche(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        for x in range(0, 25):
            name = "Hans" + str(x)
            test.hineinlegen(Item(name,1,1,1))
        test.hineinlegen(Item("Christoff",1,1,1))
        for i in range(2, 5):
            for j in range(0, 5):
                #Assert
                self.failIfEqual(test.tasche[i][j], "Christoff") 
                
                
    def test_item_hinzu_bei_halbvoller_tasche(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        for x in range(0, 10):
            name = "Hans" + str(x)
            test.hineinlegen(Item(name,1,1,1))
        test.hineinlegen(Item("Christoff",1,1,1))
        #Assert
        self.assertEqual(test.tasche[2][0].belegt_item, "Christoff")
        
    def test_item_hinzu_bei_halbvoller_tasche2(self):
        #Arrange
        test = Tasche(6, 6)
        #Act
        for i in range(0, 6, 2):
            for j in range(0, 6):
                test.feld_belegen(i, j, Item("ITEM",1,1,1))
        test.hineinlegen(Item("Testitem",1,1,1))
        test.hineinlegen(Item("Testitem2",1,1,1))
        #Assert
        self.assertEqual(test.tasche[0][1].belegt_item, "Testitem")
        self.assertEqual(test.tasche[0][3].belegt_item, "Testitem2")
        
    def test_item_hinzu_und_wieder_weg(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        test.hineinlegen(Item("Ein_Item",1,1,1))
        test.feld_belegen(2, 2, Item("Platzhalter",1,1,1))
        zu_testen = test.tasche[3][3].belegt_item
        #Assert
        self.assertEqual(zu_testen, "Leer")
        self.assertEqual(test.test_feld_belegt(3, 3), False)
        
        
    def test_item_korrupt_groesse(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        try:
            test.hineinlegen(Item("ITEM","Wurst","Clara",1))
            #Assert
            self.fail()
        except TypeError:
            pass
            
    def test_item_korrupt_z_grosse(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        try:
            test.hineinlegen(Item("Item","Wurst",5,1))
            #Assert
            self.fail()
        except TypeError:
            pass
            
    def test_item_korrupt_groesse(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        try:
            test.hineinlegen(Item("Item", 5,"Wurst",1))
            #Assert
            self.fail()
        except TypeError:
            pass
            
    def test_item_korrupt_name(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        try:
            test.hineinlegen(Item(731, 5,5,1))
            #Assert
            self.fail()
        except TypeError:
            pass
            
    def test_item_korrupt_name_leer(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        try:
            test.hineinlegen(Item("", 1,1,1))
            #Assert
            self.fail()
        except TypeError:
            pass
    
    def test_item_stapelbar(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        for x in range(0, 10):
            test.hineinlegen(Item("ITEM",1,1,1))
            
        test.herausnehmen("ITEM")
        
        for i in range(0, 5):
            for j in range(0, 5):
                #Assert
                self.assertEqual(test.test_feld_belegt(i, j), False) 
            
class Taschentest_herausnehmen(unittest.TestCase):
    def test_item_herausnehmen(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        test.hineinlegen(Item("ITEM", 1,1,1))
        test.herausnehmen("ITEM")
        #Assert
        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(test.test_feld_belegt(i, j), False)
                
    def test_item_bei_genutzer_tasche_heraus(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        test.hineinlegen(Item("ITEM", 5,5,1))
        test.hineinlegen(Item("ITEM2", 5,5,1))
        test.hineinlegen(Item("ITEM3", 5,5,1))
        
        test.herausnehmen("ITEM")
        #Assert
        self.assertEqual(test.test_feld_belegt(0, 0), False)
        self.assertEqual(test.test_feld_belegt(1, 0), True)
        self.assertEqual(test.test_feld_belegt(2, 0), True)
        self.assertEqual(test.test_feld_belegt(3, 0), False)

    def test_item_nicht_existent(self):
        #Arrange
        test = Tasche(5, 5)
        #Act
        test.herausnehmen("ITEM")
        #Assert
        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(test.test_feld_belegt(i, j), False)
        for i in range(0, 5):
            for j in range(0, 5):
                self.failIfEqual(test.test_feld_belegt(i, j), True)
        
        
if __name__ == "__main__": 
    unittest.main()
    
    
    """
        #Arrange
        #Act
        #Assert
B Are the boundary conditions correct?
I Can you check inverse relationships?
C Can you cross check using other means?
E Can you force an error condition to happen?
P Are the performance characteristics acceptable?    
    """