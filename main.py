from random import randint
import pygame
pygame.init()


#obrazovka
screen = pygame.display.set_mode([300, 300])
pygame.display.set_caption('The Best Pong On Earth')

timer = pygame.time.Clock()
framerate = 60
black = (0,0,0)
white = (255, 255, 255)
konec_hry = False
font = pygame.font.Font('obrazek1.ttf', 20)  #druhý člen je velikost fontu

# vlastnosti
hráč_y = 130
počítač_y = 130
míč_x = 145
míč_y = 145
směr_hráče = 0
rychlost_hráče = 4
směr_x_míčku = 1 #míček poletí pravé strany
směr_y_míčku = 1 #míček poletí dolů
rychlost_x_míčku = 2 #rychlost míčku po ose x  
rychlost_y_míčku = 2 #rychlost míčku po ose y
skóre = 0 # skore je 0 když hra začíná
barva_míčku = white #brava míčku ze začatku hry je bíla
rychlost_počítače = 1

# definování počítače
def better_ai(míč_y, počítač_y):
    rychlost_počítače = 3
    if počítač_y + 15 > míč_y + 5:
        počítač_y -= rychlost_počítače
    elif počítač_y + 15 < míč_y + 5:
        počítač_y += rychlost_počítače
    return počítač_y


#kolize míčku
def smart_ai(směr_x_míčku, směr_y_míčku, míč_x, míč_y, rychlost_x_míčku, rychlost_y_míčku,):
    if směr_x_míčku == 1 and míč_x < 290:
        míč_x += rychlost_x_míčku
    elif směr_x_míčku == 1 and míč_x >= 290:
        směr_x_míčku *= -1
    if směr_x_míčku == -1 and míč_x > 0:
        míč_x -= rychlost_x_míčku                #pokud směr míčku je -1 a x je větší než 0 tak miček se pohne doleva
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
    global barva_míčku # odkayuje na existující proměnlivost míčku
    if míček.colliderect(hráč) and směr_x_míčku == -1:
        směr_x_míčku = 1             #pokud proběhne kolize míčku s hráčem tak se odrazí směrem na pravou stranu 
        skóre += 1
        barva_míčku = (randint(0,255),randint(0,255),randint(0,255)) #pokažde co se zvýší skóre tak se změní barva míčku
    elif míček.colliderect(počítač) and směr_x_míčku == 1:
        směr_x_míčku = -1            #pokud proběhne kolize míčku s počítačem tak se odrazí směrem na levou stranu 
        skóre += 1
        barva_míčku = (randint(0,255),randint(0,255),randint(0,255))
    return směr_x_míčku, skóre, barva_míčku

    

def kontrola_konce_hry(míč_x, konec_hry):
    if (míč_x <= 0 or míč_x >= 290) and konec_hry == False:
        konec_hry = True
    return konec_hry
    
    
#vykreslení(zobrazení předmětů)
running = True
while running:
    timer.tick(framerate)
    screen.fill(black)
    konec_hry = kontrola_konce_hry(míč_x, konec_hry)  #kontroluje kolizi míčku do stran
    hráč = pygame.draw.rect(screen, white, [5, hráč_y, 10, 40])
    počítač = pygame.draw.rect(screen, white, [285, počítač_y, 10, 40])
    míček = pygame.draw.rect(screen, barva_míčku, [míč_x, míč_y, 10,10])
    text_skóre = font.render('Skóre: '+ str(skóre), True, white, black) 
    screen.blit(text_skóre, (110, 5)) 
 
 
#konec hry    
    if not konec_hry: #touto podmínkou říkame že míček se aktualizuje pokud konec hry je false
        počítač_y = better_ai(míč_y, počítač_y)
        směr_x_míčku, směr_y_míčku,míč_x ,míč_y = smart_ai(směr_x_míčku, směr_y_míčku, míč_x, míč_y, rychlost_x_míčku, rychlost_y_míčku)
    směr_x_míčku, skóre, barva_míčku = kontrola_kolize(míček, hráč,počítač ,směr_x_míčku, skóre)
    
    if konec_hry:
        konec_hry_text = font.render('!Konec Hry!', True, white, black) # nejdřive se musí vyrenderovat a poté se musí vyobrazit na obrazovku pomocí blit funkce
        screen.blit(konec_hry_text, (100, 120)) 
#resetování hry     
        resetovací_čudlík = pygame.draw.rect(screen, black, [70, 150, 100, 20]) #kontroluje jestli hráč klik pro novou hru
        reset_text = font.render('Klikni Pro Novou Hru', True, white, black) # nejdřive se musí vyrenderovat a poté se musí vyobrazit na obrazovku pomocí blit funkce
        screen.blit(reset_text, (50, 150))
        
    
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_w:
               směr_hráče = -1
           if event.key == pygame.K_s:
               směr_hráče = 1
       if event.type == pygame.KEYUP:
           if event.key == pygame.K_w:
               směr_hráče = 0
           if event.key == pygame.K_s:
               směr_hráče = 0
       if event.type == pygame.MOUSEBUTTONDOWN and konec_hry == True:
           if resetovací_čudlík.collidepoint(event.pos):
               konec_hry = False
               hráč_y = 130
               počítač_y = 130
               míč_x = 145
               míč_y = 145
               směr_hráče = 0           # vlastnosti se resetuj na 0 po kliknutí na tlačítko konec hry
               rychlost_hráče = 4
               směr_x_míčku = 1 
               směr_y_míčku = 1 
               rychlost_x_míčku = 2  
               rychlost_y_míčku = 2 
               rychlost_počítače = 1
               skóre = 0
             
    hráč_y += rychlost_hráče * směr_hráče
    rychlost_x_míčku = 2 + (skóre//7) # rychlost míčku se pokažde zvyšuje o 2 s odrazem od pálky když dosáhneme 7 bodů po ose X
    rychlost_y_míčku = 1 + (skóre//10) # rychlost míčku se pokaždé zvýší o 1 s odrazem od pálky pod dosáhnutí 10 bodů po ose Y
    rychlost_počítače = 1 + (skóre//17)
           
    pygame.display.flip()
    
pygame.quit()