from player import *
from forces import *
from particles import *
from GLOBVAR import *



class Bucket(pygame.sprite.Sprite):

    def __init__(self):
        self.pos = pygame.Vector2(SCREEN_HEIGHT,SCREEN_WIDTH//2)
        self.rect = (self.pos.x,self.pos.y,10,4)
        self.betadecay = False
        self.vel = pygame.Vector2(10,0)

    def update(self,player):

        if pygame.sprite.collide_mask(self,player):
            self.betadecay = True

        if self.pos >= SCREEN_WIDTH or self.pos <= 0:
            self.vel *= -1
        self.pos += self.vel*dt
        self.rect.center = self.pos
        


class Canon(pygame.sprite.Sprite):

    def __init__(self):
        self.pos = pygame.Vector2(SCREEN_WIDTH // 2, 0)
        self.image = canon_png
        self.rect = self.image.get_rect().center

    def update(self,player):
        initial_rect = self.rect
        rotated_canon = pygame.transform.rotate(self.image, player.angle)
        rotated_canon.get_rect().center = initial_rect
        self.image = rotated_canon


