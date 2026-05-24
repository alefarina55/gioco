import pygame
import sys

from player import Player
from enemy import Enemy
from boss import Boss
from save_system import save_game, load_game

pygame.init()

WIDTH, HEIGHT = 1000, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Action Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)

BACKGROUND = (25, 25, 35)

camera_x = 0

spawn_x, spawn_y = load_game()

player = Player(spawn_x, spawn_y)

# ---------------- ENEMIES ----------------

enemies = [
    Enemy(600, 480),
    Enemy(1000, 480),
    Enemy(1400, 480),
]

# ---------------- BOSSES ----------------

boss = Boss(1700, 430)
final_boss = Boss(3000, 430)

boss_active = False
final_boss_active = False

# ---------------- PLATFORMS ----------------

platforms = [
    pygame.Rect(0, 550, 4000, 50),

    pygame.Rect(300, 450, 200, 20),
    pygame.Rect(700, 350, 200, 20),
    pygame.Rect(1100, 420, 250, 20),

    pygame.Rect(1600, 300, 200, 20),

    pygame.Rect(2200, 450, 200, 20),
    pygame.Rect(2600, 350, 200, 20),
]

# ---------------- CHECKPOINT ----------------

checkpoint = pygame.Rect(2100, 470, 50, 80)

running = True

while running:

    # ---------------- EVENTS ----------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # ---------------- PLAYER ----------------

    player.update(keys, platforms)

    camera_x = player.rect.x - WIDTH // 2

    # ---------------- ENEMIES ----------------

    for e in enemies:
        e.update(player)

    # DAMAGE ENEMIES

    for e in enemies:

        if player.attacking and e.alive:
            if player.attack_rect.colliderect(e.rect):
                e.take_damage()

        if player.elemental_attacking and e.alive:
            if player.elemental_rect.colliderect(e.rect):
                e.take_damage()

    # ---------------- ACTIVATE MID BOSS ----------------

    if not boss_active:

        all_dead = True

        for e in enemies:
            if e.alive:
                all_dead = False

        if all_dead:
            boss_active = True

    # ---------------- MID BOSS ----------------

    if boss_active and boss.alive:

        boss.update(player)

        if player.attacking:
            if player.attack_rect.colliderect(boss.rect):
                boss.take_damage()

        if player.elemental_attacking:
            if player.elemental_rect.colliderect(boss.rect):
                boss.take_damage()

        boss.attack_player(player)

    # ---------------- ACTIVATE FINAL BOSS ----------------

    if boss_active and not boss.alive:
        final_boss_active = True

    # ---------------- FINAL BOSS ----------------

    if final_boss_active and final_boss.alive:

        final_boss.update(player)

        if player.attacking:
            if player.attack_rect.colliderect(final_boss.rect):
                final_boss.take_damage()

        if player.elemental_attacking:
            if player.elemental_rect.colliderect(final_boss.rect):
                final_boss.take_damage()

        final_boss.attack_player(player)

    # ---------------- DAMAGE PLAYER ----------------

    for e in enemies:
        e.attack_player(player)

    # ---------------- CHECKPOINT ----------------

    if player.rect.colliderect(checkpoint):
        save_game(player.rect.x, player.rect.y)

    # ---------------- GAME OVER ----------------

    if player.health <= 0:
        running = False

    # ---------------- WIN ----------------

    if final_boss_active and not final_boss.alive:
        print("YOU WIN")
        running = False

    # ---------------- DRAW ----------------

    screen.fill(BACKGROUND)

    # Platforms

    for p in platforms:

        pygame.draw.rect(
            screen,
            (80, 80, 80),
            (p.x - camera_x, p.y, p.width, p.height)
        )

    # Checkpoint

    pygame.draw.rect(
        screen,
        (80, 255, 80),
        (checkpoint.x - camera_x, checkpoint.y, 50, 80)
    )

    # Player

    pygame.draw.rect(
        screen,
        (220, 220, 220),
        (
            player.rect.x - camera_x,
            player.rect.y,
            player.rect.width,
            player.rect.height
        )
    )

    # Attack

    if player.attacking:

        pygame.draw.rect(
            screen,
            (255, 80, 80),
            (
                player.attack_rect.x - camera_x,
                player.attack_rect.y,
                player.attack_rect.width,
                player.attack_rect.height
            )
        )

    # Elemental

    if player.elemental_attacking:

        pygame.draw.rect(
            screen,
            (80, 180, 255),
            (
                player.elemental_rect.x - camera_x,
                player.elemental_rect.y,
                player.elemental_rect.width,
                player.elemental_rect.height
            )
        )

    # Enemies

    for e in enemies:

        if e.alive:

            pygame.draw.rect(
                screen,
                (200, 60, 60),
                (
                    e.rect.x - camera_x,
                    e.rect.y,
                    e.rect.width,
                    e.rect.height
                )
            )

    # Mid Boss

    if boss_active and boss.alive:

        pygame.draw.rect(
            screen,
            (120, 0, 180),
            (
                boss.rect.x - camera_x,
                boss.rect.y,
                boss.rect.width,
                boss.rect.height
            )
        )

    # Final Boss

    if final_boss_active and final_boss.alive:

        pygame.draw.rect(
            screen,
            (180, 0, 0),
            (
                final_boss.rect.x - camera_x,
                final_boss.rect.y,
                final_boss.rect.width,
                final_boss.rect.height
            )
        )

    # HUD

    hp = font.render(f"HP: {player.health}", True, (255, 255, 255))
    screen.blit(hp, (20, 20))

    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()