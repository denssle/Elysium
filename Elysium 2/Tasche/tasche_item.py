# -*- coding: utf-8 -*-

class Item:
    def __init__(self, name, z_platz, s_platz, stapel):
        self.name = name
        self.z_platz = z_platz#zeilen, die das item einnimmt
        self.s_platz = s_platz#spalten, die das Item einnimmt
        self.stapel = stapel
        
        if type(self.z_platz) != int or type(self.s_platz) != int or type(self.name) != str or self.name == "":
            return False
        else:
            pass
