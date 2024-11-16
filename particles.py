
import numpy as np
import pygame
from forces import *
from player import *

dt = 0.001

class Particle(pygame.sprite.Sprite):
    neutrinos = 0
    neutrons = 0
    def __init__(self,type,BoardWidth,BoardHeight,pos=None,vel = None,random = True):
        self.type = type
        if random:
            #if the particle did not come from a reaction, place it at a random spot
            self.pos = pygame.Vector2(np.random.rand()*BoardWidth,np.random.rand()*BoardHeight)
            self.vel = pygame.Vector2(2,2)
        else:
            #if the particle did come from a reaction, it has to start at a certain spot
            self.pos = pos
            self.vel = vel


        #initial velocity, dummy variable for now
        
        self.acc = pygame.Vector2(0,0)

        #should this be a sub class?
        if self.type == 'neutron':
            self.betadecay == False
            Particle.neutrons += 1
        if self.type == 'neutrino':
            self.isAbsorbed == False
            Particle.neutrinos += 1

    def update(self,particle):
        #neutrons and neutrinos are groups of particles

        #update neutrino, they don't interact so we just need to check for absorption
        if self.type == 'neutrino':
            if pygame.sprite.collide_mask(self,particle) and isinstance(particle,Player):
                self.isAbsorbed == True
                Particle.neutrinos -= 1
                self.kill()

        #update neutron, if it collides its velocity changes
        if self.type == 'neutron':
            if pygame.sprite.collide_mask(self,particle):
                self.vel.x *= -0.8
                self.vel.y *= -0.8

            #compute strong force  
            self.acc += self.computeForce(particle)


        self.pos += self.vel * dt
        self.vel += self.acc * dt



        # if Particle.neutrinos == 0:
            # end condition


    def computeForce(self,particle):
        force = pygame.Vector2(0,0)
        r = self.pos-particle.pos
        if (isinstance(particle,Particle) and particle.type == 'neutron') or isinstance(particle,Player):
                force += StrongForce(r)*r.normalize()

        return force


                
        



        