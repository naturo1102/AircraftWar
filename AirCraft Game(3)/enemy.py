# -*- coding:utf-8 -*-
import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/1.png").convert_alpha()
        self.destroy_enemies = []
        self.destroy_enemies.extend([\
            pygame.image.load("image/1.1.png").convert_alpha(), \
            pygame.image.load("image/1.2.png").convert_alpha()\
            ])
        self.rect = self.image.get_rect()
        self.width,self.heitht = bg_size[0],bg_size[1]
        self.speed = 2
        self.active = True
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-5*self.heitht,0)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.heitht:
            self.rect.top += self.speed
        else:
            self.reset()
    def reset(self):
        self.active = True
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-5*self.heitht,0)


class MidEnemy(pygame.sprite.Sprite):
    HP = 8
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/2.png").convert_alpha()
        self.destroy_enemies = []
        self.destroy_enemies.extend([ \
            pygame.image.load("image/2.1.png").convert_alpha(), \
            pygame.image.load("image/2.2.png").convert_alpha(), \
            pygame.image.load("image/2.3.png").convert_alpha() \
            ])
        self.rect = self.image.get_rect()
        self.width, self.heitht = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-10 * self.heitht, -self.heitht)
        self.mask = pygame.mask.from_surface(self.image)
        self.HP = MidEnemy.HP

    def move(self):
        if self.rect.top < self.heitht:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.HP = MidEnemy.HP
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-10 * self.heitht, -self.heitht)

class BigEnemy(pygame.sprite.Sprite):
    HP = 20
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/3.png").convert_alpha()
        self.destroy_enemies = []
        self.destroy_enemies.extend([ \
            pygame.image.load("image/3.1.png").convert_alpha(), \
            pygame.image.load("image/3.2.png").convert_alpha(), \
            pygame.image.load("image/3.3.png").convert_alpha(), \
            pygame.image.load("image/3.4.png").convert_alpha() \
            ])
        self.rect = self.image.get_rect()
        self.width, self.heitht = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-15 * self.heitht, -5*self.heitht)
        self.mask = pygame.mask.from_surface(self.image)
        self.HP = BigEnemy.HP

    def move(self):
        if self.rect.top < self.heitht:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.HP = BigEnemy.HP
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-15 * self.heitht, -5*self.heitht)