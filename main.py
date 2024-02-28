import pygame

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

run = True

while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and small_Chicken.collidepoint(event.pos):
            small_Chicken.y = 500
            scoreInt -= 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and medium_Chicken.collidepoint(event.pos):
            medium_Chicken.y = 500
            scoreInt += 1
    small_Chicken.x += 1
    medium_Chicken.x += 2
    pygame.draw.rect(win, (255, 0, 0), small_Chicken)
    pygame.draw.rect(win, (255, 255, 0), medium_Chicken)

    win.fill((0, 0, 0))

    score = "Score: " + str(scoreInt)
    text = font.render(score, True, (255, 0, 0))
    win.blit(text, (10, 10))
    pygame.draw.rect(win, (255, 0, 0), small_Chicken)
    pygame.draw.rect(win, (255, 255, 0), medium_Chicken)

    pygame.display.update()

pygame.quit()
