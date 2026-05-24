import pygame
from projectile import Projectile

class Boss:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 120, 120)

        self.health = 20
        self.alive = True

        self.speed = 2

        self.projectiles = []

        self.attack_cooldown = 0

    def update(self, player):

        if not self.alive:
            return

        distance = player.rect.centerx - self.rect.centerx

        if abs(distance) > 300:

            if distance > 0:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if abs(distance) <= 350 and self.attack_cooldown == 0:

            direction = 1

            if distance < 0:
                direction = -1

            projectile = Projectile(
                self.rect.centerx,
                self.rect.centery,
                direction,
                (255, 80, 80),
                8
            )

            self.projectiles.append(projectile)

            self.attack_cooldown = 60

        for projectile in self.projectiles:
            projectile.update()

            if projectile.rect.colliderect(player.rect):
                player.take_damage()
                projectile.alive = False

        self.projectiles = [p for p in self.projectiles if p.alive]

    def take_damage(self):

        self.health -= 1

        if self.health <= 0:
            self.alive = False

    def attack_player(self, player):
        pass