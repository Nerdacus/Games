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

# General setup

pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])

# Snag the pacman sprite sheet.
mySprites = pygame.image.load("Arcade - Pac-Man - General Sprites.png")
# Show the size of the sheet
size = mySprites.get_size()
width = int(size[0])
height = int(size[1])
print("image size is: ", width, height)

# Try to grab the first part of it, it has 3 parts.
sprite_sheet_width = int(width/3)
rect = pygame.Rect(0, 0, sprite_sheet_width, height)
sheet0 = pygame.Surface([sprite_sheet_width, height])
sheet0.blit(mySprites, (0, 0), rect)


# Show the size of the sheet0
size = sheet0.get_size()
w = int(size[0])
h = int(size[1])
print("image size is: ", w, h)

# Try to grab the second part of it, it has 3 parts.
rect = pygame.Rect(sprite_sheet_width, 0, sprite_sheet_width+sprite_sheet_width, height)
sheet1 = pygame.Surface([sprite_sheet_width, height])
sheet1.blit(mySprites, (0, 0), rect)

# Show the size of the sheet
size = sheet1.get_size()
w = int(size[0])
h = int(size[1])
print("image size is: ", w, h)

# Try to grab the last part of it, it has 3 parts.
rect = pygame.Rect(2*sprite_sheet_width, 0, 3*sprite_sheet_width, height)
sheet2 = pygame.Surface([sprite_sheet_width, height])
sheet2.blit(mySprites, (0, 0), rect)

# Show the size of the sheet
size = sheet2.get_size()
w = int(size[0])
h = int(size[1])
print("image size is: ", w, h)

# Set caption on window frame
pygame.display.set_caption("Pac Man????")

running = True
while(running):
    # Handle events
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
            
        if (event.type == pygame.MOUSEBUTTONDOWN):
            pass
        
        #if (event.type == pygame.KEYDOWN):
        #    player.animate_me()
            
    key = pygame.key.get_pressed()
    if (key[pygame.K_ESCAPE]  == True):
        running = False
    
    # Draw 
    screen.blit(sheet0, [0, 0])
    screen.blit(sheet1, [0, height])
    screen.blit(sheet2, [0, 2*height])
    
    # Put surface to video memory
    pygame.display.flip()
    # Make sure we get 60 or frames per second
    clock.tick(60)

pygame.quit()
sys.exit()