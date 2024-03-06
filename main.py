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
    def __init__(self, image_path, x_range, y_range, velocity):
        super().__init__()
        self.image, self.rect = bild_laden(image_path)
        x = random.randint(*x_range)
        y = random.randint(*y_range)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity, 0)

    def update(self):
        self.position += self.velocity
        self.rect.topleft = self.position

    def draw(self, win):
        win.blit(self.image, self.position)

    def posCheck(self, eventpos):
        rect = self.image.get_rect(topleft=self.position)
        return rect.collidepoint(eventpos)


pygame.init()

win = pygame.display.set_mode((750, 500))
pygame.display.set_caption("Chickens Game")

scoreInt = 0
font = pygame.font.Font('freesansbold.ttf', 18)

background = pygame.image.load("background_test.png")
cursorImage = pygame.image.load("smallChickenPic.png")

cursorImage, cursorImage_rect = bild_laden("smallChickenPic.png")

vel = 4

# SpriteGroups
all_Chickens = pygame.sprite.Group()
pygame.mouse.set_visible(False)
chickens = [
    Chicken("bigChickenPic.png", (1, 5), (15, 450), 3),
    Chicken("mediumChickenPic.png", (1, 5), (150, 450), 2),
    Chicken("BigChickenPic.png", (1, 5), (15, 450), 1)
]
all_Chickens.add(chickens)

# Main game loop
run = True
clock = pygame.time.Clock()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for chicken in chickens:
                if chicken.posCheck(event.pos):
                    chicken.kill()
                    scoreInt += 1

    all_Chickens.update()

    win.fill((0, 0, 0))
    current_time = int(pygame.time.get_ticks() / 1000)
    print("Current time:", current_time)
    score = "Score: " + str(scoreInt)
    text = font.render(score, True, (255, 0, 0))
    win.blit(background, (0, 0))
    win.blit(text, (10, 10))

    cursorImage_rect.topleft = pygame.mouse.get_pos() - pygame.Vector2(cursorImage_rect.width // 2, cursorImage_rect.height // 2)
    all_Chickens.draw(win)
    win.blit(cursorImage, cursorImage_rect.topleft)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
