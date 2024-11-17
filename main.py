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
    def __init__(self, x, y, width, height, function, text = None, Font = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        
        # Define a rectangle for interaction detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def process(self):
        # Detect mouse interactions and trigger the function
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Check for hover and click events
        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:  # Left mouse button
            self.function()

        
        
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

intromusic = pygame.mixer.music.load("Music/intro.mp3")
gamemusic = pygame.mixer.music.load("Music/game.mp3")

# game methods
def runIntro():
    # Load the background image
    background_image = pygame.image.load("Images/Menu_Title (1).png")
    
    intromusic.play(-1)
    
    # Create buttons with the correct positions and sizes, matching the image design
    startButton = Button(SCREEN_WIDTH / 3 - 15, SCREEN_HEIGHT / 2 - 125, 305, 70, runGame)    
    faqButton = Button(SCREEN_WIDTH / 3 - 15, SCREEN_HEIGHT / 2, 305, 70, runFAQ)
    exitButton = Button(SCREEN_WIDTH / 3 - 15, SCREEN_HEIGHT / 1.5 + 20, 305, 70, runEXIT)
    ifPiotr = Button(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT * (1 / 3 + 5 / 10), 100, 20, runPiotr)

    intro = True
    # play music
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the background image
        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(background_image, (SCREEN_WIDTH / 4, 0))  # Place the background image

        # Process button interactions (no rendering)
        startButton.process()
        faqButton.process()
        exitButton.process()
        ifPiotr.process()

        # Update the screen
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
    
    inst_title = pygame.font.SysFont('verdana', 100).render('FAQ', False, (250, 220, 210))
    
    inst_text = "Welcome to NUCLIO, a nuclear\n twist on the classic game Peggle!\n\n"\
                "GAME: Eliminate all neutrinos\n (red particles) \nwhile also collecting as\n many points as possible!\n"\
                "HOW TO PLAY:\n Use the arrow keys to\n adjust the launch angle your\n proton, and press the SPACE-bar\n to launch!\n\n"\
                "Forces:\n Note that the strong \nnuclear force is acting \non the particles, so \nthey will attract or repel each other,\n depending on their relative distances.\n More info to come...\n\n"
    
    inst_font = pygame.font.SysFont('verdana', 20)
    
    info_image = pygame.image.load("Images/Menu_Info.png")
    
    inst_text_lines = inst_text.split('\n')
    
    while faq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runEXIT()
        
        screen.fill((0, 0, 0))
        
        screen.blit(info_image, (SCREEN_WIDTH / 4, 0)) 
        
        screen.blit(inst_title, (SCREEN_WIDTH / 2 - inst_title.get_width() / 2, SCREEN_HEIGHT * (1 / 10)))
        
        y_offset = 175
        for line in inst_text_lines:
            inst_text_render = inst_font.render(line, False, (0, 0, 0))
            screen.blit(inst_text_render, (SCREEN_WIDTH / 2 - inst_text_render.get_width() / 2, y_offset))
            y_offset += inst_text_render.get_height() + 5
        
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
    
    intromusic.stop()
    gamemusic.play(-1)
    
    # add player to box
    boxes[0].addParticle(player)
    score = lives()
    
    # game loop
    running = True
    while running:
        screen.fill((0, 0, 0))
        boxes[0].addParticle(player)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            gamemusic.stop()
            runIntro()
        
        for box in boxes:
            box.updateBox(screen, keys, dt,bucket)
    
        canon.update(player, screen)
        bucket.update(player,screen,dt)
        score.update()
        screen.blit(score.lives, (SCREEN_WIDTH/2+40, 20))


        #win condition
        if Particle.neutrinos == 0:
            screen.fill((0,0,0))

        if Player.lives <= 0:
            screen.fill((0,0,0))
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamemusic.stop()
                running = False
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000


runIntro()
runEXIT()

    # if Particle.neutrinos == 0:
        # end condition
        
