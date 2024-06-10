import pygame
from requirements.settings import import_player_images

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.import_player_images()
        self.frame_index = 0
        self.animation_speed = 0.10
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.9
        self.jump_speed = -19
        self.status = 'idle'
        self.facing_right = True
        self.on_floor = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.immunity = False

    def import_player_images(self):
        folder_path = 'requirements/player animation/'
        self.animations = {'idle' : [], 'run' : [], 'jump' : [], 'fall' : []}
        for action in self.animations.keys():
            path = folder_path + action
            self.animations[action] = import_player_images(path)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = pygame.transform.scale(image, (image.get_width(), 57))
        else:
            flipped = pygame.transform.flip(image, True, False)
            self.image = pygame.transform.scale(flipped, (image.get_width(), 57))
        if self.on_floor and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_floor and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_floor:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.facing_right = True
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.facing_right = False
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_floor:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()