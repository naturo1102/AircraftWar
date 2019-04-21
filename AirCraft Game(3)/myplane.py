# -*- coding:utf-8 -*-
import pygame

class MyPlane(pygame.sprite.Sprite):
    Energy = 0
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("image/plane.png").convert_alpha()
        self.image2 = pygame.image.load("image/plane1.png").convert_alpha()
        self.destory_images = []
        self.destory_images.extend([\
            pygame.image.load("image/0.1.png").convert_alpha(), \
            pygame.image.load("image/0.2.png").convert_alpha(), \
            pygame.image.load("image/0.3.png").convert_alpha() \
            ])
        self.rect = self.image1.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left,self.rect.top = (self.width-self.rect.width)//2,self.height-self.rect.height-70
        self.speed = 10
        self.active = True
        #将飞机的非透明做标志
        self.mask = pygame.mask.from_surface(self.image1)
        self.invincible = False
        self.Energy = MyPlane.Energy

    def Up(self):
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.rect.top = 0
    def Down(self):
            if self.rect.bottom < self.height-70:
                self.rect.top += self.speed
            else:
                self.rect.bottom = self.height-70
    def Left(self):
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.rect.left = 0
    def Right(self):
            if self.rect.right < self.width:
                self.rect.right += self.speed
            else:
                self.rect.right = self.width

    def reset(self):
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, self.height - self.rect.height - 70
        self.active = True
        self.invincible = True
        self.Energy = MyPlane.Energy
