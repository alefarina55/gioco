import pygame

class Player:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 70)

        self.speed = 5

        # salto / fisica
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = 10
        self.on_ground = False

    def move(self, keys):

        # movimento laterale
        if keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_d]:
            self.rect.x += self.speed

        # salto
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False

    def apply_gravity(self):

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # pavimento (ground semplice)
        if self.rect.y >= 500:
            self.rect.y = 500
            self.vel_y = 0
            self.on_ground = True

    def update(self, keys):
        self.move(keys)
        self.apply_gravity()

    def draw(self, screen):
        pygame.draw.rect(screen, (220, 220, 220), self.rect)