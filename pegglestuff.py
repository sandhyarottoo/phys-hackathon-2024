from player import *
from forces import *
from particles import *
from GLOBVAR import *



class Bucket(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.Vector2(SCREEN_HEIGHT+20,SCREEN_WIDTH//2)
        self.betadecay = False
        self.color = (0,255,0)
        self.vel = pygame.Vector2(10,0)
        self.image = pygame.Surface((10,4))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        pygame.draw.rect(self.image,self.color,self.rect)

    def update(self,player,screen):

        if pygame.sprite.collide_mask(self,player):
            self.betadecay = True

        if self.pos.x >= SCREEN_WIDTH or self.pos.x <= 0:
            self.vel *= -1
        self.pos += self.vel*dt
        self.rect.center = self.pos
        pygame.draw.rect(self.image,self.color,self.rect)
        screen.blit(self.image, self.rect.topleft)
        


class Canon(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 90
        self.original_image = pygame.transform.rotozoom(canon_png, self.angle, 0.3)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 0))  # Position in the center top
        self.max_angle = 65
        self.min_angle = -65

    def update(self, player, screen):
        # Rotate the cannon based on the player's angle
        self.angle = player.angle  # Update the angle from the player input

        # Rotate the image and update the rect to maintain the center position
        self.image = pygame.transform.rotate(self.original_image, -self.angle)  # Negative to rotate clockwise
        self.rect = self.image.get_rect(center=self.rect.center)  # Keep the center consistent

        # Blit the updated image to the screen
        screen.blit(self.image, self.rect.topleft)



