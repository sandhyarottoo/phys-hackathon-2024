import torch
import pygame
from GLOBVAR import *
from electron import Electron

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

electron_pos = pygame.Vector2(0, 0)
electron_vel = pygame.Vector2(0, 0)
electron = Electron()
electron.load_state_dict(torch.load('model.pth', weights_only=True, map_location=torch.device('cpu')))
prev_mouse_pos = pygame.Vector2(*pygame.mouse.get_pos())

running = True
dt = 0.001
while running:
    screen.fill((0, 0, 0))
    
    mouse_pos = pygame.Vector2(*pygame.mouse.get_pos())
    mouse_vel = (mouse_pos - prev_mouse_pos) / dt
    prev_mouse_pos = mouse_pos
    pos_diff = mouse_pos - electron_pos

    t = torch.tensor([pos_diff.x, pos_diff.y, electron_vel.x, electron_vel.y, mouse_pos.x, mouse_pos.y, dt])
    with torch.no_grad():
        a = 4*electron(t)
        a = pygame.Vector2(a[0].item(), a[1].item())

    pygame.draw.circle(screen, (0, 255, 0), mouse_pos, 10)
    pygame.draw.circle(screen, (255, 255, 255), (electron_pos.x, electron_pos.y), 10)

    electron_vel += a*dt
    electron_pos += 1*electron_vel*dt
    #electron_vel *= 0.99
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000
