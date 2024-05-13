# This file was created by: Abhi Bejgam
# my first source control edit
# importing necessary modules

# BETA GOALS:
#   *Animate the player sprite (DONE)
#   *Add levels with varying maps and mobs
#   *Add shield/deflection feature and make player's points increase/decrease based off of that

import pygame as pg
import sys
from settings import *
from sprites import *
# from random import randint
from os import path
from time import sleep
from images import *
from os import path

def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 32
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, green, fill_rect)
    pg.draw.rect(surf, white, outline_rect, 2) 

class HealthBar:
    def __init__(self, x, y, w, h, max_hp,):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_hp = max_hp
        self.hp = max_hp  # Initialize hp with max_hp

    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pg.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.w, self.h))  # Red background
        pg.draw.rect(surface, (0, 255, 0), (self.x, self.y, int(self.w * ratio), self.h))  # Green foreground

    def decrease(self, amount):
        self.hp = max(self.hp - amount, 0)
        print(f"Time decreased: {self.hp}")  # Debug print
        if self.hp <= 0:
            pg.quit() #game will close if the healthbar reaches 0
    
# creating the game class
class Game:
    def __init__(self):
        pg.init()
        self.power_ups = pg.sprite.Group()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.points = 0
        self.player_health_bar = None
        self.last_health_decrease = pg.time.get_ticks()  # Initializing the timer
    
    def draw_points(self):
        # Create a font object
        font = pg.font.Font(None, 36)  # None means default font, 36 is the font size
        # Render the point counter as text
        point_text = font.render(f"Points: {self.points}", True, pg.Color('black'))
        # Blit the text onto the screen at the specified position
        self.screen.blit(point_text, (10, 10))  # Top-left corner (10, 10)    
    
    # loading the game's data 
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images') 
        game_folder = path.dirname(__file__)

        self.mob2_img = pg.image.load(path.join(self.img_folder, 'abhiramface2.png')).convert_alpha()

        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
                print(self.map_data)
                #print(enumerate(self.map_data))

    def new(self):
        # initializing all variables and setup groups, and instantiating classes
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        # self.player = Player(self, 10, 10)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                # print(col)
                # print(tiles)
                if tile == '1': #1 =  tile
                    Wall(self, col, row)
                if tile == 'P': #P = player tile
                    self.player = Player(self, col, row)
                if tile == 'U':  #U = size power up
                    PowerUp(self, col, row)
                if tile == 'B': #B = mob tile
                    Mob2(self, col, row)
                if tile == 'H': #
                    Mob3(self, col, row)
                    
                    # if self.collide_with_group(self.game.mobs, True):
                    #     if tile == 'H':
                    #         Mob2(self, col, row)
        if hasattr(self, 'player'):
            self.player_health_bar = HealthBar(10, 10, 100, 40, self.player.hitpoints)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def reset_points(self):
        self.points = 0
    
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        if self.player.hitpoints < 1:
            self.playing = False
        self.all_sprites.update()
        # Decrease the health bar every 2 seconds
        now = pg.time.get_ticks()
        if now - self.last_health_decrease > 1500:  # 1500 milliseconds = 1.5 seconds
            if self.player_health_bar:
                self.player_health_bar.decrease(10)  # Decrease health by 10 or any desired amount
            self.last_health_decrease = now
            self.points += 1
        if self.player.hitpoints <= 0:
            self.reset_points() #when the player dies, the points and level reset
        
        
     
    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, lightgrey, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, lightgrey, (0, y), (WIDTH, y))
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)        
        # Draw the health bar here
        if self.player_health_bar:
            self.player_health_bar.draw(self.screen)
            self.draw_points()
        pg.display.update()
        #draw_health_bar(self.screen, self.player.rect.x, self.player.rect.y-8, self.player.hitpoints)

    def draw_game_over(self):
        # This function draws the "Game Over" text
        font = pg.font.Font(None, 74)
        text = font.render("Game Over", 1, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect) 


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text.surface.get_rect()
        text_rect.topleft = (x*TILE_SIZE, y*TILE_SIZE)
        surface.blit(text_surface, text_rect)
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass



g = Game()
# g.show_start_screen()
while True:
    g.new()
    g.run()
    
    
 
