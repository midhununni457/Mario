import pygame
from requirements.settings import import_coin_images

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, size, name):
        super().__init__()
        self.image_raw = pygame.image.load('requirements/Level/Tiles/' + name + '.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, (size, size))
        self.rect = self.image.get_rect(topleft=position)

    def update(self, x_shift):
        self.rect.x += x_shift

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        if name == '1':
            size = (150, 140)
            x -= 50
            y -= 75
        elif name == '2':
            size = (73, 47)
            x += 90
            y += 20
        elif name == '3':
            size = (60, 60)
            x += 30
            y += 5
        elif name == '4':
            size = (35, 30)
            x += 20
            y += 35
        self.image_raw = pygame.image.load('requirements/Level/Objects/' + name + '.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, size)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_shift):
        self.rect.x += x_shift

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, coin):
        super().__init__()
        self.position = (x + 20, y + 30)
        self.coin_image = import_coin_images(coin + '.png')
        self.image = self.coin_image[0].convert_alpha()
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self, x_shift):
        self.rect.x += x_shift

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        size = (130, 130)
        x -= 35
        y += 5
        self.image_raw = pygame.image.load('requirements/Level/Objects/goal.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, size)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_shift):
        self.rect.x += x_shift

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        size = (50, 25)
        y += 25
        self.image_raw = pygame.image.load('requirements/Level/Objects/key.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, size)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_shift):
        self.rect.x += x_shift