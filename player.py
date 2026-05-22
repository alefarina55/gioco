import pygame

class Player:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 50, 70)

        # Movimento
        self.speed = 5

        # Fisica
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = 10

        # Stato
        self.on_ground = False

    def move(self, keys):

        # Movimento orizzontale
        if keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_d]:
            self.rect.x += self.speed

        # Salto
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False

    def apply_gravity(self):

        self.vel_y += self.gravity

        # Limite caduta
        if self.vel_y > 15:
            self.vel_y = 15

        self.rect.y += self.vel_y

    def check_collision(self, platforms):

        self.on_ground = False

        for platform in platforms:

            if self.rect.colliderect(platform):

                # Collisione dall'alto
                if self.vel_y > 0:

                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True

    def update(self, keys, platforms):

        self.move(keys)

        self.apply_gravity()

        self.check_collision(platforms)

    def draw(self, screen):

        pygame.draw.rect(screen, (220, 220, 220), self.rect)