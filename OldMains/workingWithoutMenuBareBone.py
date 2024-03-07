import random
import pygame

def bild_laden(name):
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print("Cannot load image")
        image = image.convert()
    return image, image.get_rect()


class Chicken(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y_range, velocity):
        super().__init__()
        self.image, self.rect = bild_laden(image_path)
        y = random.randint(
            *y_range)  # random y Koordinate, das *y_range "entpackt" quasi die beiden als (a,b) übergebenen Werte
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity, 0)

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

    def killHitbox(self):
        self.kill()


pygame.init()

win = pygame.display.set_mode((1024, 526))
pygame.display.set_caption("Chickens Game")

clock = pygame.time.Clock()

scoreInt = 0
font = pygame.font.Font('freesansbold.ttf', 18)

background = pygame.image.load("../background_test.png")

cursorImage, cursorImage_rect = bild_laden("../crosshair.png")

# SpriteGroups
all_Chickens = pygame.sprite.Group()
pygame.mouse.set_visible(False)

# Main game loop
run = True


chicken_timer = 0  # Spawncounter für Chickens
interval_ms = 90  # zeit zwischen Spawns in ms


def chickenGen():
    seite_links = int(-25)
    seite_rechts = int(win.get_size()[0] + 25)
    rand_chicken = random.randint(1, 3)  # 1=small 2=medium 3=big

    rand_spawnseite = random.choice([seite_links, seite_rechts])

    vel = 1 if rand_spawnseite == seite_links else -1

    new_chicken = None

    if rand_chicken == 1:
        new_chicken = Chicken("../smallChickenPic.png", rand_spawnseite, (15, 450), vel * random.randint(3, 4))
    elif rand_chicken == 2:
        new_chicken = Chicken("../mediumChickenPic.png", rand_spawnseite, (15, 450), vel * random.randint(2, 3))
    elif rand_chicken == 3:
        new_chicken = Chicken("../bigChickenPic.png", rand_spawnseite, (150, 450), vel * random.randint(1, 2))

    return new_chicken


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for chicken in all_Chickens:
                if chicken.posCheck(event.pos):
                    chicken.kill()
                    chicken.killHitbox()
                    scoreInt += 1

    chicken_timer += clock.get_rawtime()
    print(chicken_timer)
    if chicken_timer >= interval_ms:
        spawn_chicken = chickenGen()
        all_Chickens.add(spawn_chicken)
        print("spawn")
        chicken_timer = 0
    all_Chickens.update()

    win.fill((0, 0, 0))
    current_time = int(pygame.time.get_ticks() / 1000)
    # print("Current time:", current_time)
    score = "Score: " + str(scoreInt)
    text = font.render(score, True, (255, 0, 0))
    win.blit(background, (0, 0))
    win.blit(text, (10, 10))

    cursorImage_rect.topleft = pygame.mouse.get_pos() - pygame.Vector2(cursorImage_rect.width // 2,
                                                                       cursorImage_rect.height // 2)
    all_Chickens.draw(win)
    win.blit(cursorImage, cursorImage_rect.topleft)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
