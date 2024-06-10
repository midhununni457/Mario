import pygame
from requirements.settings import import_enemy_images

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        x, y = position
        self.import_enemy_images()
        self.frame_index = 0
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x + 25, y + 15))
        self.direction = pygame.math.Vector2(1, 0)
        self.speed = 3
        self.animation_speed = 0.12
        self.facing_right = True
        self.on_left = False
        self.on_right = False
        self.dead = False

    def import_enemy_images(self):
        path = 'requirements/enemy animation'
        self.animations = import_enemy_images(path)

    def animate(self):
        animation = self.animations
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            flipped = pygame.transform.flip(image, True, False)
            self.image = pygame.transform.scale(flipped, (40, 45))
        else:
            self.image = pygame.transform.scale(image, (40, 45))
        if self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
            self.direction.x = -1
        elif self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
            self.direction.x = 1
        else:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()