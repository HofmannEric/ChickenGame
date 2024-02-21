import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Moving rectangle")

x = 200
y = 200

width = 20
height = 20

vel = 10

run = True

while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            y += vel
    win.fill((0, 0, 0))

    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))

    pygame.display.update()

pygame.quit()
