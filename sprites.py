# This file was created by: Abhi Bejgam
# importing important modules
from settings import *
import pygame as pg
from pygame.sprite import Sprite
from random import choice
from random import randint
from images import *

vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir): #defining collide_with_walls so Mob2 can use it
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y 
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
        self.speed = 350
        self.speed2 = 400
        Player.hitpoints = 100
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.wall_change_timer = 0  # Add this line

        # def move(self, dx=0, dy=0):
        #     self.x += dx
        #     self.y += dy

    def get_keys(self): #Movement via wasd or arrow keys
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
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
    def collide_with_group(self, group, kill): #collision killing def
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            # if str(hits[0].__class__.__name__) == "PowerUp":# tried to add speed to PowerUp   
            if str(hits[0].__class__.__name__) == "Mob2":
                Player.hitpoints < 0
            if Player.hitpoints < 0:
                Player.kill()
            self.speed += 500 #when player kills mob, the player speed goes up
    def update(self): 
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.mobs, True)
        if Player.hitpoints < 0:
                Player.kill()
        

        # Power-up collision detection should occur within the update method
        # or within the game loop, not in the __init__ method of the PowerUp class
        power_up_hits = pg.sprite.spritecollide(self, self.game.power_ups,True)  
        # True to remove the sprite on collision
        for power_up in power_up_hits:
            self.collect_power_up(power_up)

        # Added a check to see if the timer has elapsed 5 seconds (5000 milliseconds)
        if self.wall_change_timer and pg.time.get_ticks() - self.wall_change_timer > 5000:
            # Changed the color of all walls
            for wall in self.game.walls:
                wall.change_color(silver)   

            self.wall_change_timer = 0  # Reset the timer

    # Add a new method to the Player class
    def collect_power_up(self, power_up):
        for wall in self.game.walls:
            wall.change_color(NEW_WALL_COLOR)
            
            
    # def collide_with_walls2(self, dir): #tried to add wall eating ability
    #     if dir == 'x':
    #         hits = pg.sprite.spritecollide(self, self.game.walls, True)
    #         if hits:
    #             if self.vx > 0:
    #                 self.x = hits[0].rect.left - self.rect.width
    #             if self.vx < 0:
    #                 self.x = hits[0].rect.right
    #             self.vx = 0
    #             self.rect.x = self.x
    #     if dir == 'y':
    #         hits = pg.sprite.spritecollide(self, self.game.walls, True)
    #         if hits:
    #             if self.vy > 0:
    #                 self.y = hits[0].rect.top - self.rect.height
    #             if self.vy < 0:
    #                 self.y = hits[0].rect.bottom
    #             self.vy = 0
    #             self.rect.y = self.y 
        
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
        self.image.fill(new_color)  # Filling the wall's surface with the new color


class PowerUp(pg.sprite.Sprite): #added PowerUp class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(green)  
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Mob2(pg.sprite.Sprite): #Mr. Cozort made class edited by Abhi Bejgam
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        Mob2.hitpoints = 100
        # self.image = game.mob_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(ORANGE)
        self.image = self.game.mob2_img
        self.image.set_colorkey(yellow)
        self.rect = self.image.get_rect()
        # self.hit_rect = MOB_HIT_RECT.copy()
        # self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILE_SIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 500
        # added
        self.speed = 200
        self.chasing = False
        # self.health = MOB_HEALTH
        self.hitpoints = 5
    def sensor(self):
        if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
    def update(self):
        if self.hitpoints < 1:
            self.kill()
        self.sensor()
        if self.chasing:
            self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
            # self.image = pg.transform.rotate(self.image, 45)
            # self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * 0.
            self.vel += self.acc * self.game.dt
            # equation of motion needed here (F=ma)
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            # self.hit_rect.centerx = self.pos.x
            self.rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            # self.hit_rect.centery = self.pos.y
            self.rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            # self.rect.center = self.hit_rect.center
            if self.hitpoints <= 0:
                self.kill() 
    
class Mob3(pg.sprite.Sprite): #Mr. Cozort made class edited by Abhi Bejgam
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        Mob2.hitpoints = 1800
        # self.image = game.mob_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(ORANGE)
        self.image = self.game.mob2_img
        self.image.set_colorkey(yellow)
        self.rect = self.image.get_rect()
        # self.hit_rect = MOB_HIT_RECT.copy()
        # self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILE_SIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 2000
        # added
        self.speed = 20
        self.chasing = False
        # self.health = MOB_HEALTH
        self.hitpoints = 6900
    def sensor(self):
        if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
    def update(self):
        # if self.hitpoints < 1:
        #     self.kill()
        self.sensor()
        if self.chasing:
            self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
            # self.image = pg.transform.rotate(self.image, 45)
            # self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * 1.
            self.vel += self.acc * self.game.dt
            # equation of motion needed here (F=ma)
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            # self.hit_rect.centerx = self.pos.x
            self.rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x') #uncomment if you want wall collision
            # self.hit_rect.centery = self.pos.y
            self.rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y') #uncomment if you want wall collision
            # self.rect.center = self.hit_rect.center
            # if self.hitpoints <= 0: #uncomment if you want this mob to be killable
            #     self.kill()

class Wall2(Sprite):
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
