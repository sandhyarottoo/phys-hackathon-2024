from player import *
from forces import *
from particles import *
from GLOBVAR import *



class Bucket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
        self.color = (0, 255, 0)
        self.vel = pygame.Vector2(50, 0)
        
        # Define image and rect for the bucket
        self.image = pygame.Surface((100, 15), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, self.image.get_rect())
        self.rect = self.image.get_rect(center=self.pos)
        
    def update(self, player, screen,dt):
        if pygame.sprite.collide_mask(self, player):
            self.betadecay = True

        # Change direction on screen edges
        if self.pos.x >= SCREEN_WIDTH or self.pos.x <= 0:
            self.vel *= -1

        # Update position and rect center
        self.pos.x += self.vel.x * dt
        self.rect.center = self.pos

        #pygame.draw.rect(self.image, self.color, self.image.get_rect())
        screen.blit(self.image, self.rect)
        

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



class lives():
    def __init__(self):
        self.lives = pygame.font.SysFont('verdana', 40).render(f"Remaining lives: {Player.lives}", False, (0,250,0))

    def update(self):
        self.lives = pygame.font.SysFont('verdana', 40).render(f"Remaining lives: {Player.lives}", False, (0,250,0))
