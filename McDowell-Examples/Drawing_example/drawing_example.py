# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 18:17:34 2023

@author: patrick

Just found out I am teaching game class, so I need to practice.

"""

import pygame as p

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

screenWidth = 1000
screenHeight = 750

def pyGameTemplate():
    
    p.init()
    
    
    # Set the width and height of the screen [width, height]
    size = (screenWidth, screenHeight)
    screen = p.display.set_mode(size)
     
    p.display.set_caption("basic Python graphics window()")
     
    # Loop until the user clicks the close button.
    running = True 
     
    # Used to manage how fast the screen updates
    clock = p.time.Clock()
     
    # -------- Main Program Loop -----------
    while running:
        # --- Main event loop
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        
        """ Check for keyboard presses. """
        key = p.key.get_pressed()
        
        if (key[p.K_ESCAPE] == True): 
            running = False
        if (key[p.K_UP] == True): 
            pass
        if (key[p.K_DOWN] == True): 
            pass
        if (key[p.K_LEFT] == True):
            pass
        if (key[p.K_RIGHT] == True):
            pass
        if (key[p.K_SPACE] == True):
            pass
            
        # --- Game logic should go here
        
            
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)

     
        # --- Drawing code should go here
        p.draw.circle(screen, ORANGE, [350, 250], 50, 10)
        p.draw.line(screen, GREEN, [0, 0], [700, 500], 2)
        p.draw.line(screen, CYAN, [0, 500], [700, 0], 2)

                
        # --- Go ahead and update the screen with what we've drawn.
        p.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(60)
     
    # Close the window and quit.
    p.quit()
    
    return

pyGameTemplate()