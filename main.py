import pygame
import sys

from player import Player
from enemy import Enemy

# Inizializza pygame
pygame.init()

# Dimensioni finestra
WIDTH = 1000
HEIGHT = 600

# Crea finestra
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Action Game")

# Clock FPS
clock = pygame.time.Clock()

# Colori
BACKGROUND_COLOR = (25, 25, 35)
camera_x = 0
font = pygame.font.SysFont(None, 40)

# Player
player = Player(100, 300)

enemy = Enemy(600, 480)

# Piattaforme
platforms = [
    pygame.Rect(0, 550, 3000, 50),
    pygame.Rect(300, 450, 200, 20),
    pygame.Rect(700, 350, 200, 20),
    pygame.Rect(1100, 420, 250, 20),
    pygame.Rect(1600, 300, 200, 20),
    pygame.Rect(2100, 500, 250, 20),
]

# Game loop
running = True

while running:

    # Eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input tastiera
    keys = pygame.key.get_pressed()

    # Update player
    player.update(keys, platforms)
    enemy.update(player)

    # Camera segue player
    camera_x = player.rect.x - WIDTH // 2

    if player.attacking and enemy.alive:

        if player.attack_rect.colliderect(enemy.rect):

            enemy.take_damage()

    # Disegna sfondo
    screen.fill(BACKGROUND_COLOR)

    # Disegna piattaforme
    for platform in platforms:

        shifted_platform = pygame.Rect(
            platform.x - camera_x,
            platform.y,
            platform.width,
            platform.height
        )

        pygame.draw.rect(screen, (80, 80, 80), shifted_platform)

    # Disegno player con camera
    shifted_player = player.rect.copy()
    shifted_player.x -= camera_x

    original_rect = player.rect
    player.rect = shifted_player

    player.draw(screen)

    player.rect = original_rect

    # Disegno nemico con camera
    shifted_enemy = enemy.rect.copy()
    shifted_enemy.x -= camera_x

    original_enemy_rect = enemy.rect
    enemy.rect = shifted_enemy

    enemy.draw(screen)

    enemy.rect = original_enemy_rect

    #Game over
    if player.health <= 0:
        running = False

    # HUD vita
    health_text = font.render(f"HP: {player.health}", True, (255, 255, 255))
    screen.blit(health_text, (20, 20))

    # Aggiorna schermo
    pygame.display.update()

    # FPS
    clock.tick(60)

pygame.quit()
sys.exit()