import pygame
import sys
from requirements.settings import width, height
from requirements.level import Level
from requirements.overworld import Overworld

class Game:
    def __init__(self):
        self.life = 5
        self.max_level = 1
        self.overworld = Overworld(1, self.max_level, window, self.create_level, self.life)
        self.status = 'overworld'

    def create_level(self, current_level, life):
        self.level = Level(current_level, window, self.create_overworld, life)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level, life):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        elif new_max_level == 0:
            self.max_level = 1
        self.overworld = Overworld(current_level, self.max_level, window, self.create_level, life)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()

pygame.init()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mario')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
game = Game()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    bg_img = pygame.image.load('requirements/Level/bg.png').convert_alpha()
    bg = pygame.transform.scale(bg_img, (width, height))
    window.blit(bg, (0, 0))
    game.run()
    pygame.display.update()