import random
import pygame, sys
from pygame.locals import *

# Set up the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

windowwidth = 400
windowheight = 400

# Creates display surface
displaysurf = pygame.display.set_mode((windowwidth, windowheight))

# Cotnrols the fps of game
fps_clock = pygame.time.Clock()
fps = 20 # FPS of game

class Game():
    def __init__(self, linethickness=10):
        self.linethickness = linethickness
        
        # Initiate variables and starting positions
        head_x = int(windowwidth/2)
        head_y = int(windowheight/2)
        pel_x = random.randrange(self.linethickness*2, windowwidth - self.linethickness*2, self.linethickness)
        pel_y = random.randrange(self.linethickness*2, windowheight - self.linethickness*2, self.linethickness)
        self.head = Snake(head_x, head_y, self.linethickness, self.linethickness, self.linethickness)
        self.pellet = Pellet(pel_x, pel_y, self.linethickness, self.linethickness)
        
    # Draws arena game will be played in
    def draw_arena(self):
        displaysurf.fill(BLACK)
        # Draw outline of arena
        pygame.draw.rect(displaysurf, RED, ((0,0),(windowwidth,windowheight)), self.linethickness*2)
        
    def update(self):
        newpel_x = random.randrange(self.linethickness*2, windowwidth - self.linethickness*2, self.linethickness)
        newpel_y = random.randrange(self.linethickness*2, windowheight - self.linethickness*2, self.linethickness)
        
        self.draw_arena()
        self.head.draw_head()
        self.head.draw_tail()
        self.head.move_head()
        self.head.change_dir()
        self.head.checkGameOver()
        
        if self.head.eat(self.pellet):
            self.pellet = Pellet(newpel_x, newpel_y, self.linethickness, self.linethickness)
        
        
        self.pellet.draw_pellet()

class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, scl):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.scl = scl
        # snake can only move in one direction, either 0, 1, or -1
        self.dirX = 0 #  0 - none, 1 - right, -1 - left
        self.dirY = 1 #  0 - none, 1 - down, -1 - up
        
        self.total = 0
        self.tail = []
        
        self.rect = pygame.Rect((self.x, self.y), (self.w, self.h))
    
    # Draws the snake
    def draw_head(self):
        self.tail.append(self.getLocation())
        #print (self.getLocation())
        pygame.draw.rect(displaysurf, WHITE, self.rect)
    
    # Draws and extends the body of the snake    
    def draw_tail(self):
        self.tail = self.tail[::-1]
        #print(self.tail)
        for x in range(self.total):
            coor = self.tail[x+1]
            coor = tuple(coor)
            self.tailrect = pygame.Rect(coor, (self.w, self.h))
            pygame.draw.rect(displaysurf, WHITE, self.tailrect)
    
    # Moves the head returns new position
    def move_head(self):
        self.rect.x += (self.dirX*self.scl)
        self.rect.y += (self.dirY*self.scl)  
        
        # Checks for collision with walls
        if self.hit_wall():
            if self.dirX == -1:
                self.rect.left = self.w
            else:
                self.rect.right = windowwidth - self.w
        elif self.hit_ceiling_floor():
            if self.dirY == -1:
                self.rect.top = self.w
            else:
                self.rect.bottom = windowheight - self.w
    
    # Controls direction of snake head
    def change_dir(self):
        keys = pygame.key.get_pressed() # checking pressed keys
        if keys[pygame.K_UP]:
            self.dirX = 0
            self.dirY = -1
        elif keys[pygame.K_DOWN]:
            self.dirX = 0
            self.dirY = 1
        elif keys[pygame.K_LEFT]:
            self.dirX = -1
            self.dirY = 0
        elif keys[pygame.K_RIGHT]:
            self.dirX = 1
            self.dirY = 0
            
    
    def hit_wall(self):
        if ((self.dirX == -1 and self.rect.left <= self.w) or
             self.dirX == 1 and self.rect.right >= windowwidth - self.w):
            return True
        else:
            return False
    
    def hit_ceiling_floor(self):
        if ((self.dirY == -1 and self.rect.top <= self.w) or
             self.dirY == 1 and self.rect.bottom >= windowheight - self.w):
            return True
        else:
            return False
    
    def eat(self, pellet):
        if pygame.sprite.collide_rect(self, pellet):
            self.total += 1
            return True
        else:
            return False
        
    def getLocation(self):
        return [self.rect.x, self.rect.y]
    
    def checkGameOver(self):
        if self.hit_wall() or self.hit_ceiling_floor():
            return True
        else:
            return False

class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    
    def draw_pellet(self):
        pygame.draw.rect(displaysurf, WHITE, self.rect)
     
# Main Function
def main():
    pygame.init()
    pygame.display.set_caption('Snake')
    pygame.mouse.set_visible(1) # make cursor invisible/visible
    
    game = Game()
    
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        game.update()
        pygame.display.update()
        fps_clock.tick(fps)
        
if __name__=='__main__':
    main()
