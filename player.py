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

        # Direzione player
        self.facing_right = True

        # Attacco
        self.attacking = False
        self.attack_timer = 0

        self.attack_rect = pygame.Rect(0, 0, 40, 20)

    def move(self, keys):

        # Movimento orizzontale
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing_right = False

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing_right = True

        # Salto
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False

    def attack(self, keys):

        if keys[pygame.K_j] and not self.attacking:

            self.attacking = True
            self.attack_timer = 15

        if self.attacking:

            self.attack_timer -= 1

            # Posizione hitbox
            if self.facing_right:
                self.attack_rect.x = self.rect.right
            else:
                self.attack_rect.x = self.rect.left - 40

            self.attack_rect.y = self.rect.y + 20

            if self.attack_timer <= 0:
                self.attacking = False

    def apply_gravity(self):

        self.vel_y += self.gravity

        if self.vel_y > 15:
            self.vel_y = 15

        self.rect.y += self.vel_y

    def check_collision(self, platforms):

        self.on_ground = False

        for platform in platforms:

            if self.rect.colliderect(platform):

                if self.vel_y > 0:

                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True

    def update(self, keys, platforms):

        self.move(keys)

        self.attack(keys)

        self.apply_gravity()

        self.check_collision(platforms)

    def draw(self, screen):

        # Player
        pygame.draw.rect(screen, (220, 220, 220), self.rect)

        # Hitbox attacco
        if self.attacking:
            pygame.draw.rect(screen, (255, 80, 80), self.attack_rect)