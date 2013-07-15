// Cool Class Diagram
[Elysium|hero|neu;speichern;laden;gegnerwahl;status]-[Held]
[Elysium]-[Gegner|von; bis; angriff1; angriff2; angriff3|]
[Elysium]<>-[Händler|hero|kaufmenue; kaufen;verkaufen;preisliste]
[Held|spielstand|level_up;item_nutzen;heilung;manaheilung]<>-[Item|st; itemwahl|hinzufügen;entfernen;anzeigen;auswählen]
[Held]-[Kampf|hero;gegn|kampfmenue;ablauf;spieleraktion;gegneraktion;physischer_angriff;magischer_angriff]
[Held]-[Händler]
[Gegner]-<>[Kampf]
[Gegner]<>-[abstract;Zauber_Tränke||name;wirkung;ziel]
[Item]<>-[abstract;Zauber_Tränke]
[Item]<>-[abstract;Ausrüstung||name;bonus;ziel;typ]
[Händler]<>-[Item]


[Held]-(Inventar)
[Held]-(Talente)
[Held]-(Beschreibung)
[Gegner]-(Talente)

// Cool Class Diagram[Spiel]-[Itemverwaltung]
[Spiel]-[Monster]
[Spieler]-[Kampf]
[Spieler]-[Handel]
[Spieler]-[Inventar]
[Spieler]-[Talente&Zauber]
[Monster]-[Kampf]
[Monster]-[Talente&Zauber]
[Händler]-[Handel]
[Itemverwaltung]-[Inventar]

#
(start)-><a>->[Neuer Charakter]->[Hauptmenue],<a>->[Charakter laden]->[Hauptmenue]-><b>->[Status]-><b>, <b>->[Kampf], <b>->[Duell], <b>->[Inventar], <b>->[Speichern], <b>->[Quit]->(end),<b>->[Handel],[Inventar]-><c>->[Item benutzen],<c>-Abbrechen><b>,[Handel]-><d>->[Kaufen],<d>->[Verkaufen], <d>-Abbrechen><b>


#Kampf
(start)->[Gegnerwahl]->[Gegner]->[Rundenbeginn]->[Spieleraktionswahl]->[Gegneraktionswahl]->[Kampfablauf]-><a>, <a>->[Kampfende]-(end), <a>->[Rundenbeginn]

#Aktionswahl
[Kampfmenue]-><a>, <a>->[Angriffe], <a>->[Item], <a>->[Flucht]->(end), [Angriffe]->[Magieangriffe], [Magieangriffe]-><b>, <b>->[Magieangriff1],<b>->[Magieangriff2],<b>->[Magieangriff3], <b>-abbruch>[Magieangriffe], [Angriffe]->[Angriff]-><d>, [Magieangriff1]-><d>,[Magieangriff2]-><d>,[Magieangriff3]-><d>, [Item]-><c>->[Itemwahl]-><d>, <c>-Abbruch>[Kampfmenue], <d>->[Kampfablauf]


#Ablauf
(start)->[Geschick und Zufallswert legen Initiative fest]->[Erste Aktion]->[Kampfendecheck]-><a>->[Aktion des Kontrahenten]->[Kampfendecheck 2]-><c>,<a>->[Kampfende]->[Auswirkungen]->(end), <c>->[Kampfende], <c>->[Naechste Runde]->[Geschick und Zufallswert legen Initiative fest]

#Duell
(start)->[Duell]-><a>,<a>->[Hosten],<a>-Abbruch>(end),<a>->[Einsteigen],[Hosten]-><b>->[Hostkampfmenue], <b>-Abbruch>(end),[Einsteigen]-><c>->[Warten auf Host], <c>-Abbruch>(end),[Hostkampfmenue]->[Warten auf Client], [Warten auf Host]->[Clientwahl], [Clientwahl]->[Warten auf Ergebnis]->|d|, [Warten auf Client]->[Kampfergebnis berechnen]->|d|, |d|->[Ausgabe der Ergebnisse]->[Kampfende Check], [Kampfende Check]-><e>, <e>->[Naechste Runde],<e>->[Kampfende]
