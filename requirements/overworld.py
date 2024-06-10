import pygame
from requirements.game_data import levels


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, speed, name):
        super().__init__()
        self.image_raw = pygame.image.load('requirements/Level/Overworld/' + name + '.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, (275, 220))
        if status == 'unlocked':
            self.status = 'unlocked'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center=pos)
        self.detection_zone = pygame.Rect(self.rect.centerx-(speed/2), self.rect.centery-(speed/2)-50, speed, speed)

    def update(self):
        if self.status == 'locked':
            tint_surf = self.image.copy()
            tint_surf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0, 0))

class Icon(pygame.sprite.Sprite):
    def __init__(self, node):
        super().__init__()
        self.pos = (node.rect.centerx, node.rect.centery-50)
        self.image = pygame.transform.scale(pygame.image.load('requirements/Level/Overworld/player icon.png').convert_alpha(), (45, 50))
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self, start_level, max_level, surface, create_level, life):
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.setup_nodes()
        self.setup_icon()
        self.life = life

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, level in levels.items():
            if index <= self.max_level:
                node_sprite = Node(level['node_position'], 'unlocked', self.speed, str(index))
            else:
                node_sprite = Node(level['node_position'], 'locked', self.speed, str(index))
            self.nodes.add(node_sprite)

    def draw_paths(self):
        if self.max_level != 1:
            points = [node['node_position'] for index, node in levels.items() if index <= self.max_level]
            pygame.draw.lines(self.display_surface, '#69392b', False, points, 7)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level-1])
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 1:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_RETURN]:
                self.create_level(self.current_level, self.life)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(levels[self.current_level]['node_position'])
        if target == 'next':
            end = pygame.math.Vector2(levels[self.current_level + 1]['node_position'])
        else:
            end = pygame.math.Vector2(levels[self.current_level - 1]['node_position'])
        return (end - start).normalize()

    def update_icon(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level-1]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)
            if self.move_direction.x < 0 and self.icon.sprite.rect.centerx < target_node.rect.centerx:
                self.icon.sprite.pos = levels[self.current_level]['node_position']
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)
            if self.move_direction.x > 0 and self.icon.sprite.rect.centery > target_node.rect.centerx:
                self.icon.sprite.pos = levels[self.current_level]['node_position']
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def run(self):
        self.input()
        self.update_icon()
        self.icon.update()
        self.nodes.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)