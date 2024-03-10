import pygame


class Ammostack:
    def __init__(self):
        self.all_ammo = pygame.sprite.Group()

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

    def draw_ammostack(self, screen: pygame.Surface):
        count = 5
        winSize = screen.get_size()
        for ammo in self.all_ammo:
            screen.blit(ammo.image, (winSize[0] - 20 - count * (ammo.image.get_width()), winSize[1] - 125))
            count -= 1


class Ammo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ammo/pics/MunitionVoll.png")
        self.fired = False

    def fire(self):
        self.image = pygame.image.load("Ammo/pics/MunitionLeer.png")
        self.fired = True

    def reload(self):
        self.image = pygame.image.load("Ammo/pics/MunitionVoll.png")
        self.fired = False
