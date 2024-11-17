from particles import *
from pegglestuff import *
from box import Box, boxes
from GLOBVAR import *
import forces
import pygame
import sys

bucket = Bucket()
canon = Canon()

### BUTTON CLASS ###
class Button():
    def __init__(self, x, y, width, height, function, text, font, inMenu=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        
        
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        if inMenu:
            self.textSurf = font.render(text,True, (40, 40, 40))
            self.colors = {
                'normal': (196,164,132),
                'hover': (156, 124, 92),
                'pressed': (220, 220, 220),
            }
        else:
            self.textSurf = font.render(text,True, (200, 200, 200))
            self.colors = {
                'normal': (160, 160, 160),
                'hover' : (190, 190, 190),
                'pressed': (130,130,130)
            }
        
    def process(self):
        mouse = pygame.mouse
        mousePos = mouse.get_pos()
        self.surface.fill(self.colors['normal'])
        if self.rect.collidepoint(mousePos):
            self.surface.fill(self.colors['hover'])
            if mouse.get_pressed(num_buttons=3)[0]:
                self.surface.fill(self.colors['pressed'])
                self.function()
                
        self.surface.blit(self.textSurf, [self.rect.width/2 - self.textSurf.get_rect().width/2, 
                                                self.rect.height/2 - self.textSurf.get_rect().height/2])
        screen.blit(self.surface, self.rect)
        
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
        

#### GAME ####
pygame.init()
pygame.display.set_caption("NUCLIO")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# setting fonts
font = pygame.font.SysFont('arial', 40)

keys = pygame.key.get_pressed()
player = Player(bucket,canon)

piotrfont = pygame.font.SysFont('arial', 12)

# game methods
def runIntro():
    startButton = Button(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT*(1/3+2/10), 200, 50, runGame, "Start", font)
    faqButton = Button(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT*(1/3 + 3/10), 200, 50, runFAQ, "FAQ", font)
    exitButton = Button(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT*(1/3 + 4/10), 200, 50, runEXIT, "Exit", font)
    
    ifPiotr = Button(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT*(1/3 + 5/10), 100, 20, runPiotr, "Press if Piotr", piotrfont, inMenu=False)
    
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0,0,0))
        startButton.process()
        faqButton.process()
        exitButton.process()
        ifPiotr.process()
        
        pygame.display.flip()
        clock.tick(60)
        
def runPiotr():
    menuButton = Button(20, 10, 140, 50, runIntro, "Menu", font)
    piotr = True
    while piotr:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runEXIT()
        screen.fill((0, 0, 0))
        screen.blit(font.render("Get outa here you silly boy you", True, (255, 255, 255)), (SCREEN_WIDTH/2 - 300, SCREEN_HEIGHT/2))
        menuButton.process()
        pygame.display.flip()
        clock.tick(60)
    
def runEXIT():
    pygame.quit()
    sys.exit()
    
def runFAQ():
    faq = True
    menuButton = Button(20, 10, 140, 50, runIntro, "Menu", font)
    
    # main text
    inst_title = pygame.font.SysFont('verdana', 100).render('FAQ', False, (250, 220, 210))

    inst_text = "Welcome to NUCLIO, a nuclear twist on the classic game Peggle!\n\n"\
                "GAME: Eliminate all neutrinos (red particules) while also collecting as many points as possible!\n\n"\
                "HOW TO PLAY: Use the arrow keys to adjust the launch angle your proton, and press the SPACE-bar to launch!\n\n"\
                "Forces: Note that the strong nuclear force is acting on the particles, so they will attract or repel each other, depending on their relative distances. More info to come...\n\n" 
    inst_font = pygame.font.SysFont('verdana', 20)
    
    while faq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runEXIT()
        screen.fill((0, 0, 0))
        screen.blit(inst_title, (SCREEN_WIDTH/2 - inst_title.get_width()/2, SCREEN_HEIGHT*(1/10)))
        blit_text(screen, inst_text, (15, 275), inst_font, (250, 200, 200))
        # screen.blit(instructions, (WIDTH/2-instructions.get_width()/2, HEIGHT/2-instructions.get_height()/2))
        menuButton.process()
        pygame.display.flip()
        clock.tick(60)

def runGame():
    global dt
    global player
    global boxes
    global bucket
    global canon
    global keys
    global screen
    
    # add player to box
    boxes[0].addParticle(player)
    
    # game loop
    running = True
    while running:
        screen.fill((0, 0, 0))
        boxes[0].addParticle(player)
        
        keys = pygame.key.get_pressed()
        
        for box in boxes:
            box.updateBox(screen, keys, dt)
    
        canon.update(player, screen)
        bucket.update(player,screen)

        #win condition
        if Particle.neutrinos == 0:
            screen.fill((0,0,0))
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000


runIntro()
runEXIT()

    # if Particle.neutrinos == 0:
        # end condition
        
