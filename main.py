
from particles import *
from pegglestuff import *
from box import Box, boxes
from GLOBVAR import *
import forces
import pygame

keys = pygame.key.get_pressed()
bucket = Bucket()
canon = Canon()
player = Player(keys,bucket,canon)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

running = True
dt = 0
while running:
    screen.fill((0, 0, 0))
    
    for box in boxes:
        box.updateBox()
        box.draw(screen, signal_content=True)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000



    # if Particle.neutrinos == 0:
        # end condition