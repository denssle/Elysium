import pygame

pygame.init()
grosse = breite, hoehe = 1024, 720
screen = pygame.display.set_mode(grosse)
pygame.display.set_caption("DER WOW KILLER")
gedrueckt = False
feldgroesse = 120
abstand_rand = 110
felderzahl = 4

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

class Grafik:
    def __init__(self):
        pass
    
    def felder_zeichnen(self):
        for x in range(0, 4):            
            for y in range(0, 4):
                position = [abstand_rand+(x*feldgroesse), abstand_rand+(y*feldgroesse), feldgroesse-1, feldgroesse-1]# x, y
                if Tasche(zeilen_1, spalten_1).test_feld_belegt(x, y) == False:
                    pygame.draw.rect(screen, WHITE, position, 0) #position, groesse
                else:
                    pygame.draw.rect(screen, RED, position, 0) #position, groesse
                    
    def text_schreiben(self, text):
        font = pygame.font.Font(None, 30)
        p1_surf = font.render(text, 1, WHITE)
        screen.blit(p1_surf, [100, 40])
        
#controller
def anklicken(pos):
    x = pos[0]
    y = pos[1]
    umrechner = umrechnen(x, y)
    return umrechner

def umrechnen(x, y):
    mit_abstand = abstand_rand + feldgroesse
    if x >= abstand_rand and x < abstand_rand + (felderzahl*feldgroesse):#drinnen
        if x <= mit_abstand:
            spalte_x = 0
        elif x > mit_abstand and x <= mit_abstand + feldgroesse:
            spalte_x = 1
        elif x > mit_abstand + feldgroesse and x <= mit_abstand + (feldgroesse * 2):
            spalte_x = 2
        elif x > mit_abstand + (feldgroesse * 2) and x <= mit_abstand + (feldgroesse * 3):
            spalte_x = 3
            
    if y >= abstand_rand and y < abstand_rand + (felderzahl*feldgroesse):#drinnen
        if y <= mit_abstand:
            zeile_y = 0
        elif y > mit_abstand and y <= mit_abstand + feldgroesse:
            zeile_y = 1
        elif y > mit_abstand + feldgroesse and y <= mit_abstand + (feldgroesse * 2):
            zeile_y = 2
        elif y > mit_abstand + (feldgroesse * 2) and y <= mit_abstand + (feldgroesse * 3):
            zeile_y = 3
        try:
            umrechner = [spalte_x, zeile_y]
            return umrechner
        except:
            pass

while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gedrueckt = True
        elif event.type == pygame.MOUSEBUTTONUP:
            gedrueckt = False
        elif event.type == pygame.MOUSEMOTION:
            if gedrueckt == True:
                umrechner = anklicken(pygame.mouse.get_pos())
                
    try:
        zeile_x, spalte_y = umrechner[0], umrechner[1]
        fuu = Tasche(zeilen_1, spalten_1)
        fuu.test_feld_belegt(zeile_x, spalte_y)
        fuu.feld_belegen(zeile_x, spalte_y)
    except:
        pass
        
    Grafik().felder_zeichnen()
    Grafik().text_schreiben("Die Tasche!")
    
    pygame.display.update()
    time.sleep(0.1)
