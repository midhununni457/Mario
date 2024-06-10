import pygame
import time
from requirements.groups import Tile, Object, Coin, Goal, Key
from requirements.settings import tile_size, width, height
from requirements.player import Player
from requirements.enemy import Enemy
from requirements.game_data import levels

class Level:
    def __init__(self, current_level, surface, create_overworld, life):
        # General
        self.display_surface = surface
        self.max_score = 0
        self.draw_level(current_level)
        self.screen_shift = 0
        self.current_x = 0
        self.frame_speed = 0
        self.create_overworld = create_overworld
        self.current_level = current_level
        self.new_max_level = levels[self.current_level]['unlock']
        self.life = life
        # Timers
        self.life_timer = 0
        self.game_over_timer = 0
        # Coin count
        self.gold_coin_count = 0
        self.silver_coin_count = 0
        # Font
        self.items_font = pygame.font.SysFont('bahnschrift', 40)
        # Images
        self.gold_coin_img = pygame.transform.scale(pygame.image.load('requirements/Level/Coins/gold.png'), (40, 40))
        self.silver_coin_img = pygame.transform.scale(pygame.image.load('requirements/Level/Coins/silver.png'), (40, 40))
        self.key_img = pygame.transform.scale(pygame.image.load('requirements/Level/Objects/key.png'), (80, 40))
        self.victory_img = pygame.transform.scale(pygame.image.load('requirements/victory.png'), (600, 200))
        # Audio
        self.coin_sound = pygame.mixer.Sound('requirements/sound effects/coin sound.mp3')
        # Game data
        self.score = 0
        self.get_key = False

    def draw_level(self, current_level):
        self.map = levels[current_level]['content']
        self.tiles = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.gold_coins = pygame.sprite.Group()
        self.silver_coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goal = pygame.sprite.GroupSingle()
        self.key = pygame.sprite.GroupSingle()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(self.map):
            for column_index, column in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if column.isdigit():
                    obstacle = Object(x, y, column)
                    self.objects.add(obstacle)
                elif column == 'c':
                    gcoin = Coin(x, y, 'gold')
                    self.gold_coins.add(gcoin)
                    self.max_score += 70
                elif column == 's':
                    scoin = Coin(x, y, 'silver')
                    self.silver_coins.add(scoin)
                    self.max_score += 40
                elif column == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                elif column == 'e':
                    enemy_sprite = Enemy((x, y))
                    self.enemies.add(enemy_sprite)
                    self.max_score += 100
                elif column == 'g':
                    goal = Goal(x, y)
                    self.goal.add(goal)
                elif column == 'k':
                    key = Key(x, y)
                    self.key.add(key)
                elif column != ' ':
                    tile = Tile((x, y), tile_size, column)
                    self.tiles.add(tile)

    def move_x(self):
        player = self.player.sprite
        player_x_left, _ = player.rect.midleft
        player_x_right, _ = player.rect.midright
        direction_x = player.direction.x
        if player_x_left < width * 0.2 and direction_x < 0:
            self.screen_shift = 5
            player.speed = 0
        elif player_x_right > width * 0.8 and direction_x > 0:
            self.screen_shift = -5
            player.speed = 0
        else:
            self.screen_shift = 0
            player.speed = 5

    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and player.rect.left != self.current_x:
            player.on_left = False
        if player.on_right and player.rect.right != self.current_x:
            player.on_right = False

    def enemy_movement(self):
        enemies = self.enemies.sprites()
        player = self.player.sprite
        for enemy in self.enemies.sprites():
            enemy.rect.x += enemy.direction.x * enemy.speed
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right
                        enemy.on_left = True
                        enemy.on_right = False
                        enemy.facing_right = True
                        continue
                    elif enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left
                        enemy.on_right = True
                        enemy.on_left = False
                        enemy.facing_right = False
                        continue
                    enemy.rect.bottom = sprite.rect.top
            if enemy.rect.colliderect(player.rect):
                if player.direction.y > 1 and enemy.rect.top <= player.rect.bottom:
                    self.enemies.remove(enemy)
                    self.score += 100
                elif player.direction.y == 0 and not player.immunity:
                    if self.life - 1 == 0:
                        self.create_overworld(1, 0, 5)
                    else:
                        self.life -= 1
                        player.immunity = True
                        self.life_timer = pygame.time.get_ticks()

    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_floor = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if player.on_floor and player.direction.y < 0 or player.direction.y > 1:
            player.on_floor = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def coins_collision(self):
        player = self.player.sprite
        for s_coin in self.silver_coins.sprites():
            if s_coin.rect.colliderect(player.rect):
                self.coin_sound.play()
                self.silver_coin_count += 1
                self.silver_coins.remove(s_coin)
                self.score += 40
        for g_coin in self.gold_coins.sprites():
            if g_coin.rect.colliderect(player.rect):
                self.coin_sound.play()
                self.gold_coin_count += 1
                self.gold_coins.remove(g_coin)
                self.score += 70

    def key_collision(self):
        player = self.player.sprite
        key = self.key.sprite
        if not self.get_key and key.rect.colliderect(player.rect):
            self.key.remove(self.key.sprite)
            self.get_key = True

    def display_life(self):
        life_text = self.items_font.render('LIFE :', 1, 'black')
        life_img_raw = pygame.image.load(f'requirements/game data/life/life {self.life}.png')
        life_img = pygame.transform.scale(life_img_raw, (40 * self.life, 40))
        self.display_surface.blit(life_text, (20, 5))
        self.display_surface.blit(life_img, (130, 10))

    def display_coins(self):
        # Gold coin
        gold_coin_text = self.items_font.render(f'x {self.gold_coin_count}', 1, 'black')
        self.display_surface.blit(self.gold_coin_img, (400, 10))
        self.display_surface.blit(gold_coin_text, (460, 5))
        # Silver coin
        silver_coin_text = self.items_font.render(f'x {self.silver_coin_count}', 1, 'black')
        self.display_surface.blit(self.silver_coin_img, (530, 10))
        self.display_surface.blit(silver_coin_text, (610, 5))

    def display_key(self):
        if self.get_key:
            self.display_surface.blit(self.key_img, (790, 10))

    def display_score(self):
        score_text = self.items_font.render(f'SCORE : {self.score}', 1, 'black')
        self.display_surface.blit(score_text, (970, 5))

    def handle_player_immunity(self):
        player = self.player.sprite
        if player.immunity:
            current_time = pygame.time.get_ticks()
            if current_time - self.life_timer >= 600:
                player.immunity = False

    def check_player_death(self):
        if self.player.sprite.rect.top > height * 2:
            if self.life != 1:
                self.create_overworld(self.current_level, 1, self.life - 1)
            else:
                self.create_overworld(1, 0, 5)

    def check_player_win(self):
        if (self.player.sprite.rect.centerx > self.goal.sprite.rect.centerx) and (self.player.sprite.rect.centery > self.goal.sprite.rect.centery)\
                and self.get_key and (self.score >= self.max_score - 100):
            if self.current_level == 5:
                self.display_surface.blit(self.victory_img, (width//2 - self.victory_img.get_width()//2, height//2 - self.victory_img.get_height()//2 - 50))
            else:
                time.sleep(1)
                self.create_overworld(self.current_level, self.new_max_level, self.life)

    def run(self):
        # Tiles
        self.tiles.update(self.screen_shift)
        self.tiles.draw(self.display_surface)
        # Objects
        self.objects.update(self.screen_shift)
        self.objects.draw(self.display_surface)
        # Coins
        self.gold_coins.update(self.screen_shift)
        self.gold_coins.draw(self.display_surface)
        self.silver_coins.update(self.screen_shift)
        self.silver_coins.draw(self.display_surface)
        self.coins_collision()
        # Goal
        self.goal.update(self.screen_shift)
        self.goal.draw(self.display_surface)
        # Key
        self.key.update(self.screen_shift)
        self.key.draw(self.display_surface)
        self.key_collision()
        # Others
        self.move_x()
        self.enemies.update(self.screen_shift)
        self.player.update()
        self.horizontal_collision()
        self.vertical_collision()
        self.enemy_movement()
        self.enemies.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.handle_player_immunity()
        # Display
        self.display_life()
        self.display_coins()
        self.display_key()
        self.display_score()
        # Game states
        self.check_player_death()
        self.check_player_win()