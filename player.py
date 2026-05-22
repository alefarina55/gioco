import pygame

class Player:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 70)

        self.speed = 5

    def move(self, keys):

        if keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_d]:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (220, 220, 220), self.rect)