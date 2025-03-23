"""
Pong hra v Pythonu s použitím Pygame a PyQt.
Obsahuje režimy:
1. Hráč vs. Počítač
2. Hráč vs. Hráč

Umožňuje:
- Přihlašování uživatelů
- Ukládání skóre do databáze MariaDB a souborů
- Zobrazení menu a výherních obrazovek
"""

from random import randint
import pygame
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
import re
import mariadb


# Inicializace PyQt aplikace
app = QApplication(sys.argv)

# Inicializace Pygame

pygame.init()

# barvy
black = (0,0,0)
white = (255, 255, 255)
red = (239, 20, 26)
green = (15, 207, 20)

# nastavení okna
SIRKA, VYSKA = 300, 300
screen = pygame.display.set_mode([SIRKA, VYSKA], pygame.SCALED)
pygame.display.set_caption('The Best Pong On Earth')

# Herní časovač a FPS
timer = pygame.time.Clock()
framerate = 60

# Načtení fontu
font = pygame.font.Font('obrazek1.ttf', 20)  # druhý člen je velikost fontu

# --- Herní objekty ---
# Pozice hráče a počítače na ose Y (vertikální pohyb)
hráč_y = 130
hráč2_y = 130
počítač_y = 130

# Pozice míčku
míč_x = 145
míč_y = 145

# Směry pohybu objektů (-1, 0, 1)
směr_hráče = 0
směr_hráče2 = 0
směr_x_míčku = 1  # 1 doprava, -1 doleva
směr_y_míčku = 1  # 1 dolů, -1 nahoru

# Rychlosti objektů (vyšší číslo = rychlejší pohyb)
rychlost_hráče = 4
rychlost_hráče2 = 4
rychlost_x_míčku = 1
rychlost_y_míčku = 1
rychlost_počítače = 4

# --- Herní skóre ---
skóre_hráč1 = 0
skóre_hráč2 = 0
skóre = 0  # pouze pro režim hráč vs. počítač

barva_míčku = white  # barva míčku ze začátku hry je bílá
rychlost_počítače = 4
# --- Stav hry ---
konec_hry = False
konec_W = False
jméno_hráče = ''
jméno_hráče2= ''
userID = 0
highest_score = 0


# vytvoření spojení s db (MaridaDB)
try:
    conn = mariadb.connect(
        user="student13",
        password="spsnet",
        host="dbs.spskladno.cz",
        port=3306,
        database="vyuka13"
    )
    print("Connected to MariaDB!")
    cursor = conn.cursor()
    
    # Vytvoření tabulek, pokud neexistují
    cursor.execute('CREATE TABLE IF NOT EXISTS `1AUsers` (user_id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(255))')
    cursor.execute('CREATE TABLE IF NOT EXISTS `1AScores` (id INT PRIMARY KEY AUTO_INCREMENT, user_id INT, score INT, FOREIGN KEY (user_id) REFERENCES `1AUsers`(user_id) ON DELETE CASCADE ON UPDATE CASCADE);')
    conn.commit()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")


# Funkce pro uložení nového skóre do souboru pro herni rezim hrac vs pocitac
def save_high_score(jméno_hráče, skóre):
    """
    Uloží skóre hráče do souboru 'high_score_solo.txt'.
    Pokud hráč už má záznam, aktualizuje skóre, pokud je nové skóre vyšší.
    Uchovává pouze 10 nejlepších skóre.
    """
    try:
        # Načtení aktuálních skóre
        with open("high_score_solo.txt", "r") as file:
            high_scores = file.readlines()

        # Zkontroluj, zda už hráč má skóre
        player_found = False
        for i, line in enumerate(high_scores):
            name, current_score = line.strip().split(": ")
            if name == jméno_hráče:
                if int(current_score) < skóre:  # Pokud je nové skóre lepší
                    high_scores[i] = f"{jméno_hráče}: {skóre}\n"  # Uprav skóre
                player_found = True
                break

        if not player_found:
            high_scores.append(f"{jméno_hráče}: {skóre}\n")  # Přidej nového hráče

        # Seřaď skóre podle hodnoty (z nejvyššího)
        high_scores.sort(key=lambda x: int(x.split(": ")[1]), reverse=True)
        
        # Udržuj pouze top 10 skóre
        high_scores = high_scores[:10]

        # Ulož výsledky
        with open("high_score_solo.txt", "w") as file:
            file.writelines(high_scores)
    except FileNotFoundError:
        # Pokud soubor neexistuje, vytvoř ho
        with open("high_score_solo.txt", "w") as file:
            file.write(f"{jméno_hráče}: {skóre}\n")
            
            
def save_high_score_pvp(jméno_hráče, skóre1, jméno_hráče2, skóre2):
    """
    Uloží skóre obou hráčů v PvP režimu do souboru 'high_score_pvp.txt'.
    Uchovává pouze 10 nejlepších skore.
    """
    try:
        with open("high_score_pvp.txt", "r", encoding="utf-8") as file:
            high_scores = file.readlines()

        # Přidání nového skóre
        high_scores.append(f"Hráč:{jméno_hráče} skóre: {skóre1} vs Hráč2:{jméno_hráče2} skóre: {skóre2}\n")

        # Seřaď skóre podle celkového skóre obou hráčů
        high_scores.sort(key=lambda x: sum(map(int, re.findall(r'\d+', x))), reverse=True)

        # Udržuj pouze top 10 výsledků
        high_scores = high_scores[:10]

        # Ulož do souboru
        with open("high_score_pvp.txt", "w", encoding="utf-8") as file:
            file.writelines(high_scores)
    
    except FileNotFoundError:
        with open("high_score_pvp.txt", "w", encoding="utf-8") as file:
            file.write(f"Hráč:{jméno_hráče} skóre: {skóre1} vs Hráč2:{jméno_hráče2} skóre: {skóre2}\n")
            
            
def update_user_id(username):
    """
    Najde ID hráče v databázi. Pokud neexistuje, vytvoří nový záznam.
    """
    cursor.execute('SELECT user_id FROM `1AUsers` WHERE username = ?', (username,))
    conn.commit()
    tempId = cursor.fetchone()
    if tempId is None:
        print(f"Inserting {username} into database...")
        cursor.execute('INSERT INTO `1AUsers` (username) VALUES (?)', (username,))
        conn.commit()
        update_user_id(username) # Rekurzivně zavolá, aby načetlo nové ID
    else:
        global userID
        userID = tempId[0]
        print(f"Logged as {username} ({userID})")
    return(userID)

def update_highest_score():
    """
    Získá nejvyšší skóre daného hráče z databáze.
    """
    print(f"Getting high skóre of user {userID}...")
    cursor.execute('SELECT MAX(score) FROM `1AScores` WHERE user_id = ?;', (userID,))
    conn.commit()
    skóre = cursor.fetchone()
    if skóre is None:
        print("Nebylo nalezeno žádné skóre pro uživatele #", userID)
        highest_score = 0
    else:
        highest_score = skóre[0]
        print(f"High skóre: {highest_score}")
        
# Uloží skóre
already_saved = False
def save_score(userID, skóre):
    global already_saved
    if (skóre < 1):
        return
    if already_saved:
        return
    already_saved = True
    print(f"Inserting skóre {skóre} for user {userID} into database...")
    cursor.execute('INSERT INTO `1AScores` (user_id, score) VALUES (?, ?)', (userID,skóre)) # Vloží skóre hráče
    conn.commit()

            
# přihlašení hráče
def přihlašovací_obrazovka(nadpis):
    """
    Funkce zobrazující přihlašovací obrazovku, kde uživatel může zadat své jméno a heslo.
    Heslo se při zadávání zobrazuje jako hvězdičky.
    Přepínání mezi poli se provádí klávesou TAB.
    Potvrzení přihlášení probíhá stiskem ENTER.
    Zobrazuje blikající kurzor v aktivním poli.
    
    :return: Vrací pouze zadané uživatelské jméno.
    """
    jméno = ''  # Uchovává zadané uživatelské jméno
    heslo = ''  # Uchovává zadané heslo
    aktivní_input = 'jméno'  # Určuje, do kterého pole se aktuálně zapisuje
    
    clock = pygame.time.Clock()  # Hodiny pro řízení obnovovací frekvence
    
    while True:
        screen.fill(black)  # Vyčištění obrazovky černou barvou
        
        # ** Přidání nápisu (pro Hráče 1 nebo Hráče 2) **
        text_nadpis = font.render(nadpis, True, white)
        screen.blit(text_nadpis, (SIRKA // 2 - text_nadpis.get_width() // 2, 20))  # Umístění do středu
        
        # Získání aktuálního času pro blikání kurzoru
        čas = pygame.time.get_ticks()
        kurzor = '|' if (čas // 500) % 2 == 0 else ''  # Kurzoru bliká každých 500 ms
        
        # Vykreslení textu pro uživatelské jméno
        text_jméno = font.render('Username: ' + jméno + (kurzor if aktivní_input == 'jméno' else ''), True, white)
        screen.blit(text_jméno, (50, 100))
        
        # Vykreslení textu pro heslo (zobrazené jako hvězdičky)
        text_heslo = font.render('Password: ' + '*' * len(heslo) + (kurzor if aktivní_input == 'heslo' else ''), True, white)
        screen.blit(text_heslo, (50, 150))
        
        pygame.display.flip()  # Aktualizace obrazovky, aby se změny projevily míč_x +=
        
        for event in pygame.event.get():  # Smyčka pro zpracování událostí
            if event.type == pygame.QUIT:  # Pokud uživatel zavře okno
                pygame.quit()  # Ukončení Pygame
                quit()  # Ukončení programu
            if event.type == pygame.KEYDOWN:  # Pokud je stisknuta klávesa
                if event.key == pygame.K_RETURN:  # Stisk ENTER -> přihlášení
                    if jméno.strip() == "":  # Kontrola, zda hráč zadal jméno
                        msg = QMessageBox()
                        msg.setWindowTitle("Chyba")
                        msg.setText("Musíte zadat jméno!")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec()
                    elif heslo.strip() == "":  # Kontrola, zda hráč zadal heslo
                        msg = QMessageBox()
                        msg.setWindowTitle("Chyba")
                        msg.setText("Musíte zadat heslo!")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec()
                    else:
                        return jméno, heslo  # Vrací tuple (jméno, heslo)
                elif event.key == pygame.K_TAB:  # Přepínání mezi jménem a heslem klávesou TAB
                    aktivní_input = 'heslo' if aktivní_input == 'jméno' else 'jméno'  # Přepne aktivní vstup
                elif event.key == pygame.K_BACKSPACE:  # Mazání posledního znaku klávesou BACKSPACE
                    if aktivní_input == 'jméno':  # Pokud je aktivní vstup jméno
                        jméno = jméno[:-1]  # Odstraní poslední znak ze jména
                    else:  # Pokud je aktivní vstup heslo
                        heslo = heslo[:-1]  # Odstraní poslední znak z hesla
                else:  # Pokud je stisknuta jiná klávesa
                    if aktivní_input == 'jméno':  # Pokud je aktivní vstup jméno
                        jméno += event.unicode  # Přidání znaku do jména
                    else:  # Pokud je aktivní vstup heslo
                        heslo += event.unicode  # Přidání znaku do hesla

    
        timer.tick(framerate)
        pygame.display.flip()
        

#  nastaví`rezim_hry` na None, aby byla dostupná
rezim_hry = None  

# spustí přihlašovací obrazovku hráče 1
jméno_hráče, heslo_hráče = přihlašovací_obrazovka("Přihlášení Hráče1:")

def zobrazit_menu():
    global rezim_hry
    
    running = True
    
    
    # Vytvoření gradientního pozadí
    gradient = pygame.Surface((SIRKA, VYSKA))
    for y in range(VYSKA):
        color = (y // 2, y // 2, y // 2)  # Stupňující se šedá barva
        pygame.draw.line(gradient, color, (0, y), (SIRKA, y))

    while running:
        screen.blit(gradient, (0, 0))  # Vykreslení gradientního pozadí
        
        # Přidání loga hry
        title_text = font.render('The Best Pong', True, white)
        screen.blit(title_text, (SIRKA // 2 - 70, 30))
        
        # Definice tlačítek
        tlacitko1 = pygame.Rect(50, 100, 200, 40)
        tlacitko2 = pygame.Rect(50, 160, 200, 40)

        # Animace najetí myší – změna barvy tlačítka
        color1 = green if tlacitko1.collidepoint(pygame.mouse.get_pos()) else white
        color2 = red if tlacitko2.collidepoint(pygame.mouse.get_pos()) else white
        
        pygame.draw.rect(screen, color1, tlacitko1, border_radius=10)
        pygame.draw.rect(screen, color2, tlacitko2, border_radius=10)
        
        # Text na tlačítkách
        text1 = font.render('Hráč vs. Počítač', True, black)
        text2 = font.render('Hráč vs. Hráč', True, black)
        screen.blit(text1, (70, 110))
        screen.blit(text2, (80, 170))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tlacitko1.collidepoint(event.pos):
                    rezim_hry = 'pc'
                    running = False
                elif tlacitko2.collidepoint(event.pos):
                    rezim_hry = 'hrac'
                    running = False
        
        timer.tick(framerate)
        pygame.display.flip()

zobrazit_menu()
#dodatrčné přihlašeni hrace 2 pro rezim hry hrac vs hrac


if rezim_hry == 'hrac':
    jméno_hráče2, heslo_hráče2 = přihlašovací_obrazovka("Přihlášení Hráče2:")

print(f"Hráč 1: {jméno_hráče} (heslo: {heslo_hráče})")
if rezim_hry == 'hrac':
    print(f"Hráč 2: {jméno_hráče2} (heslo: {heslo_hráče2})")

# PyQt funkce pro zobrazení okna Game Over pro hrac vs pocitac
def show_game_over_popup(jméno_hráče, skóre, rezim_hry):
  if rezim_hry == "pc":
    msg = QMessageBox()
    msg.setWindowTitle("GAME OVER")
    msg.setText(f"Hráč :{jméno_hráče}, tvoje skóre: {skóre}\nChcete si zahrát znovu?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    result = msg.exec()
    return result == QMessageBox.Yes
  return False

# Funkce pro zobrazení Game Over okna pro hrac vs hrac
def show_game_over(skóre1, skóre2):
    msg = QMessageBox()
    msg.setWindowTitle("GAME OVER")
    msg.setText(f"{jméno_hráče}: {skóre1} bodů\n{jméno_hráče2}: {skóre2} bodů\nChcete hrát znovu?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    
    result = msg.exec()
    return result == QMessageBox.Yes  # Vrací True pokud klikneme "Yes"
        

# Funkce pro reset hry
def reset_game():
    global míč_x, míč_y, směr_x_míčku, směr_y_míčku, skóre_hráč1, skóre_hráč2
    míč_x, míč_y = 145, 145
    směr_x_míčku, směr_y_míčku = 1, 1
    skóre_hráč1 = skóre_hráč2 = 0
    

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
    """
    Funkce řídící pohyb míčku, odraz od stěn a změnu směru.

    Parametry:
        směr_x_míčku (int): Směr pohybu míčku horizontálně (1 = vpravo, -1 = vlevo)
        směr_y_míčku (int): Směr pohybu míčku vertikálně (1 = dolů, -1 = nahoru)
        míč_x (int): Aktuální X pozice míčku
        míč_y (int): Aktuální Y pozice míčku
        rychlost_x_míčku (int): Rychlost pohybu míčku horizontálně
        rychlost_y_míčku (int): Rychlost pohybu míčku vertikálně
    
    Vrací:
        aktualizované hodnoty (směr_x_míčku, směr_y_míčku, míč_x, míč_y)
    """
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
    
    # Přidání efektu "záblesku"
        pygame.draw.circle(screen, red, (míček.x + 6, míček.y + 6), 10)
        pygame.display.flip()
        pygame.time.delay(50)  # Krátká pauza pro efekt
    
    elif míček.colliderect(počítač) and směr_x_míčku == 1:
        směr_x_míčku = -1  # pokud proběhne kolize míčku s počítačem tak se odrazí směrem na levou stranu 
        barva_míčku = (randint(0,255),randint(0,255),randint(0,255))
        
        # Přidání efektu "záblesku"
        pygame.draw.circle(screen, green, (míček.x + 6, míček.y + 6), 10)
        pygame.display.flip()
        pygame.time.delay(50)
    
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
    if rezim_hry == 'pc':
        konec_hry = kontrola_konce_hry(míč_x, konec_hry)  # kontroluje kolizi míčku do strany
        konec_W = kontrola_výhry(míč_x, konec_W)
        hráč = pygame.draw.rect(screen, white, [5, hráč_y, 10, 40])
    
    if rezim_hry == 'pc':
        počítač = pygame.draw.rect(screen, white, [285, počítač_y, 10, 40])
        text_skóre = font.render(f'skóre: {skóre}', True, white)
        screen.blit(text_skóre, (110, 5))
        text_jméno = font.render(f'Hráč: {jméno_hráče}', True, white)
        screen.blit(text_jméno, (110, 30))
    else:
        hráč2 = pygame.draw.rect(screen, red, [285, hráč2_y, 10, 40])
        text_skóre1 = font.render(f'{jméno_hráče}: {skóre_hráč1}', True, white)
        text_skóre2 = font.render(f'{jméno_hráče2}: {skóre_hráč2}', True, white)
        screen.blit(text_skóre1, (50, 5))
        screen.blit(text_skóre2, (180, 5))
        
    hráč = pygame.draw.rect(screen, white, [5, hráč_y, 10, 40])
    míček = pygame.draw.rect(screen, barva_míčku, [míč_x, míč_y, 13,13])
    
   
    if rezim_hry == 'hrac':
        # *** Bodování v režimu Hráč vs. Hráč ***
        if míč_x <= SIRKA - 299:  # Míček narazil do levé strany -> bod pro hráče 2
            skóre_hráč2 += 1
            míč_x, míč_y = 145, 145  # Reset míčku
        if míč_x >= SIRKA - 16:  # Míček narazil do pravé strany -> bod pro hráče 1
            skóre_hráč1 += 1
            míč_x, míč_y = 145, 145  # Reset míčku

        # *** Kontrola výhry ***
        if skóre_hráč1 == 10 or skóre_hráč2 == 10:
            save_high_score_pvp(jméno_hráče, skóre_hráč1, jméno_hráče2, skóre_hráč2)
            # Nejprve vynutíme vykreslení aktualizovaného skóre
            screen.fill(black)
            text_skóre1 = font.render(f'{jméno_hráče}: {skóre_hráč1}', True, white)
            text_skóre2 = font.render(f'{jméno_hráče2}: {skóre_hráč2}', True, white)
            screen.blit(text_skóre1, (50, 5))
            screen.blit(text_skóre2, (180, 5))
            hráč2_y = 130
            hráč_y = 130
            pygame.display.flip()  # Vykreslíme změnu
            if not show_game_over(skóre_hráč1, skóre_hráč2):
                running = False
            else:
                reset_game()  # Restart hry
    
    
       # pohyb hráčů/počítače
    hráč_y += směr_hráče * rychlost_hráče
    hráč_y = max(0, min(VYSKA - 40, hráč_y))
    if rezim_hry == 'pc':
        počítač_y = better_ai(míč_y, počítač_y)
    else:
        hráč2_y += směr_hráče2 * rychlost_hráče2
        hráč2_y = max(0, min(VYSKA - 40, hráč2_y))


    # konec hry    
    if not konec_hry and not konec_W:  # touto podmínkou říkáme, že míček se aktualizuje pokud konec hry je false 
        směr_x_míčku, směr_y_míčku, míč_x ,míč_y = smart_ai(směr_x_míčku, směr_y_míčku, míč_x, míč_y, rychlost_x_míčku, rychlost_y_míčku) # ai sleduje míček
        if rezim_hry == 'pc':
            počítač_y = better_ai(míč_y, počítač_y)
            směr_x_míčku, skóre, barva_míčku = kontrola_kolize(míček, hráč, počítač, směr_x_míčku, skóre)
        else:
            směr_x_míčku, skóre, barva_míčku = kontrola_kolize(míček, hráč, hráč2, směr_x_míčku, skóre)

    if konec_hry:
        userid = update_user_id(jméno_hráče)
        print(userid)
        save_score(userid, skóre)
        save_high_score(jméno_hráče, skóre)      
        if not show_game_over_popup(jméno_hráče, skóre, rezim_hry):
            running = False
        else:
            # Reset skóre, pozice, atd. pro novou hru
            hráč_y = 130
            hráč2_y = 130
            počítač_y = 130
            míč_x = 145
            míč_y = 145
            směr_hráče = 0
            směr_hráče2 = 0
            rychlost_hráče = 4
            rychlost_hráče2 = 4
            směr_x_míčku = 1  # směr míčku po ose x
            směr_y_míčku = 1  # míček poletí dolů
            rychlost_x_míčku = 1  # rychlost míčku po ose x  
            rychlost_y_míčku = 1  # rychlost míčku po ose y
            skóre_hráč1 = 0
            skóre_hráč2 = 0
            skóre = 0  # skore je 0 když hra začíná
            barva_míčku = white  # barva míčku ze začátku hry je bílá
            rychlost_počítače = 4
            konec_hry = False
        

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

    hráč_y += rychlost_hráče * směr_hráče
    if hráč_y < 0:
        hráč_y = 0
    elif hráč_y > VYSKA - 40:  
        hráč_y = VYSKA - 40
        
    hráč2_y += rychlost_hráče2 * směr_hráče2
    if hráč2_y < 0:
        hráč2_y = 0
    elif hráč2_y > VYSKA - 40:
        hráč2_y = VYSKA - 40
        
    elif počítač_y > VYSKA - 40: # kolize počítače
        počítač_y = VYSKA - 40

    rychlost_x_míčku = 2 + (skóre//7)  # rychlost míčku se pokaždé zvyšuje o 2 s odrazem od pálky když dosáhneme 7 bodů po ose X
    rychlost_y_míčku = 1 + (skóre//10)  # rychlost míčku se pokaždé zvýší o 1 s odrazem od pálky pod dosáhnutí 10 bodů po ose Y
    rychlost_počítače = 1 + (skóre//17)

    pygame.display.flip()

pygame.quit()