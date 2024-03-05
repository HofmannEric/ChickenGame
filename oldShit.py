import random

import pygame


def bild_laden(name):
    global image
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print("Cannot load image")
        image = image.convert()
    return image, image.get_rect()


class BigChicken(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image, self.rect = bild_laden("BigChickenPic.png")
        x = random.randint(1, 5)
        y = random.randint(15, 450)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(1, 0)

    def update(self):
        self.position += self.velocity
        self.rect.topleft = self.position

    def draw(self, win):
        win.blit(self.image, self.position)

    def posCheck(self, eventpos):
        rect = self.image.get_rect(topleft=self.position)
        if rect.collidepoint(eventpos):
            return True
        else:
            return False


class MediumChicken(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image, self.rect = bild_laden("mediumChickenPic.png")
        x = random.randint(1, 5)
        y = random.randint(150, 450)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(2, 0)

    def update(self):
        self.position += self.velocity
        self.rect.topleft = self.position

    def draw(self, win):
        win.blit(self.image, self.position)

    def posCheck(self, eventpos):
        rect = self.image.get_rect(topleft=self.position)
        if rect.collidepoint(eventpos):
            return True
        else:
            return False


class SmallChicken(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image, self.rect = bild_laden("bigChickenPic.png")
        x = random.randint(1, 5)
        y = random.randint(15, 450)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(3, 0)

    def update(self):
        self.position += self.velocity
        self.rect.topleft = self.position

    def draw(self, win):
        win.blit(self.image, self.position)

    def posCheck(self, eventpos):
        rect = self.image.get_rect(topleft=self.position)
        if rect.collidepoint(eventpos):
            return True
        else:
            return False


pygame.init()

win = pygame.display.set_mode((750, 500))

pygame.display.set_caption("Moving rectangle")
scoreInt = 0
score = "Score: " + str(scoreInt)
ui = pygame.font.Font

font = pygame.font.Font('freesansbold.ttf', 18)

vel = 4

# SpriteGroups
all_Chickens = pygame.sprite.Group()

testObj = SmallChicken()
testObj2 = MediumChicken()
all_Chickens.add(testObj)

testObj3 = BigChicken()

def SpawnChickens():
    x = 1

run = True

while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and testObj.posCheck(event.pos) == True:
            print(event.pos)
            print(testObj.position)
            scoreInt += 1
            testObj.kill()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and testObj2.posCheck(event.pos) == True:
            scoreInt += 1
            testObj2.kill()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and testObj3.posCheck(event.pos) == True:
            testObj3.kill()
            scoreInt += 1


    testObj.update()
    testObj2.update()
    testObj3.update()

    win.fill((0, 0, 0))
    current_time = int(pygame.time.get_ticks() / 1000)
    print("Current time:", current_time)
    score = "Score: " + str(scoreInt)
    text = font.render(score, True, (255, 0, 0))
    win.blit(text, (10, 10))

    testObj.draw(win)
    testObj2.draw(win)
    testObj3.draw(win)
    pygame.display.update()

pygame.quit()