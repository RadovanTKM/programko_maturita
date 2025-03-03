from random import randint
import pygame
pygame.init()

# oblíbené barvy
black = (0,0,0)
white = (255, 255, 255)
red = (239, 20, 26)
green = (15, 207, 20)

# obrazovka
SIRKA, VYSKA = 300, 300
screen = pygame.display.set_mode([SIRKA, VYSKA])
pygame.display.set_caption('The Best Pong On Earth')


timer = pygame.time.Clock()
framerate = 60

font = pygame.font.Font('obrazek1.ttf', 20)  # druhý člen je velikost fontu

# vlastnosti
hráč_y = 130
hráč2_y = 130
počítač_y = 130
míč_x = 145
míč_y = 145
směr_hráče = 0
směr_hráče2 = 0
rychlost_hráče = 4
směr_x_míčku = 1  # míček poletí pravé strany
směr_y_míčku = 1  # míček poletí dolů
rychlost_x_míčku = 1  # rychlost míčku po ose x  
rychlost_y_míčku = 1  # rychlost míčku po ose y
skóre = 0  # skore je 0 když hra začíná
barva_míčku = white  # barva míčku ze začátku hry je bílá
rychlost_počítače = 4
konec_hry = False
konec_W = False

    
# Přihlašovací obrazovka
def přihlašovací_obrazovka():
    jméno = ''
    aktivní_input = True
    while aktivní_input:
        screen.fill(black)
        text_jméno = font.render('Username: ' + jméno, True, white)
        screen.blit(text_jméno, (50, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Když stiskne Enter, přihlásí se
                    return jméno
                elif event.key == pygame.K_BACKSPACE:  # Pokud stiskne Backspace, odstraní poslední znak
                    jméno = jméno[:-1]
                else:
                    jméno += event.unicode  # Přidá znak do jména

        pygame.display.flip()
        timer.tick(framerate)
        

# volání přihlašovací obrazovky
jméno_hráče = přihlašovací_obrazovka()

rezim_hry = None

def zobrazit_menu():
    global rezim_hry
    while rezim_hry is None:
        screen.fill(black)
        text1 = font.render('Hráč vs. Počítač', True, black)
        text2 = font.render(' Hráč vs. Hráč', True, black)
        tlacitko1 = pygame.draw.rect(screen, white, [50, 100, 200, 40])
        tlacitko2 = pygame.draw.rect(screen, white, [50, 160, 200, 40])
        screen.blit(text1, (70, 110))
        screen.blit(text2, (80, 170))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tlacitko1.collidepoint(event.pos):
                    rezim_hry = 'pc'
                elif tlacitko2.collidepoint(event.pos):
                    rezim_hry = 'hrac'
        
        pygame.display.flip()
        timer.tick(framerate)

zobrazit_menu()

# definování počítače
def better_ai(míč_y, počítač_y):
    rychlost_počítače = 3
    if počítač_y + 15 > míč_y + 5:
        počítač_y -= rychlost_počítače
    elif počítač_y + 15 < míč_y + 5:
        počítač_y += rychlost_počítače
    return počítač_y


# kolize míčku
def smart_ai(směr_x_míčku, směr_y_míčku, míč_x, míč_y, rychlost_x_míčku, rychlost_y_míčku):
    if směr_x_míčku == 1 and míč_x < 290:
        míč_x += rychlost_x_míčku
    elif směr_x_míčku == 1 and míč_x >= 290:
        směr_x_míčku *= -1
    if směr_x_míčku == -1 and míč_x > 0:
        míč_x -= rychlost_x_míčku
    elif směr_x_míčku == -1 and míč_x <= 0:
        směr_x_míčku *= -1
    if směr_y_míčku == 1 and míč_y < 290:
        míč_y += rychlost_y_míčku
    elif směr_y_míčku == 1 and míč_y >= 290:
        směr_y_míčku *= -1
    if směr_y_míčku == -1 and míč_y > 0:
        míč_y -= rychlost_y_míčku
    elif směr_y_míčku == -1 and míč_y <= 0:
        směr_y_míčku *= -1
    return směr_x_míčku, směr_y_míčku, míč_x, míč_y


def kontrola_kolize(míček, hráč, počítač, směr_x_míčku, skóre):
    global barva_míčku  # odkazuje na existující proměnlivost míčku
    if míček.colliderect(hráč) and směr_x_míčku == -1:
        směr_x_míčku = 1  # pokud proběhne kolize míčku s hráčem tak se odrazí směrem na pravou stranu 
        skóre += 1
        barva_míčku = (randint(0,255),randint(0,255),randint(0,255))  # pokaždé co se zvýší skóre tak se změní barva míčku
    elif míček.colliderect(počítač) and směr_x_míčku == 1:
        směr_x_míčku = -1  # pokud proběhne kolize míčku s počítačem tak se odrazí směrem na levou stranu 
        skóre += 1
        barva_míčku = (randint(0,255),randint(0,255),randint(0,255))
    return směr_x_míčku, skóre, barva_míčku


def kontrola_konce_hry(míč_x, konec_hry):
    if míč_x <= 0  and konec_hry == False:
        konec_hry = True
    return konec_hry

def kontrola_výhry(míč_x, konec_W):
    if míč_x >= 290 and konec_W == False:
        konec_W = True
    return konec_W


# vykreslení (zobrazení předmětů)
running = True
while running: # loop který pořad běžý dokud je running True
    timer.tick(framerate)
    screen.fill(black)
    konec_hry = kontrola_konce_hry(míč_x, konec_hry)  # kontroluje kolizi míčku do strany
    konec_W = kontrola_výhry(míč_x, konec_W)
    hráč = pygame.draw.rect(screen, white, [5, hráč_y, 10, 40])
    if rezim_hry == 'pc':
        počítač = pygame.draw.rect(screen, white, [285, počítač_y, 10, 40])
    else:
        hráč2 = pygame.draw.rect(screen, white, [285, hráč2_y, 10, 40])
    míček = pygame.draw.rect(screen, barva_míčku, [míč_x, míč_y, 13,13])
    text_skóre = font.render('Skóre: '+ str(skóre), True, white, black) 
    screen.blit(text_skóre, (110, 5)) 
    text_jméno = font.render(f'Hráč: {jméno_hráče}', True, white)
    screen.blit(text_jméno, (110, 30))
    
       # pohyb hráčů/počítače
    hráč_y += směr_hráče * rychlost_hráče
    hráč_y = max(0, min(VYSKA - 40, hráč_y))
    if rezim_hry == 'pc':
        počítač_y = better_ai(míč_y, počítač_y)
    else:
        hráč2_y += směr_hráče2 * rychlost_hráče
        hráč2_y = max(0, min(VYSKA - 40, hráč2_y))

    směr_x_míčku, směr_y_míčku, míč_x ,míč_y = smart_ai(směr_x_míčku, směr_y_míčku, míč_x, míč_y, rychlost_x_míčku, rychlost_y_míčku)

    # key bind pro hráče
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                směr_hráče = -1
            if event.key == pygame.K_s:
                směr_hráče = 1
            if rezim_hry == 'hrac':
                if event.key == pygame.K_UP:
                    směr_hráče2 = -1
                if event.key == pygame.K_DOWN:
                    směr_hráče2 = 1
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_w, pygame.K_s]:
                směr_hráče = 0
            if rezim_hry == 'hrac' and event.key in [pygame.K_UP, pygame.K_DOWN]:
                směr_hráče2 = 0

    # konec hry    
    if not konec_hry and not konec_W:  # touto podmínkou říkáme, že míček se aktualizuje pokud konec hry je false
        počítač_y = better_ai(míč_y, počítač_y)
        směr_x_míčku, směr_y_míčku, míč_x ,míč_y = smart_ai(směr_x_míčku, směr_y_míčku, míč_x, míč_y, rychlost_x_míčku, rychlost_y_míčku) # ai sleduje míček
    směr_x_míčku, skóre, barva_míčku = kontrola_kolize(míček, hráč,počítač ,směr_x_míčku, skóre)

    if konec_hry:
            # resetování hry     
        resetovací_čudlík = pygame.draw.rect(screen, black, [0, 0, 300, 300])  # kontroluje jestli hráč klikne pro novou hru
        reset_text = font.render('Klikni Pro Novou Hru', True, white, black)  # nejdříve se musí vyrenderovat a poté se musí vyobrazit na obrazovku pomocí blit funkce
        screen.blit(reset_text, (45, 150))
        
        konec_hry_text = font.render('! PROHRÁL SI !', True, red, black)  # nejdříve se musí vyrenderovat a poté se musí vyobrazit na obrazovku pomocí blit funkce
        screen.blit(konec_hry_text, (85, 120)) 

    # výhra     
    if konec_W:
            # resetování hry     
        resetovací_čudlík = pygame.draw.rect(screen, black, [0, 0, 300, 300])  # kontroluje jestli hráč klikne pro novou hru
        reset_text = font.render('Klikni Pro Novou Hru', True, white, black)  # nejdříve se musí vyrenderovat a poté se musí vyobrazit na obrazovku pomocí blit funkce
        screen.blit(reset_text, (45, 150))
        
        konec_hry_text = font.render('! VYHRÁL SI !', True, green, black)  # nejdříve se musí vyrenderovat a poté se musí vyobrazit na obrazovku pomocí blit funkce
        screen.blit(konec_hry_text, (90, 120)) 


    # key bind pro hráče
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_w or event.key == pygame.K_UP:
               směr_hráče = -1
           if event.key == pygame.K_s or event.key == pygame.K_DOWN:
               směr_hráče = 1
       if event.type == pygame.KEYUP:
           if event.key == pygame.K_w or event.key == pygame.K_UP:
               směr_hráče = 0
           if event.key == pygame.K_s or event.key == pygame.K_DOWN:
               směr_hráče = 0

       if event.type == pygame.MOUSEBUTTONDOWN and konec_hry or event.type == pygame.MOUSEBUTTONDOWN and konec_W : # funkce pro tlačítko stisknutí pravý tlačítko myši
               konec_hry = False
               konec_W = False
               hráč_y = 130
               počítač_y = 130
               míč_x = 145
               míč_y = 145
               směr_hráče = 0  # vlastnosti se resetují na 0 po kliknutí na tlačítko konec hry
               rychlost_hráče = 4
               směr_x_míčku = 1 
               směr_y_míčku = 1 
               rychlost_x_míčku = 1
               rychlost_y_míčku = 1
               rychlost_počítače = 1
               skóre = 0

    hráč_y += rychlost_hráče * směr_hráče
    if hráč_y < 0:
        hráč_y = 0

    elif hráč_y > 300 - 40:  # 300 je výška obrazovky, 40 je výška pálky , kolize hráče 
        hráč_y = 300 - 40
        
    elif počítač_y > 300 - 40: # kolize počítače
        počítač_y = 300 - 40

    rychlost_x_míčku = 2 + (skóre//7)  # rychlost míčku se pokaždé zvyšuje o 2 s odrazem od pálky když dosáhneme 7 bodů po ose X
    rychlost_y_míčku = 1 + (skóre//10)  # rychlost míčku se pokaždé zvýší o 1 s odrazem od pálky pod dosáhnutí 10 bodů po ose Y
    rychlost_počítače = 1 + (skóre//17)

    pygame.display.flip()

pygame.quit()