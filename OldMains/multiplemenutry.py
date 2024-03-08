import random
import pygame
import sqlite3


class Ammo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../MunitionVoll.png")
        self.fired = False

    def fire(self):
        self.image = pygame.image.load("../MunitionLeer.png")
        self.fired = True

    def reload(self):
        self.image = pygame.image.load("../MunitionVoll.png")
        self.fired = False


class Ammostack:
    def __init__(self):
        self.all_ammo = pygame.sprite.Group()
        self.shots_left = 5

    def gen_ammo(self):
        count = 0
        while count < 5:
            self.all_ammo.add(Ammo())
            count += 1

    def count_full_ammo(self):
        count = 0
        for ammo in self.all_ammo:
            if not ammo.fired:
                count += 1
        return count

    def draw_ammostack(self, screen):
        count = 5
        for ammo in self.all_ammo:
            screen.blit(ammo.image, (winSize[0] - 20 - count * (ammo.image.get_size()[0]), winSize[1] - 125))
            count -= 1


class MainMenu:
    def __init__(self, screen):
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.start_button = pygame.Rect(25, 200, 220, 50)
        self.leaderboard_title = pygame.Rect(750, 140, 220, 50)
        self.leaderboard_placements = [
            pygame.Rect(750, 200, 220, 35),
            pygame.Rect(750, 240, 220, 35),
            pygame.Rect(750, 280, 220, 35),
            pygame.Rect(750, 320, 220, 35),
            pygame.Rect(750, 360, 220, 35)
        ]
        self.Highscores = []

    def draw(self, screen):
        mm_background = pygame.image.load("../background_test.png")
        screen.blit(mm_background, (0, 0))
        pygame.draw.rect(screen, (133, 166, 45), self.start_button)
        start_text = self.font.render("Start Game", True, (255, 255, 255))
        screen.blit(start_text, (self.start_button.x + 10, self.start_button.y + 10))

        self.get_highscores()
        # drawing the Leaderboard

        pygame.draw.rect(screen, (100, 100, 100), self.leaderboard_title)
        highscore_text = self.font.render("Highscores:", True, (255, 255, 255))
        screen.blit(highscore_text, (self.leaderboard_title.x + 10, self.leaderboard_title.y + 10))

        highscore_counter = 0
        while highscore_counter < 5:
            pygame.draw.rect(screen, (150, 0, 0), self.leaderboard_placements[highscore_counter])
            print("drawn rect")

            if self.Highscores.__len__() > highscore_counter:
                highscore_text_raw = str(self.Highscores[highscore_counter][1]) + " || " + \
                                     str(self.Highscores[highscore_counter][0])
                highscore_text = self.font.render(highscore_text_raw, True, (255, 255, 255))
                screen.blit(highscore_text, (self.leaderboard_placements[highscore_counter].x + 5,
                                             self.leaderboard_placements[highscore_counter].y))
                print("blitted text")
            highscore_counter += 1

    def get_highscores(self):
        conn = sqlite3.connect('Highscores.db')
        cursor = conn.cursor()
        cursor.execute(
            '''Create Table if not exists leaderboard (id Integer PRIMARY KEY, player_name TEXT, score INTEGER)''')
        # cursor.execute('''Insert into leaderboard (player_name, score) values ('eric', 5)''')
        cursor.execute('''select * from leaderboard Order by score DESC LIMIT 5''')
        self.Highscores = cursor.fetchall()
        conn.commit()
        conn.close()

    def start_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button.collidepoint(event.pos):
                return "start_game"
        return None


def bild_laden(name):
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print("Cannot load image")
        image = image.convert()
    return image, image.get_rect()


class Chicken(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y_range, velocity, chicken_score):
        super().__init__()
        self.image, self.rect = bild_laden(image_path)
        y = random.randint(
            *y_range)  # random y Koordinate, das *y_range "entpackt" quasi die beiden als (a,b) übergebenen Werte
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity, 0)
        self.score = chicken_score

    def update(self):
        self.position += self.velocity
        self.rect.topleft = self.position

    def draw(self, win):
        win.blit(self.image, self.position)

    def posCheck(self, eventpos):
        if self.rect is not None:
            rect = self.image.get_rect(topleft=self.position)
            return rect.collidepoint(eventpos)
        return False

    def get_score(self):
        return self.score

    def killHitbox(self):
        self.kill()


pygame.init()

win = pygame.display.set_mode((1024, 526))
winSize = win.get_size()
pygame.display.set_caption("Chickens Game")

clock = pygame.time.Clock()
menu = MainMenu(win)

state = "main_menu"


def save_score(save_name, save_score):
    conn = sqlite3.connect('Highscores.db')
    cursor = conn.cursor()
    cursor.execute('''Insert into leaderboard (player_name, score) values (?,?)''', (save_name, save_score))
    conn.commit()
    conn.close()


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
            background = pygame.image.load("../background_test.png")
            grass = pygame.image.load("../grass.png")

            cursorImage, cursorImage_rect = bild_laden("../crosshair.png")

            ammo_pic = pygame.image.load("../MunitionVoll.png")

            # SpriteGroups
            all_Chickens = pygame.sprite.Group()

            game_ammo = Ammostack()
            game_ammo.gen_ammo()

            pygame.mouse.set_visible(False)

            # Main game loop
            run = True
            reloading = False

            # Timers & Intervalle
            # reload_timer = 0
            # reload_interval = 15
            reload_start_time = 0
            reload_interval = 500

            chicken_timer = 0  # Spawncounter für Chickens
            interval_ms = 150  # 90 zeit zwischen Spawns in ms


            def chickenGen():
                seite_links = int(-25)
                seite_rechts = int(win.get_size()[0] + 25)
                rand_chicken = random.randint(1, 3)  # 1=small 2=medium 3=big

                rand_spawnseite = random.choice([seite_links, seite_rechts])

                vel = 1 if rand_spawnseite == seite_links else -1  # Entscheidung der Richtung
                side = "L" if rand_spawnseite == seite_links else "R"  # Richtige sprites für Richtung

                new_chicken = None

                if rand_chicken == 1:
                    new_chicken = Chicken("../ChickenPics/small_" + side + ".png", rand_spawnseite, (15, 250),
                                          vel * random.randint(3, 4), 3)
                elif rand_chicken == 2:
                    new_chicken = Chicken("../ChickenPics/medium_" + side + ".png", rand_spawnseite, (15, 250),
                                          vel * random.randint(2, 3), 2)
                elif rand_chicken == 3:
                    new_chicken = Chicken("../ChickenPics/big_" + side + ".png", rand_spawnseite, (15, 250),
                                          vel * random.randint(1, 2), 1)

                return new_chicken


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
                        save_score()
                        run = False
                        state = "main_menu"
                reload_time = pygame.time.get_ticks()
                game_time_left = int(60 - pygame.time.get_ticks() / 1000)  # gametime in sekunden
                chicken_timer += clock.get_rawtime()
                # print(chicken_timer)
                if chicken_timer >= interval_ms:
                    spawn_chicken = chickenGen()
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
                    state = "main_menu"
                    save_score()
                win.blit(cursorImage, cursorImage_rect.topleft)
                pygame.display.update()

                clock.tick(60)

            pygame.mouse.set_visible(True)
        # pygame.quit()

        win.fill((0, 0, 0))

        if state == "main_menu":
            menu.draw(win)

        pygame.display.flip()  # nötig um main menu zu zeigen
