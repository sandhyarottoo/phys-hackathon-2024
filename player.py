import numpy as np
import pygame

from forces import *
from particles import *
from globals import *


class Player(pygame.sprite.Sprite):
    lives = 3
    def __init__(self,angle):
        self.angle = angle
        self.initial_speed = 10
        #start the particle at the top
        self.pos = pygame.Vector2(boardWidth //2, 0)
        self.acc = pygame.Vector2(0,0)

        #these are whatever
        self.radius = 2
        self.color = (50, 50, 60)

        #initialize the image and rect 
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.respawn = False
        self.electroncapture = False

    # def start(self,keys):
    #     if keys[pygame.K_SPACE]:


    def update(self,keys,particle,dt,bucket,walls,canon):

        #this is for the start of the game, move the canon around to choose angle of initial velocity
        if keys[pygame.K_LEFT]:
            self.angle += 1
            canon.angle += 1
        if keys[pygame.K_RIGHT]:
            self.angle -= 1
            canon.angle += 1

        #shoot the player
        if keys[pygame.K_SPACE]:
            self.vel = pygame.Vector2(self.initial_speed*np.cos(self.angle),self.initial_speed*np.sin(self.angle))
        
        if pygame.sprite.collide_mask(self,particle):

            #reflect off of neutrons
            if particle.type == 'neutron':
                self.vel.x*= -0.8
                self.vel.y*= -0.8

            #get killed by electrons
            if particle.type == 'electron':
                Player.lives -= 1
                if Player.lives != 0:
                    self.respawn = True
                self.electroncapture = True


        #reflect off the walls
        for wall in walls:
            if pygame.sprite.collide_mask(self,wall):
                self.vel.x *= -0.8
                self.vel.y *= -0.8

        #get a free ball if you collide with the bucket
        if pygame.sprite.collide_mask(self,bucket):
            Player.lives += 1
            self.respawn = True

        #respawn at the top of the board again
        if self.respawn:
            self.pos = pygame.Vector2(boardWidth //2, 0)
            self.respawn = False
        
        # if Player.lives == 0:
            #condition to end game

        self.pos += self.vel*dt
        self.vel += self.acc*dt
        self.acc*=0
        self.acc += self.computeForce(particle)


        self.rect.center = self.pos


    def computeForce(self,particle):
        force = pygame.Vector2(0,0)
        r = self.pos-particle.pos
        if particle.type == 'neutron':
            force += StrongForce(r)*r.normalize()
        if particle.type == 'electron':
            force += CoulombForce(r)*r.normalize()
        return force



