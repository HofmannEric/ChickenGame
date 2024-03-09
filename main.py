import pygame

from Ammunition import Ammostack
from ChickenGenerator import chickenGen
from Hauptmenu import MainMenu
from gameoverScreen import GameOver


def bild_laden(name):
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print("Cannot load image")
        image = image.convert()
    return image, image.get_rect()


pygame.init()

win = pygame.display.set_mode((1024, 526))
winSize = win.get_size()
pygame.display.set_caption("Chickens Game")

clock = pygame.time.Clock()
menu = MainMenu()


game_over = GameOver()

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
            scoreInt = 0
            font = pygame.font.Font('freesansbold.ttf', 18)

            # Umgebungsbilder
            background = pygame.image.load("Background & Ammo/background_test.png")
            grass = pygame.image.load("Background & Ammo/grass.png")

            cursorImage = pygame.image.load("Crosshair/crosshair.png")
            cursorImage_rect = cursorImage.get_rect()

            ammo_pic = pygame.image.load("Background & Ammo/MunitionVoll.png")

            # SpriteGroups
            all_Chickens = pygame.sprite.Group()

            game_ammo = Ammostack()
            game_ammo.gen_ammo()

            pygame.mouse.set_visible(False)

            # Main game loop
            run = True
            reloading = False

            reload_start_time = 0
            reload_interval = 500

            chicken_timer = 0  # Spawncounter für Chickens
            interval_ms = 150  # 90 zeit zwischen Spawns in ms


            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("Safely quit game")
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and reloading is False:
                        if game_ammo.count_full_ammo() > 0:
                            next_ammo = next(ammo for ammo in game_ammo.all_ammo if not ammo.fired)
                            next_ammo.fire()
                            for chicken in all_Chickens:
                                if chicken.posCheck(event.pos):
                                    chicken.kill()
                                    chicken.killHitbox()
                                    scoreInt += chicken.get_score()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        ammo_list = list(game_ammo.all_ammo)
                        if not reloading and game_ammo.count_full_ammo() < 5:
                            reloading = True
                            reload_start_time = pygame.time.get_ticks()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        game_over.get_score(scoreInt)
                        state = "GameOver"
                        run = False

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over.main_check(event.pos):
                        pygame.init()

                reload_time = pygame.time.get_ticks()
                game_time_left = int(60 - pygame.time.get_ticks() / 1000)  # gametime in sekunden
                chicken_timer += clock.get_rawtime()
                # print(chicken_timer)
                if chicken_timer >= interval_ms:
                    spawn_chicken = chickenGen(win)
                    all_Chickens.add(spawn_chicken)
                    # print("spawn")
                    chicken_timer = 0
                all_Chickens.update()

                if reloading and game_ammo.count_full_ammo() < 5:
                    current_time = pygame.time.get_ticks()
                    # blit reloading text
                    if current_time - reload_start_time >= reload_interval:
                        next_reload = next(ammo for ammo in reversed(ammo_list) if ammo.fired)
                        next_reload.reload()
                        reload_start_time = current_time
                if game_ammo.count_full_ammo() == 5:
                    reloading = False

                win.fill((0, 0, 0))
                # print("Current time:", current_time)
                reloadingText = font.render("Reloading...", True, (255, 255, 0))
                score = "Score: " + str(scoreInt)
                scoreText = font.render(score, True, (255, 255, 255))
                win.blit(background, (0, 0))
                win.blit(scoreText, (10, 10))

                game_time_left_text = font.render("Time left:" + str(game_time_left), True, (255, 255, 255))
                win.blit(game_time_left_text, (175, 10))

                cursorImage_rect.topleft = pygame.mouse.get_pos() - pygame.Vector2(cursorImage_rect.width // 2,
                                                                                   cursorImage_rect.height // 2)
                # win.blit(ammo_pic, (winSize[0] - 100, winSize[1] - 125))
                all_Chickens.draw(win)
                win.blit(grass, (-200, win.get_size()[1] - 300))
                game_ammo.draw_ammostack(win)

                if reloading:
                    win.blit(reloadingText, (winSize[0] - 175, winSize[1] - 90))

                if game_time_left <= 0:
                    run = False
                    game_over.get_score(scoreInt)
                    state = "GameOver"
                    # save_score()
                win.blit(cursorImage, cursorImage_rect.topleft)
                pygame.display.update()

                clock.tick(60)

            pygame.mouse.set_visible(True)
        # pygame.quit()

        win.fill((0, 0, 0))

        if state == "main_menu":
            menu.draw(win)

        if state == "GameOver":
            game_over.draw(win)

        pygame.display.flip()  # nötig um main menu zu zeigen
