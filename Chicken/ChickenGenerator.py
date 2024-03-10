import pygame
import random


class Chicken(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y_range, velocity, chicken_score):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
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


def chickenGen(screen: pygame.surface):
    seite_links = int(-25)
    seite_rechts = int(screen.get_size()[0] + 25)
    rand_chicken = random.randint(1, 3)  # 1=small 2=medium 3=big

    rand_spawnseite = random.choice([seite_links, seite_rechts])

    vel = 1 if rand_spawnseite == seite_links else -1  # Entscheidung der Richtung
    side = "L" if rand_spawnseite == seite_links else "R"  # Richtige sprites für Richtung

    new_chicken = None

    if rand_chicken == 1:
        new_chicken = Chicken("Chicken/pics/small_" + side + ".png", rand_spawnseite, (15, 250),
                              vel * random.randint(3, 4), 3)
    elif rand_chicken == 2:
        new_chicken = Chicken("Chicken/pics/medium_" + side + ".png", rand_spawnseite, (15, 250),
                              vel * random.randint(2, 3), 2)
    elif rand_chicken == 3:
        new_chicken = Chicken("Chicken/pics/big_" + side + ".png", rand_spawnseite, (15, 250),
                              vel * random.randint(1, 2), 1)

    return new_chicken
