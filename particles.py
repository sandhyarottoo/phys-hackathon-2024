
import numpy as np
import pygame
from forces import *
from GLOBVAR import *
from electron import Electron
import torch

class Particle(pygame.sprite.Sprite):
    neutrinos = 0
    neutrons = 0
class Particle(pygame.sprite.Sprite):
    neutrinos = 0
    neutrons = 0
    
    def __init__(self, type, pos, vel=None):
        pygame.sprite.Sprite.__init__(self)
        
        self.type = type
        self.pos = pos
        self.is_player = False
        self.betadecay = False
        
        # Load images for each particle type
        neutrino_image = pygame.image.load("Images/Neutrino.png")
        electron_image = pygame.image.load("Images/New_Electron.png")
        proton_image = pygame.image.load("Images/Proton.png")
        neutron_image = pygame.image.load("Images/Neutron.png")

        # Scale images based on new width and height
        neutrino_image = pygame.transform.scale(neutrino_image, (10, 10))
        electron_image = pygame.transform.scale(electron_image, (10, 10))
        proton_image = pygame.transform.scale(proton_image, (15, 15))
        neutron_image = pygame.transform.scale(neutron_image, (15, 15))
        
        # Set default velocity if not provided
        if vel is None:
            self.vel = pygame.Vector2(np.random.rand() * 10, np.random.rand() * 10)
        else:
            self.vel = vel

        self.acc = pygame.Vector2(0, 0)
        self.radius = 12  # Default radius, but will be replaced by image size
        
        # Set image and position based on particle type
        if self.type == 'neutron':
            self.betadecay = False
            Particle.neutrons += 1
            self.color = (150, 150, 150)
            self.is_player = False
            self.image = neutron_image  # Assign image for neutron
        elif self.type == 'neutrino':
            self.isAbsorbed = False
            Particle.neutrinos += 1
            self.color = (200, 50, 50)
            self.is_player = False
            self.image = neutrino_image  # Assign image for neutrino
        elif self.type == 'electron':
            self.electroncapture = False
            self.color = (100, 100, 200)
            self.is_player = False
            self.image = electron_image  # Assign image for electron
        elif self.type == 'proton':
            self.radius = 10  # Specific size for proton
            self.color = (10, 10, 250)
            self.image = proton_image  # Assign image for proton
        
        # Set the rect attribute based on the image size and position
        self.rect = self.image.get_rect()
        self.rect.center = self.pos  # Set the center to the particle's position


        self.mask = pygame.mask.from_surface(self.image)

    def update(self, screen, particle, keys, dt, electron):
        if self.is_player:
            bucket = self.bucket
            canon = self.canon
            # control cannon angle
            if keys[pygame.K_LEFT] and canon.angle < canon.max_angle:
                self.angle += 0.1
                canon.angle += 0.1
            if keys[pygame.K_RIGHT] and canon.angle > canon.min_angle:
                self.angle -= 0.1
                canon.angle -= 0.1

            # shoot the player
            # print(Player.lives)
            if Player.start:
                # if Player.lives < 3:
                    # print("Starting")
                self.acc = pygame.Vector2(0,0)
                if  keys[pygame.K_SPACE]:
                    # print(self.angle)
                    if self.angle >= 0:
                        self.vel = pygame.Vector2(-1*self.initial_speed * np.sin(np.deg2rad(self.angle)), 
                                                1*self.initial_speed * np.cos(np.deg2rad(self.angle)))
                    else:
                        # print('rhugwfds')
                        self.vel = pygame.Vector2(1*self.initial_speed * abs(np.sin(np.deg2rad(self.angle))), 
                                                1*self.initial_speed * np.cos(np.deg2rad(self.angle)))
                    Player.start = False

            # detect collisions and apply responses
            if self.show:
                if pygame.sprite.collide_mask(self, particle) and not Player.start:
                    # reflect off of neutrons
                    if particle.type == 'neutron' or particle.type == 'Higgs':
                        # print('wooo collision')
                        # self.applycollision(particle)
                        self.vel.x *= -1.01
                        self.vel.y *= -1.01

                    # get "killed" by electrons
                    if particle.type == 'electron':
                        Player.lives -= 1
                        if Player.lives != 0:
                            Player.respawn = True
                            Player.start = True
                        self.electroncapture = True

                # gain a life if colliding with the bucket
                if pygame.sprite.collide_mask(self, bucket):
                    Player.lives += 1
                    Player.respawn = True
                    # Player.start = True
                    self.vel = pygame.Vector2(0,0)
                    
                    self.betadecay = True

                # # respawn if needed
                # if Player.respawn:
                #     self.pos = pygame.Vector2(SCREEN_WIDTH // 2, 12)
                #     Player.respawn = False

                # self.pos += self.vel * dt
                # self.vel += self.acc * dt
                # self.acc = pygame.Vector2(0, 0)  # reset acceleration
                # if not Player.start:
                #     self.acc += self.computeForce(particle)
                # self.rect.center = self.pos
                
                screen.blit(self.image,self.rect)

        
        #neutrons and neutrinos are groups of particles

        #update neutrino, they don't interact so we just need to check for absorption
        if self.type == 'neutrino':
            if pygame.sprite.collide_mask(self,particle) and particle.is_player and not Player.start:
                # print('Player collided with neutrino')
                self.isAbsorbed = True
                self.vel.x = 0
                self.vel.y = 0
                Particle.neutrinos -= 1

        if self.type == 'neutron':
            if pygame.sprite.collide_mask(self, particle) and particle.type != 'neutrino':
                self.vel.x *= -1.01
                self.vel.y *= -1.01

            # compute strong force  
            self.acc += self.computeForce(particle)

        if self.type == 'electron':
            if particle.is_player:
                mouse_pos = particle.rect.center
                mouse_vel = particle.vel
                electron_pos = self.pos
                electron_vel = self.vel
                pos_diff = mouse_pos - electron_pos
                t = torch.tensor([pos_diff.x, pos_diff.y, electron_vel.x, electron_vel.y, mouse_pos.x, mouse_pos.y, dt])
                with torch.no_grad():
                    a = 4 * electron(t)
                    self.acc = pygame.Vector2(a[0].item(), a[1].item())
            if pygame.sprite.collide_mask(self, particle) and particle.type == 'proton':
                self.electroncapture = True

        speed = np.sqrt(self.vel.x ** 2 + self.vel.y ** 2)
        while speed > 10:
            self.vel.x *= 0.5
            self.vel.y *= 0.5
            speed = np.sqrt(self.vel.x ** 2 + self.vel.y ** 2)
        self.pos += self.vel * dt
        self.vel += self.acc * dt

        self.rect.center = self.pos
        screen.blit(self.image, self.rect)  # Ensure the image is drawn



    def computeForce(self,particle):
        force = pygame.Vector2(0,0)
        r = self.pos-particle.pos
        r_norm = np.sqrt(r.x**2 + r.y**2)
        if (self.type == 'neutron' or self.type == 'proton') and (particle.type == 'proton' or particle.type == 'neutron'):
                force += StrongForce(r_norm)*r.normalize()

        # if (self.type == 'electron' or self.type == 'proton') and (particle.type == 'electron' or particle.type == 'proton'):
        #     force += CoulombForce(r)*r.normalize()
        return force
        
    def applycollision(self,particle):
        step = 10
        if self.pos.x > particle.pos.x and self.vel.x < 0:
            self.pos.x += step
            particle.pos.x -= step
        if self.pos.x < particle.pos.x and self.vel.x > 0:
            self.pos.x -= step
            particle.pos.x += step

        if self.pos.y < particle.pos.y and self.vel.y > 0:
            self.pos.y -= step
            particle.pos.y += step
        
        if self.pos.y > particle.pos.y and self.vel.y < 0:
            self.pos.y += step
            particle.pos.x -= step


                
    
class Player(Particle):
    lives = 3
    respawn = False
    start = True
    def __init__(self,bucket,canon):
        super().__init__(type='proton', pos=pygame.Vector2(SCREEN_WIDTH // 2, 20))
        self.is_player = True
        self.electroncapture = False
        self.angle = 0
        self.initial_speed = 10
        self.acc = pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(0,0)
        self.init_pos = pygame.Vector2(SCREEN_WIDTH // 2, 20)
        self.show = True
   
        self.bucket = bucket
        self.canon = canon
       


    # def update(self, particle, keys, dt):
    #     bucket = self.bucket
    #     canon = self.canon
    #     # control cannon angle
    #     if keys[pygame.K_LEFT]:
    #         self.angle += 1
    #         canon.angle += 1
    #     if keys[pygame.K_RIGHT]:
    #         self.angle -= 1
    #         canon.angle -= 1

    #     # shoot the player
    #     if keys[pygame.K_SPACE]:
    #         self.vel = pygame.Vector2(self.initial_speed * np.cos(self.angle), 
    #                                   self.initial_speed * np.sin(self.angle))

    #     # detect collisions and apply responses
    #     if pygame.sprite.collide_mask(self, particle):
    #         # reflect off of neutrons
    #         if particle.type == 'neutron' or particle.type == 'Higgs':
    #             self.vel.x *= -0.8
    #             self.vel.y *= -0.8

    #         # get "killed" by electrons
    #         if particle.type == 'electron':
    #             Player.lives -= 1
    #             if Player.lives != 0:
    #                 self.respawn = True
    #             self.electroncapture = True

    #     # gain a life if colliding with the bucket
    #     if pygame.sprite.collide_mask(self, bucket):
    #         Player.lives += 1
    #         self.respawn = True

    #     # respawn if needed
    #     if self.respawn:
    #         self.pos = pygame.Vector2(SCREEN_WIDTH // 2, 0)

    #     self.pos += self.vel * dt
    #     self.vel += self.acc * dt
    #     self.acc = pygame.Vector2(0, 0)  # reset acceleration
    #     self.acc += self.computeForce(particle)
    #     self.rect.center = self.pos





class HiggsDisturbance(Particle):

    def __init__(self,pos):
        super.__init__(type = 'Higgs',pos = pos,vel = pygame.Vector2(0,0))
        self.collisioncounter = 0

    def update(self,particle):
         if pygame.sprite.collide_mask(self,particle):
             self.collisioncounter += 1

         if self.collisioncounter > 3:
             self.kill()   
        
    

