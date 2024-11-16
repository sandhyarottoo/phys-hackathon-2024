import numpy as np
import pygame



def CoulombForce(r,A = 2):
    return A/r**2

def StrongForce(r,k = 1):
    return -k*np.exp(-k*r)/r -np.exp(-k*r)/r**2



class Player(pygame.sprite.Sprite):
    def __init__(self,angle,boardWidth,boardHeight,dt,vel = 10):
        self.angle = angle
        self.initial_vel = pygame.Vector2(vel*np.sin(angle),vel*np.cos(angle))
        #start the particle at the top
        self.pos = pygame.Vector2(boardWidth //2, 0)
        self.acc = pygame.Vector2(0,0)
        self.radius = 4
        self.color = 
        self.image = 
        self.rect = 

    # def start(self,keys):
    #     if keys[pygame.K_SPACE]:


    def update(self,keys,particle,dt):
        if keys[pygame.K_SPACE]:
            self.vel = self.initial_vel
        
        if pygame.sprite.collide_mask(self,particle):
            if particle.type == 'neutrino':
                particle.kill()
            if particle.type == 'neutron':
                self.vel.x*= -0.8
                self.vel.y*= 0.8
        

        self.pos += self.vel*dt
        self.vel += self.acc*dt
        self.acc*=0
        self.acc += self.computeForce(particle)


    def computeForce(self,particle):
        force = pygame.Vector2(0,0)
        r = self.pos-particle.pos
        if particle.type == 'neutron':
            force += StrongForce(r)*r.normalize()
        if particle.type == 'electron':
            force += CoulombForce(r)*r.normalize()
        return force


