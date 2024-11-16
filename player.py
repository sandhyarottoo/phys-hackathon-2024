import numpy as np
import pygame

from forces import *
from particles import *


class Player(pygame.sprite.Sprite):
    lives = 3
    def __init__(self,angle,boardWidth,boardHeight,dt,vel = 10):
        self.angle = angle
        self.initial_speed = vel
        #start the particle at the top
        self.pos = pygame.Vector2(boardWidth //2, 0)
        self.acc = pygame.Vector2(0,0)
        self.radius = 4
        self.color = (50, 50, 60)
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    # def start(self,keys):
    #     if keys[pygame.K_SPACE]:


    def update(self,keys,particle,dt,bucket,walls,canon):
        if keys[pygame.K_LEFT]:
            self.angle += 1
            canon.angle += 1
        if keys[pygame.K_RIGHT]:
            self.angle -= 1
            canon.angle += 1
        if keys[pygame.K_SPACE]:
            self.vel = pygame.Vector2(self.initial_speed*np.sin(self.angle),self.initial_speed*np.cos(self.angle))
        
        if pygame.sprite.collide_mask(self,particle):
            if particle.type == 'neutrino':
                particle.kill()
            if particle.type == 'neutron':
                self.vel.x*= -0.8
                self.vel.y*= -0.8
            if particle.type == 'electron':
                Player.lives -= 1
                particle.electroncapture == True
                self.kill()
        for wall in walls:
            if pygame.sprite.collide_mask(self,wall):
                self.vel.x *= -0.8
                self.vel.y *= -0.8

        if pygame.sprite.collide_mask(self,bucket):
            bucket.freeball == True
            Player.lives += 1
            self.kill()
        

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



