import pygame, sys
from pygame.locals import QUIT
import player
import constants
import lines

pygame.init()


DISPLAYSURF = pygame.display.set_mode((constants.X, constants.Y))
DISPLAYSURF.fill(pygame.Color("white"))
pygame.display.set_caption('Hello World!')

player = player.Player()

clock = pygame.time.Clock()

def draw(DISPLAYSURF):
    player.render(DISPLAYSURF)
    lines.draw(DISPLAYSURF, 8)

def update():
    player.update()

def key_pressed(key):
    if (key == pygame.K_ESCAPE or key == pygame.K_q):
        quit()
    player.key_pressed(key)

def quit():
    print('quitting')
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            key_pressed(event.key)

    update()
    DISPLAYSURF.fill(pygame.Color("white"))
    draw(DISPLAYSURF)
    pygame.display.update()
    clock.tick(30)