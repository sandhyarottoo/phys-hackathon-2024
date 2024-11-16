
import numpy as np
import pygame
from forces import *
from player import *

class Particle(pygame.sprite.Sprite):
    def __init__(self,type,BoardWidth,BoardHeight,pos,random = True):
        self.type = type
        if random:
            #if the particle did not come from a reaction, place it at a random spot
            self.pos = pygame.Vector2(np.random.rand()*BoardWidth,np.random.rand()*BoardHeight)
        else:
            #if the particle did come from a reaction, it has to start at a certain spot
            self.pos = pos
        self.vel = pygame.Vector2(2,2)
        self.acc = pygame.Vector2(0,0)
        if self.type == 'neutron':
            self.betadecay == False
        if self.type == 'neutrino':
            self.isAbsorbed == False

    def update(self,player,particle,dt,neutrons,neutrinos,BoardWidth,BoardHeight):
        #neutrons and neutrinos are groups of particles

        if pygame.sprite.collide_mask(self,player):
            if self.type == 'neutrino':
                self.isAbsorbed == True
            if self.type == 'neutron':
                self.vel.x *= -0.8
                self.vel.y *= -0.8
        if self.type == 'neutron':
            self.acc += self.computeForce(particle)
            if self.betadecay:
                neutrino = Particle('neutrino',BoardWidth,BoardHeight,self.pos,random =False)
                neutrinos.add(neutrino)

                #also create an electron

                self.kill()
        if self.type == 'neutrino':
            if self.isAbsorbed:
                self.kill()

        self.pos += self.vel * dt
        self.vel += self.acc * dt



    def computeForce(self,particle):
        force = pygame.Vector2(0,0)
        r = self.pos-particle.pos
        if (isinstance(particle,Particle) and particle.type == 'neutron') or isinstance(particle,Player):
                force += StrongForce(r)*r.normalize()

        return force


                
        



        