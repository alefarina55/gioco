import pygame

class Projectile:

    def __init__(self, x, y, direction, color=(80, 180, 255), speed=10):

        self.rect = pygame.Rect(x, y, 20, 10)

        self.direction = direction
        self.speed = speed
        self.color = color

        self.alive = True

    def update(self):

        self.rect.x += self.speed * self.direction

        if self.rect.x < -100 or self.rect.x > 5000:
            self.alive = False

    def draw(self, screen, camera_x):

        pygame.draw.rect(
            screen,
            self.color,
            (
                self.rect.x - camera_x,
                self.rect.y,
                self.rect.width,
                self.rect.height
            )
        )