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

enemies = [
    Enemy(600, 480),
    Enemy(1000, 480),
    Enemy(1400, 480),
]

boss = Boss(1700, 430)
final_boss = Boss(3000, 430)

boss_active = False
final_boss_active = False

platforms = [
    pygame.Rect(0, 550, 4000, 50),
    pygame.Rect(300, 450, 200, 20),
    pygame.Rect(700, 350, 200, 20),
    pygame.Rect(1100, 420, 250, 20),
    pygame.Rect(1600, 300, 200, 20),
    pygame.Rect(2200, 450, 200, 20),
    pygame.Rect(2600, 350, 200, 20),
]

checkpoint = pygame.Rect(2100, 470, 50, 80)

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player.update(keys, platforms)

    camera_x = player.rect.x - WIDTH // 2

    for e in enemies:
        e.update(player)

    # PLAYER ATTACKS ENEMIES

    for e in enemies:

        if player.attacking and e.alive:
            if player.attack_rect.colliderect(e.rect):
                e.take_damage()

        for projectile in player.projectiles:
            if e.alive and projectile.rect.colliderect(e.rect):
                e.take_damage()
                projectile.alive = False

    # MID BOSS ACTIVATION

    if not boss_active:

        all_dead = True

        for e in enemies:
            if e.alive:
                all_dead = False

        if all_dead:
            boss_active = True

    # MID BOSS

    if boss_active and boss.alive:

        boss.update(player)

        if player.attacking:
            if player.attack_rect.colliderect(boss.rect):
                boss.take_damage()

        for projectile in player.projectiles:
            if projectile.rect.colliderect(boss.rect):
                boss.take_damage()
                projectile.alive = False

    # FINAL BOSS ACTIVATION

    if boss_active and not boss.alive:
        final_boss_active = True

    # FINAL BOSS

    if final_boss_active and final_boss.alive:

        final_boss.update(player)

        if player.attacking:
            if player.attack_rect.colliderect(final_boss.rect):
                final_boss.take_damage()

        for projectile in player.projectiles:
            if projectile.rect.colliderect(final_boss.rect):
                final_boss.take_damage()
                projectile.alive = False

    # ENEMY DAMAGE

    for e in enemies:
        e.attack_player(player)

    # CHECKPOINT

    if player.rect.colliderect(checkpoint):
        save_game(player.rect.x, player.rect.y)

    # GAME OVER

    if player.health <= 0:
        running = False

    # WIN

    if final_boss_active and not final_boss.alive:
        print("YOU WIN")
        running = False

    # DRAW

    screen.fill(BACKGROUND)

    for p in platforms:

        pygame.draw.rect(
            screen,
            (80, 80, 80),
            (p.x - camera_x, p.y, p.width, p.height)
        )

    pygame.draw.rect(
        screen,
        (80, 255, 80),
        (checkpoint.x - camera_x, checkpoint.y, 50, 80)
    )

    # PLAYER

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

    # SWORD ATTACK

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

    # PLAYER PROJECTILES

    for projectile in player.projectiles:
        projectile.draw(screen, camera_x)

    # ENEMIES

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

    # MID BOSS

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

        for projectile in boss.projectiles:
            projectile.draw(screen, camera_x)

    # FINAL BOSS

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

        for projectile in final_boss.projectiles:
            projectile.draw(screen, camera_x)

    # HUD

    hp = font.render(f"HP: {player.health}", True, (255, 255, 255))
    screen.blit(hp, (20, 20))

    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()