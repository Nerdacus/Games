# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 13:36:40 2023

@author: patrick

In this file I will be messing around with a pacman stuff.

The pacMan sprite sheet came from here:
    https://www.spriters-resource.com/arcade/pacman/sheet/52631/
    

This file shows how to grab groups of pixels out of an image and put them into
another image.  It is clunky and is based on code from here:

https://ehmatthes.github.io/pcc_2e/beyond_pcc/pygame_sprite_sheets/

"""

import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self, source, pos_x, pos_y, num_sprites, sp_width, sp_height, sp_x0, sp_y0):
        super().__init__()
        self.is_animating = False
        self.sprites = []
        
        for j in range(num_sprites):
            mySprite = get_pixels_at((sp_x0 + j*sp_width), sp_y0, sp_width, sp_height, source)
            self.sprites.append(mySprite)
            
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.topleft = [pos_x, pos_y]
        
    def update(self, speed):
        if (self.is_animating == True):
            self.current_sprite += speed
            if (self.current_sprite >= len(self.sprites)):
                self.current_sprite = 0
                
            self.image = self.sprites[int(self.current_sprite)]
            
    def animate_me(self):
        self.is_animating = not(self.is_animating)
        
    def set_position(self, x0, y0):
        self.x = x0
        self.y = y0
        self.rect.topleft = [x0, y0]
        return
    
    def move_right(self):
        self.x = self.x + 1
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_left(self):
        self.x = self.x - 1
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_up(self):
        self.y = self.y - 1
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_down(self):
        self.y = self.y + 1
        self.rect.topleft = [self.x, self.y]
        return
    
    def get_sprite(self, sprite_index):
        return self.sprites[sprite_index]
    
    def add_sprite(self, mySprite):
        self.sprites.append(mySprite)
        return
    
    def saveSprites(self, fileName, spriteWidth, spriteHeight):
        # Make a surface to hold the game layer image.
        spriteSufaceWidth = spriteWidth * len(self.sprites)
        spriteSurfaceHeight = spriteHeight
        mySpriteSurface = pygame.Surface((spriteSufaceWidth, spriteSurfaceHeight))
        
        # Blit the sprites to the screen.
        x = 0
        y = 0
        for sprite in self.sprites:
            mySprite = pygame.transform.scale(sprite, [spriteWidth, spriteHeight])
            mySpriteSurface.blit(mySprite, [x, y])
            x = x + spriteWidth
        # Save the screen as .png
        pygame.image.save(mySpriteSurface, fileName)
        return
        
        
def rescale_Sprite(sprite0, scaleFactor):
    size = sprite0.get_size()
    width = int(size[0]) * scaleFactor
    height = int(size[1]) * scaleFactor
    scaledSprite = pygame.transform.scale(sprite0, [width, height])
    return scaledSprite

def get_pixels_at(x, y, width, height, image0):
    rect = pygame.Rect(x, y, width, height)
    pixels = pygame.Surface((width, height))
    pixels.blit(image0, (0, 0), rect)
    
    return pixels

# General setup

pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])

# Snag the pacman sprite sheet.
spriteSheet = pygame.image.load("Arcade - Pac-Man - General Sprites.png")
# Show the size of the sheet
size = spriteSheet.get_size()
width = int(size[0])
height = int(size[1])
print("spriteSheet size is: ", width, height)

# Get sprite sheet 0.
sheet_width = int(width/3)
print("sheet_width = ", sheet_width)
sheet0 = get_pixels_at(0, 0, sheet_width, height, spriteSheet)

# Get sprite sheet 1
sheet1 = get_pixels_at(sheet_width, 0, sheet_width, height, spriteSheet)

# Get sprite sheet 2
sheet2 = get_pixels_at(2*sheet_width, 0, sheet_width, height, spriteSheet)

# Extract pacman moving right from sprite sheet 2
pacManR = Player(sheet2, 0, 0, 3, 17, 16, 0, 0)
moving_sprites = pygame.sprite.Group()
moving_sprites.add(pacManR)
pacManR.set_position(sheet_width, height)

# Extract pacman moving left from sprite sheet 2
pacManL = Player(sheet2, 0, 0, 2, 16, 16, 2, 16)
moving_sprites.add(pacManL)
# Add the last sprite from above to this pacman
mySprite = pacManR.get_sprite(2)
pacManL.add_sprite(mySprite)
pacManL.set_position(sheet_width, height + 32)

# Extract pacman moving up from sprite sheet 2
pacManU = Player(sheet2, 0, 0, 2, 16, 16, 2, 32)
moving_sprites.add(pacManU)
# Add the last sprite from above to this pacman
mySprite = pacManR.get_sprite(2)
pacManU.add_sprite(mySprite)
pacManU.set_position(sheet_width, height + 64)

# Extract pacman moving down from sprite sheet 2
pacManD = Player(sheet2, 0, 0, 2, 16, 16, 2, 48)
moving_sprites.add(pacManD)
# Add the last sprite from above to this pacman
mySprite = pacManR.get_sprite(2)
pacManD.add_sprite(mySprite)
pacManD.set_position(sheet_width, height + 80)

# Snag the maze parts sprite sheet.
mazeSheet = pygame.image.load("Arcade - Pac-Man - Maze Parts.png")
# Show the size of the sheet
size = mazeSheet.get_size()
width = int(size[0])
height = int(size[1])
print("mazeSheet size is: ", width, height)

# Snag the parts sprites from the maze parts image.
sheet_width = sheet_width - 1
mazeParts = get_pixels_at(sheet_width, 0, 144, 80, mazeSheet)

# Get blue tiles from maze parts, start at 225, 27, read 8 by 8, skip border
# of one, read 8 by 8.  Do this 16 times.
tiles = []
x = 0
y = 0
xinc = 9
yinc = 9
x_size = 8
y_size = 8
scaleFactor = 6
for j in range(3):
    x = 0
    for k in range(16):
        mySprite = get_pixels_at(x, y, x_size, y_size, mazeParts)
        scaledSprite = rescale_Sprite(mySprite, scaleFactor)
        tiles.append(scaledSprite)
        print("start x = ", x + sheet_width, " end x = ", x + x_size + sheet_width)
        x = x + xinc
        
        y = y
    y = y+yinc
    


# Set caption on window frame
pygame.display.set_caption("Pac Man????")

running = True
while(running):
    # Handle events
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
            
        if (event.type == pygame.MOUSEBUTTONDOWN):
            pacManR.animate_me()
            pacManL.animate_me()
            pacManU.animate_me()
            pacManD.animate_me()
        
    key = pygame.key.get_pressed()
    if (key[pygame.K_ESCAPE]  == True):
        running = False
    if (key[pygame.K_UP] == True): 
        pacManU.move_up()
    if (key[pygame.K_DOWN] == True): 
        pacManD.move_down()
    if (key[pygame.K_LEFT] == True):
        pacManL.move_left()
    if (key[pygame.K_RIGHT] == True):
        pacManR.move_right()
    if (key[pygame.K_SPACE] == True):
        pass
        
    
    # Game logic
    
    
    # Draw 
    # Draw various parts of sprite sheet.
    screen.blit(spriteSheet, [0, 0])
    screen.blit(sheet0, [0, height])
    screen.blit(sheet1, [0, 2*height])
    screen.blit(sheet2, [sheet_width, 2*height])
    screen.blit(mazeSheet, [2*sheet_width, 2*height])
    screen.blit(mazeParts, [4*sheet_width, 2*height])
    
    
    # Draw the tiles from the sprite sheet.
    xSpot = sheet_width+100
    ySpot = height+50
    j = 0
    for t in tiles:
        screen.blit(t, [xSpot, ySpot])
        xSpot = xSpot + (x_size*scaleFactor)+4
        j = j+1
        if ((j % 16) == 0):
            xSpot = sheet_width + 100
            ySpot = ySpot + (y_size*scaleFactor) + y_size
    
    moving_sprites.update(.10)
    moving_sprites.draw(screen)
    
    
    
    
    # Put surface to video memory
    pygame.display.flip()
    # Make sure we get 60 or frames per second
    clock.tick(60)
    
pacManR.saveSprites("pacManR.png", 48, 48)
pacManL.saveSprites("pacManL.png", 48, 48)
pacManD.saveSprites("pacManD.png", 48, 48)
pacManU.saveSprites("pacManU.png", 48, 48)

pygame.quit()
sys.exit()