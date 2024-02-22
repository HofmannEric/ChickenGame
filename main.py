import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Moving rectangle")

x = 200
y = 200

width = 20
height = 20

vel = 10

event_rect = pygame.Rect(x, y, width, height)

run = True


def fallen():
    event_rect.x += 1
    pygame.draw.rect(win, (255, 0, 0), event_rect)
    pygame.time.wait(100)
    event_rect.y += 1
    pygame.draw.rect(win, (255, 0, 0), event_rect)
    pygame.time.wait(100)
    event_rect.y += 1
    pygame.draw.rect(win, (255, 0, 0), event_rect)
    pygame.time.wait(100)
    event_rect.y += 1
    pygame.draw.rect(win, (255, 0, 0), event_rect)
    pygame.time.wait(100)
    event_rect.y += 1
    pygame.draw.rect(win, (255, 0, 0), event_rect)
    pygame.time.wait(100)
    event_rect.y += 1
    pygame.draw.rect(win, (255, 0, 0), event_rect)
    pygame.time.wait(100)
    event_rect.y += 1
    pygame.draw.rect(win, (255, 0, 0), event_rect)
    pygame.time.wait(100)
    event_rect.y += 1
    pygame.draw.rect(win, (255, 0, 0), event_rect)



while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event_rect.collidepoint(event.pos):
            event_rect.y += vel
            fallen()

    win.fill((0, 0, 0))

    pygame.draw.rect(win, (255, 0, 0), event_rect)

    pygame.display.update()

pygame.quit()
