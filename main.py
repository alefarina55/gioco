import pygame
import sys

from player import Player

pygame.init()

WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Action Game")

clock = pygame.time.Clock()

BACKGROUND_COLOR = (25, 25, 35)

# Player
player = Player(100, 400)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input tastiera
    keys = pygame.key.get_pressed()

    # Movimento player
    player.update(keys)

    # Sfondo
    screen.fill(BACKGROUND_COLOR)

    # Disegna player
    player.draw(screen)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()