import pygame
import sys

# Inizializza pygame
pygame.init()

# Dimensioni finestra
WIDTH = 1000
HEIGHT = 600

# Crea finestra
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Titolo finestra
pygame.display.set_caption("2D Action Game")

# Clock per FPS
clock = pygame.time.Clock()

# Colori
BACKGROUND_COLOR = (25, 25, 35)

# Game loop
running = True

while running:

    # Eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Sfondo
    screen.fill(BACKGROUND_COLOR)

    # Aggiorna schermo
    pygame.display.update()

    # 60 FPS
    clock.tick(60)

# Chiusura gioco
pygame.quit()
sys.exit()