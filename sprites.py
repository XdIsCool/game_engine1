# This file was created by: Abhi Bejgam
# importing important modules
from settings import *
import pygame as pg
from pygame.sprite import Sprite
from random import choice

vec = pg.math.Vector2


# creating a player class
# Capital "player" is advised rather than lowercase
# creating a player class
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.wall_change_timer = 0  # Add this line

        # def move(self, dx=0, dy=0):
        #     self.x += dx
        #     self.y += dy

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071  # this is to cancel out moving faster diagonally

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

        # Power-up collision detection should occur within the update method
        # or within the game loop, not in the __init__ method of the PowerUp class.
        power_up_hits = pg.sprite.spritecollide(self, self.game.power_ups,
                                                True)  # True to remove the sprite on collision
        for power_up in power_up_hits:
            self.collect_power_up(power_up)

        # Add a check to see if the timer has elapsed 5 seconds (5000 milliseconds)
        if self.wall_change_timer and pg.time.get_ticks() - self.wall_change_timer > 5000:
            # Change the color of all walls
            for wall in self.game.walls:
                wall.change_color(silver)
            self.wall_change_timer = 0  # Reset the timer

    # Add a new method to the Player class
    def collect_power_up(self, power_up):
        print("Power-up collected!")
        for wall in self.game.walls:
            wall.change_color(NEW_WALL_COLOR)
        # Change the color of all walls
            self.wall_change_timer = pg.time.get_ticks()  # Start the timer when a power-up is collected

# creating a wall class
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(silver)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

    def change_color(self, new_color):
        self.image.fill(new_color)  # Fill the wall's surface with the new color


class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(green)  # Choose an appropriate color for the power-up
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

# class Wall_Eater(Sprite):
#     pass

# class Health(Sprite):
#     pass