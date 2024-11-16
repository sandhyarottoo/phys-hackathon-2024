from player import *
from forces import *
from particles import *
from globals import *



class Bucket(pygame.sprite.Sprite):

    def __init__(self):
        self.pos = pygame.Vector2(boardHeight,boardWidth//2)
        self.rect = (self.pos.x,self.pos.y,10,4)
        self.betadecay = False
        self.vel = pygame.Vector2(10,0)

    def update(self,player):

        if pygame.sprite.collide_mask(self,player):
            self.betadecay = True

        if self.pos >= boardWidth or self.pos <= 0:
            self.vel *= -1
        self.pos += self.vel*dt
        self.rect.center = self.pos
        