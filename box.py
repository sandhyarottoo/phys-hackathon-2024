import numpy as n
import pygame
from particles import *
from GLOBVAR import *
from electron import Electron
import torch
from pegglestuff import *

electron = Electron()
electron.load_state_dict(torch.load('model.pth', weights_only=True, map_location=torch.device('cpu')))


class Box():
    def __init__(self, x, y, w, h, index):
        self.rect = pygame.Rect(x, y, w, h)
        self.index = index
        self.particles = []
        
    def initializeParticles(self, n_particles, distribtution='random'):
        if n_particles <= 0:
            return
        
        xs = []
        ys =[]
        for i in range(n_particles):
            if distribtution == 'random':
                while True:
                    x = n.random.randint(self.rect.left, self.rect.right)
                    if x not in xs:
                        break
                while True:
                    y = n.random.randint(self.rect.top, self.rect.bottom)
                    if x not in ys:
                        break
                type = n.random.choice(['neutron', 'neutrino'])
                xs.append(x)
                ys.append(y)
                
                velx = 1*n.random.randn(1)
                vely = 1*n.random.randn(1)
                
            else:
                x, y = None # distribution() to be implemented
            self.particles.append(Particle(type, pygame.Vector2(x, y), pygame.Vector2(velx,vely)))
    
        
    def isEdgeBox(self):
        return self.index % NBOX_X == 0 or self.index % NBOX_X == NBOX_X - 1 or self.index < NBOX_X or self.index >= NBOX_X * (NBOX_Y - 1)
    
    def isBottomBox(self):
        return self.index >= NBOX_X * (NBOX_Y - 1)
        
    def updateBox(self, screen, keys, dt,bucket):
        if not self.contains_particles():
            return
        
        neighbors = self.getAdjBoxes()
        for particle in self.particles:
            self.wallCollide(particle)
            for neighbor in neighbors:
                for other_particle in neighbor.particles:
                    if particle != other_particle:
                        particle.update(screen, other_particle, keys, dt,electron)
                        if bucket.betadecay and particle.is_player:
                            self.betaDecay()
                            bucket.betadecay = False
                            Player.respawn = True
                            Player.start = True
                        if particle.is_player and Player.respawn:
                            self.particles.remove(particle)
                            if Player.lives > 0:
                                boxes[0].addParticle(particle)
                                Player.respawn = False
                                Player.start = True

                        

                        if (particle.type == 'electron' or particle.type == 'proton') and particle.electroncapture:
                            x, y, velx, vely = particle.pos.x, particle.pos.y, particle.vel.x, particle.vel.y
                            x1, y1, velx1, vely1 = other_particle.pos.x, other_particle.pos.y, other_particle.vel.x, other_particle.vel.y
                            self.removeParticle(particle)
                            self.removeParticle(other_particle)
                            self.addParticle(Particle('neutron', pygame.Vector2(x, y), pygame.Vector2(velx, vely)))
                            self.addParticle(Particle('neutrino', pygame.Vector2(x1, y1), pygame.Vector2(velx1, vely1)))
                        if particle.type == 'neutrino' and particle.isAbsorbed:
                            try:
                                self.removeParticle(particle)
                            except:
                                try: 
                                    for neighbor in neighbors:
                                        neighbor.removeParticle(particle)
                                except:
                                    pass
                                    # print('Neutrino collided, but it is no longer in the box')

                        
            self.checkParticles()
        
    def getAdjBoxes(self):
        current = self.index
        right = self.index + 1
        left = self.index - 1
        up = self.index - NBOX_X
        down = self.index + NBOX_X
        up_right = up + 1
        up_left = up - 1
        down_right = down + 1
        down_left = down - 1
        
        if self.index % NBOX_X == 0:
            left = None
            up_left = None
            down_left = None
            
        if self.index % NBOX_X == NBOX_X - 1:
            right = None
            up_right = None
            down_right = None
            
        if self.index < NBOX_X:
            up = None
            up_right = None
            up_left = None
            
        if self.index >= NBOX_X * (NBOX_Y - 1):
            down = None
            down_right = None
            down_left = None
            
        adj_boxes = [boxes[i] for i in (current, right, left, up, down, up_right, up_left, down_right, down_left) if i is not None]
            
        return adj_boxes
    
    def isValidIndex(self, index):
        if not (0 <= index < len(boxes)):
            return False
        adj_indices = [self.index + 1, self.index - 1, self.index + NBOX_X, self.index - NBOX_X,
                       self.index + NBOX_X + 1, self.index + NBOX_X - 1, self.index - NBOX_X + 1, self.index - NBOX_X - 1]
        return index in adj_indices    

    def wallCollide(self, particle):
        if particle.rect.left < 0:
            particle.vel.x = particle.vel.x * -1
            particle.rect.left = 0
            return True

        if particle.rect.right > SCREEN_WIDTH:
            particle.vel.x = particle.vel.x * -1
            particle.rect.right = SCREEN_WIDTH
            return True
        
        if particle.rect.top < 0:
            particle.vel.y = particle.vel.y * -1
            particle.rect.top = 0 
            return True
        
        if particle.rect.bottom > SCREEN_HEIGHT:
            if self.isBottomBox() and particle.is_player:
                print("Player hit bottom. updating lives from ", Player.lives, " to ", end='')
                Player.lives -= 1
                print(Player.lives)
                Player.respawn = True
                particle.pos = pygame.Vector2(SCREEN_WIDTH // 2, 12)
                particle.vel = pygame.Vector2(0, 0)
                particle.angle = 0
                particle.show = True
                # boxes[0].addParticle(particle)
                # self.particles.remove(particle)
            if not particle.is_player:
                particle.vel.y = particle.vel.y * -1
                particle.rect.bottom = SCREEN_HEIGHT - 1
            return True
        
        return False
    
    def checkParticles(self):
        if not self.contains_particles():
            return
        
        gone_particles = []
        
        for particle in self.particles:
            box_x, box_y, box_w, box_h = self.rect
            
            collides = False
            if self.isEdgeBox():
                collides = self.wallCollide(particle)
                    
            if not collides:
                if particle.rect.right > box_x + box_w and self.isValidIndex(self.index + 1):
                    boxes[self.index + 1].addParticle(particle)
                if particle.rect.left < box_x and self.isValidIndex(self.index - 1):
                    boxes[self.index - 1].addParticle(particle)
                if particle.rect.bottom > box_y + box_h and self.isValidIndex(self.index + NBOX_X):
                    boxes[self.index + NBOX_X].addParticle(particle)
                if particle.rect.top < box_y and self.isValidIndex(self.index - NBOX_X):
                    boxes[self.index - NBOX_X].addParticle(particle)
                if particle.rect.right > box_x + box_w and particle.rect.bottom > box_y + box_h and self.isValidIndex(self.index + NBOX_X + 1):
                    boxes[self.index + NBOX_X + 1].addParticle(particle)
                if particle.rect.right > box_x + box_w and particle.rect.top < box_y and self.isValidIndex(self.index - NBOX_X + 1):
                    boxes[self.index - NBOX_X + 1].addParticle(particle)
                if particle.rect.left < box_x and particle.rect.bottom > box_y + box_h and self.isValidIndex(self.index + NBOX_X - 1):
                    boxes[self.index + NBOX_X - 1].addParticle(particle)
                if particle.rect.left < box_x and particle.rect.top < box_y and self.isValidIndex(self.index - NBOX_X - 1):
                    boxes[self.index - NBOX_X - 1].addParticle(particle)
                if (particle.rect.left > box_x + box_w or particle.rect.right < box_x or particle.rect.bottom < box_y or particle.rect.top > box_y + box_h):
                    gone_particles.append(particle)
                    
        for particle in gone_particles:
            self.removeParticle(particle)
        
    def addParticle(self, particle):
        if particle not in self.particles:
            self.particles.append(particle)
            particle.updated = True
        
    def removeParticle(self, particle):
        self.particles.remove(particle)
        particle.kill()
        
    def betaDecay(self)->bool:
        for particle in self.particles:
            if particle.type == 'neutron':
                x, y, velx, vely = particle.pos.x, particle.pos.y, particle.vel.x, particle.vel.y
                self.removeParticle(particle)
                boxes[self.index].addParticle(Particle('neutrino', pygame.Vector2(x, y), pygame.Vector2(velx, vely))) # to change... maybe
                boxes[self.index].addParticle(Particle('electron', pygame.Vector2(x, y), pygame.Vector2(-1*velx, -1*vely))) # to change... maybe
                Player.respawn = False
                return True
        return False
            
    def contains_particles(self):
        return len(self.particles) > 0
        
    def draw(self, screen, color=(255, 255, 255), signal_content=False):
        if signal_content and self.contains_particles():
                color = (75, 50, 50)
        pygame.draw.rect(screen, color, self.rect)
        
# getting all boxes
boxes = []
for j in range(NBOX_Y):
    n_particles = 1
    for i in range(NBOX_X):
        box = Box(i*BOX_WIDTH, j*BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT, i+j*NBOX_X)
        box.initializeParticles(n_particles)
        boxes.append(box)