import pygame
from os import walk
from random import randint

tile_size = 64
width = 1200
height = 704

def import_player_images(path):
    surface_list = []
    ht = [55, 58]
    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = path + '/' + img
            img_surf = pygame.image.load(full_path).convert_alpha()
            if path[-1] == 'e':
                img_surf = pygame.transform.scale(img_surf, (35, ht[randint(0, 1)]))
            elif path[-1] == 'n':
                img_surf = pygame.transform.scale(img_surf, (35, 57))
                img_surf = pygame.transform.rotate(img_surf, 330)
            elif path[-1] == 'p':
                img_surf = pygame.transform.scale(img_surf, (35, 57))
            elif path[-1] == 'l':
                img_surf = pygame.transform.scale(img_surf, (40, 57))
            surface_list.append(img_surf)
    return surface_list

def import_enemy_images(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = path + '/' + img
            img_surf_raw = pygame.image.load(full_path).convert_alpha()
            img_surf = pygame.transform.scale(img_surf_raw, (40, 45))
            surface_list.append(img_surf)
    return surface_list

def import_coin_images(coin):
    path = 'requirements/Level/Coins/' + coin
    surface_list = []
    img_surf_raw = pygame.image.load(path).convert_alpha()
    img_surf = pygame.transform.scale(img_surf_raw, (25, 25))
    surface_list.append(img_surf)
    return surface_list
