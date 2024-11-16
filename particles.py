
import numpy as np
import pygame
from forces import *
from globals import *

class Particle(pygame.sprite.Sprite):
    neutrinos = 0
    neutrons = 0
    def __init__(self,type,pos,vel = None):
        self.type = type
        self.pos = pos
        if vel == None:
            self.vel = pygame.Vector2(np.random.rand()*10,np.random.rand()*10)
        else:
            self.vel = vel

        
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
        r_norm = np.sqrt(r.x**2 + r.y**2)
        if (self.type == 'neutron' or self.type == 'proton') and (particle.type == 'proton' or particle.type == 'neutron'):
                force += StrongForce(r_norm)*r.normalize()

        # if (self.type == 'electron' or self.type == 'proton') and (particle.type == 'electron' or particle.type == 'proton'):
        #     force += CoulombForce(r)*r.normalize()
        return force


                
    
class Player(Particle):
    lives = 3
    
    def __init__(self,keys,bucket,canon):
        super().__init__(type='proton', pos=pygame.Vector2(boardWidth // 2, 0), random=False)
        self.angle = 0
        self.initial_speed = 10
        self.acc = pygame.Vector2(0, 0)

        # these are specific to Player
        self.radius = 2
        self.color = (50, 50, 60)
        
        # initialize the image and rect
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.respawn = False
        self.electroncapture = False
        self.keys = keys
        self.bucket = bucket
        self.canon = canon

    def update(self, particle):
        keys = self.keys
        bucket = self.bucket
        canon = self.canon
        # control cannon angle
        if keys[pygame.K_LEFT]:
            self.angle += 1
            canon.angle += 1
        if keys[pygame.K_RIGHT]:
            self.angle -= 1
            canon.angle -= 1

        # shoot the player
        if keys[pygame.K_SPACE]:
            self.vel = pygame.Vector2(self.initial_speed * np.cos(self.angle), 
                                      self.initial_speed * np.sin(self.angle))

        # detect collisions and apply responses
        if pygame.sprite.collide_mask(self, particle):
            # reflect off of neutrons
            if particle.type == 'neutron':
                self.vel.x *= -0.8
                self.vel.y *= -0.8

            # get "killed" by electrons
            if particle.type == 'electron':
                Player.lives -= 1
                if Player.lives != 0:
                    self.respawn = True
                self.electroncapture = True

        # gain a life if colliding with the bucket
        if pygame.sprite.collide_mask(self, bucket):
            Player.lives += 1
            self.respawn = True

        # respawn if needed
        if self.respawn:
            self.pos = pygame.Vector2(boardWidth // 2, 0)

        self.pos += self.vel * dt
        self.vel += self.acc * dt
        self.acc = pygame.Vector2(0, 0)  # reset acceleration
        self.acc += self.computeForce(particle)
        self.rect.center = self.pos





class HiggsDisturbance(Particle):

    def __init__(self,pos):
        super.__init__(type = 'Higgs',pos = pos,vel = pygame.Vector2(0,0))

        
        
    