import pygame


def bild_laden(name):
    global image
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print("Cannot load image")
        image = image.convert()
    return image, image.get_rect()


class SmallChicken(pygame.sprite.Sprite):
    radius = int(10)
    trueX = bool(False)
    trueY = bool(False)

    def __init__(self, x, y, vel_x, vel_y):
        super().__init__()
        self.position = (x, y)
        self.velocity = (vel_x, vel_y)
        self.rect = bild_laden("ben_bild.png")
        self.image = pygame.image.load("ben_bild.png")
        self.image.get_rect()

    def update(self):
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    def draw(self, win):
        win.blit(self.image, self.position)
        pygame.draw.circle(win, (255, 0, 0), self.position, self.radius)

    def die(self):
        self.position = (-15, -15)

    def move(self):
        self.position = (self.position[0] + 1, self.position[1])

    def posCheck(self, eventpos):
        if self.rect.collidepoint(eventpos):
            return True
        else:
            return False



pygame.init()

win = pygame.display.set_mode((750, 500))

pygame.display.set_caption("Moving rectangle")
scoreInt = 0
score = "Score: " + str(scoreInt)
ui = pygame.font.Font

x = 200
y = 200
xx = 300
yy = 300

width = 20
height = 20
widthh = 25
heightt = 25

font = pygame.font.Font('freesansbold.ttf', 18)

vel = 10

# SpriteGroups
all_Chickens = pygame.sprite.Group()

small_Chicken = pygame.Rect(x, y, width, height)
medium_Chicken = pygame.Rect(xx, yy, widthh, heightt)
big_Chicken = pygame.sprite.Sprite()
# all_Chickens.add(small_Chicken)

testObj = SmallChicken(x, y, vel, vel)

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

        # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and medium_Chicken.collidepoint(event.pos):
        #   medium_Chicken.y = 500
        #   scoreInt += 1
    testObj.move()
    # small_Chicken.x += 1
    # medium_Chicken.x += 2
    # pygame.draw.rect(win, (255, 0, 0), small_Chicken)
    # pygame.draw.rect(win, (255, 255, 0), medium_Chicken)

    win.fill((0, 0, 0))

    score = "Score: " + str(scoreInt)
    text = font.render(score, True, (255, 0, 0))
    win.blit(text, (10, 10))

    testObj.draw(win)

    # pygame.draw.rect(win, (255, 0, 0), small_Chicken)
    # pygame.draw.rect(win, (255, 255, 0), medium_Chicken)

    pygame.display.update()

pygame.quit()
