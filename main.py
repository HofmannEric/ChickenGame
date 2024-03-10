import pygame
from Ammo.Ammunition import Ammostack
from Chicken.ChickenGenerator import chickenGen
from Crosshair.CrosshairCursor import CrossCursor
from Views.Hauptmenu import MainMenu
from Views.gameoverScreen import GameOver

pygame.init()

# Fenster erstellen + Einstellungen
win = pygame.display.set_mode((1024, 526))
winSize = win.get_size()
pygame.display.set_caption("Chickens Game")
font = pygame.font.Font('freesansbold.ttf', 18)

# Umgebungsbilder
background = pygame.image.load("Background/background_test.png")
grass = pygame.image.load("Background/grass.png")

# Objekte erstellen
menu = MainMenu()
crosshair = CrossCursor()
game_over = GameOver()
clock = pygame.time.Clock()
game_ammo = Ammostack()
game_ammo.gen_ammo()
scoreInt = 0
game_time_left = 0

state = "main_menu"

while state != "exit":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = "exit"

        if state == "main_menu":
            state_result = menu.start_clicked(event)
            if state_result:
                state = state_result

        if state == "start_game":

            # SpriteGroups um alle Chickens gleichzeitig ansprechen zu können
            all_Chickens = pygame.sprite.Group()

            # Maus im Spiel unsichtbar machen
            pygame.mouse.set_visible(False)

            # Main game loop
            run = True
            reloading = False

            # Spieleinstellungen
            reload_start_time = 0  # wird event bzw key-presses abfragen gesetzt
            reload_interval = 500  # Nachladezeit für jede Patrone in ms (500ms -> 0.5 sek)
            chicken_timer = 0  # Spawncounter für Chickens
            interval_ms = 150  # 90 zeit zwischen Spawns in ms

            while run:
                # hier events bzw. key-presses abfragen
                for event in pygame.event.get():

                    # wenn das Fenster geschlossen wird über das X oben rechts
                    if event.type == pygame.QUIT:
                        print("Safely quit game")
                        run = False
                        pygame.quit()

                    # wenn im spiel geschossen wird & nicht nachgeladen wird
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and reloading is False:
                        if game_ammo.count_full_ammo() > 0:  # Falls ammo vorhanden & immer die ammo ganz links benutzen
                            next_ammo = next(
                                ammo for ammo in game_ammo.all_ammo if not ammo.fired)  # ammo links suchen
                            next_ammo.fire()  # ammo verwenden
                            for chicken in all_Chickens:
                                if chicken.posCheck(event.pos):
                                    chicken.killHitbox()  # chicken object entfernen aus Spritegroup
                                    scoreInt += chicken.get_score()  # score je nach Chicken erhöhen

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # wenn Leertaste gedrückt wird
                        if not reloading and game_ammo.count_full_ammo() < 5:
                            reloading = True
                            reload_start_time = pygame.time.get_ticks()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        game_over.get_score(scoreInt)
                        state = "GameOver"
                        run = False

                # Timer fürs Nachladen, Chicken spawnen & verbleibende Spielzeit
                reload_time = pygame.time.get_ticks()
                game_time_left = int(60 - pygame.time.get_ticks() / 1000)
                chicken_timer += clock.get_rawtime()

                # Spawnzeiten für Chickens checken
                if chicken_timer >= interval_ms:
                    spawn_chicken = chickenGen(win)
                    all_Chickens.add(spawn_chicken)
                    # print("spawn")
                    chicken_timer = 0
                all_Chickens.update()

                # Reloadfunktion für zeitbasiertes Nachladen
                if reloading and game_ammo.count_full_ammo() < 5:
                    current_time = pygame.time.get_ticks()
                    if current_time - reload_start_time >= reload_interval:
                        # list(game_ammo.all_ammo) -> für reversed function
                        next_reload = next(ammo for ammo in reversed(list(game_ammo.all_ammo)) if ammo.fired)
                        next_reload.reload()  # einzelne ammo nachladen
                        reload_start_time = current_time  # zeit restarten
                if game_ammo.count_full_ammo() == 5:  # Falls ammo bereits Voll
                    reloading = False

                # Verschiedene Texte
                reloadingText = font.render("Reloading...", True, (255, 255, 0))
                scoreText = font.render("Score: " + str(scoreInt), True, (255, 255, 255))
                game_time_left_text = font.render("Time left:" + str(game_time_left), True, (255, 255, 255))

                # Anzeigen der Oberfläche & Chickens
                win.blit(background, (0, 0))
                win.blit(scoreText, (10, 10))
                win.blit(game_time_left_text, (175, 10))
                all_Chickens.draw(win)
                win.blit(grass, (-200, win.get_size()[1] - 300))
                game_ammo.draw_ammostack(win)
                win.blit(crosshair.cursorImage, crosshair.cursorImage_rect.topleft)

                # Das Crosshair bild konstant in der Mitte der Maus halten
                crosshair.cursorImage_rect.topleft = pygame.mouse.get_pos() - pygame.Vector2(
                    crosshair.cursorImage_rect.width / 2,
                    crosshair.cursorImage_rect.height / 2)

                # Checken von Ingamezuständen
                if reloading:
                    win.blit(reloadingText, (winSize[0] - 175, winSize[1] - 90))

                if game_time_left <= 0:
                    run = False
                    game_over.get_score(scoreInt)
                    state = "GameOver"
                    # save_score()

                pygame.display.update()  # updaten des displays falls

                clock.tick(60)  # Festlegen der Refreshrate, muss im gameloop passieren

            # Maus im GameOver screen sichtbar machen
            pygame.mouse.set_visible(True)

        if state == "main_menu":
            menu.draw(win)

        if state == "GameOver":
            game_over.draw(win)
            # wenn "back to main menu" im gameover screen gedrückt wird
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over.main_check(event.pos):
                state = "main_menu"
                pygame.display.update()

        pygame.display.flip()  # main_menu anzeigen
