
import numpy as np
import pygame
from forces import *
from player import *
from globals import *

dt = 0.001

class Particle(pygame.sprite.Sprite):
    neutrinos = 0
    neutrons = 0
    def __init__(self,type,pos=None,vel = None,random = True):
        self.type = type
        if random:
            #if the particle did not come from a reaction, place it at a random spot
            self.pos = pygame.Vector2(np.random.rand()*boardWidth,np.random.rand()*boardHeight)
            self.vel = pygame.Vector2(2,2)
        else:
            #if the particle did come from a reaction, it has to start at a certain spot
            self.pos = pos
            self.vel = vel


        #initial velocity, dummy variable for now
        
        self.acc = pygame.Vector2(0,0)

        #should this be a sub class?
        if self.type == 'neutron':
            self.betadecay = False
            Particle.neutrons += 1
        if self.type == 'neutrino':
            self.isAbsorbed = False
            Particle.neutrinos += 1
        if self.type == 'electron':
            self.electroncapture = False

        #these are whatever
        self.radius = 2
        self.color = (50, 50, 60)

        #initialize the image and rect 
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

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

        if self.type == 'electron':
            if pygame.sprite.collide_mask(self,particle) and isinstance(particle,Player):
                self.electroncapture = True
            self.acc += self.computeForce(particle)

        self.pos += self.vel * dt
        self.vel += self.acc * dt

        self.rect.center = self.pos

        # if Particle.neutrinos == 0:
            # end condition


    def computeForce(self,particle):
        force = pygame.Vector2(0,0)
        r = self.pos-particle.pos
        if self.type == 'neutron' and (isinstance(particle,Particle) and particle.type == 'neutron') or isinstance(particle,Player):
                force += StrongForce(r)*r.normalize()

        if self.type == 'electron' and isinstance(particle,Player):
            force += CoulombForce(r)*r.normalize()

        return force


                
        



        