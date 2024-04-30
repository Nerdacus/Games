# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 08:46:31 2018

@author: userselu
"""

import pygame as p
import math as m

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
MYCOLOR = (100,75,255)

screenWidth = 700
screenHeight = 500



class bullet:
    def __init__(self, x0, y0, heading0):
        self.x = x0
        self.y = y0
        self.radius = 5
        self.heading = heading0
        self.velocity = 20
        self.exists = True
        self.hit = False
        return
    
    def drawMe(self, s):
        if (self.hit == False):
            p.draw.circle(s, MYCOLOR, [int(self.x), int(self.y)], self.radius, 1)
        else:
            self.explodeMe(s)
            
        return
    
    def moveMe(self):
        angRad = deg2Rad(self.heading)
        bX = self.x + self.velocity*m.cos(angRad)
        bY = self.y + self.velocity*m.sin(angRad)
        if ((bX > 0) and (bX < screenWidth))and((bY > 0) and (bY < screenHeight)):
            self.x = bX
            self.y = bY
        else:
            self.exists = False              
        return
    
    def doIExist(self):
        return self.exists
    
    def explodeMe(self, s):
        p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius-4, 1)
        p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius, 1)
        p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius+4, 1)
        p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+6, 1)
        p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+9, 1)
        p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+11, 1)
        p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+13, 1)
        
        self.hit = False
        self.exists = False
        return
    
class target:
    def __init__(self, x0, y0, heading0):
        self.x = x0
        self.y = y0
        self.width = 20
        self.height = 30
        self.heading = heading0
        self.velocity = 5
        self.exists = True
        return
    
    def drawMe(self, s):
        p.draw.rect(s, RED, [self.x - self.width/2,self.y - self.height/2, self.width, self.height], 2)
        return
    
    def moveMe(self):
        angRad = deg2Rad(self.heading)
        bX = self.x + self.velocity*m.cos(angRad)
        bY = self.y + self.velocity*m.sin(angRad)
        if ((bX > 0) and (bX < screenWidth))and((bY > 0) and (bY < screenHeight)):
            self.x = bX
            self.y = bY
        else:
            self.exists = False              
        return
    
    def doIExist(self):
        return self.exists
    
    

class turret:
   def  __init__(self, x0, y0, rad0):
        self.x = x0
        self.y = y0
        self.rad = rad0
        self.gunLen = rad0*2
        self.gunAngle = 270
        self.gunTipX = 0
        self.gunTipY = 0      
        return
    
   def drawMe(self, s):
       p.draw.circle(s, WHITE, [self.x, self.y], self.rad, 1)
       angRad = deg2Rad(self.gunAngle)
       self.gunTipX = self.x + self.gunLen*m.cos(angRad)
       self.gunTipY = self.y + self.gunLen*m.sin(angRad)
       p.draw.line(s, WHITE, [self.x, self.y], [self.gunTipX, self.gunTipY], 1)
       
   def rotateMe(self, inc):
       self.gunAngle = self.gunAngle + inc
       if (self.gunAngle >= 360):
           self.gunAngle = 0;
       elif (self.gunAngle < 0):
           self.gunAngle = 359
       return
   
   def getGunTip(self):
       x = self.gunTipX
       y = self.gunTipY
       
       return x, y
   
   def getGunAngle(self):
       return self.gunAngle
   
    
def deg2Rad(deg):
    rad = (deg/180.0)*m.pi
    return rad

def collide(bx, by, bRad, tx, ty, tw, th):
    collision = False
    if ((bx >= tx-tw/2-bRad) and (bx <= (tx+tw/2+bRad))) and ((by >= ty-th/2-bRad) and (by <= (ty+th/2+bRad))):
        collision = True
    return collision


def learnGame():
    
    turrX = (int)(screenWidth/2)
    turrY = screenHeight - 50
    
    testX = (int)(screenWidth/2)
    testY = 20
    
    p.init()
    
    t = turret(turrX, turrY, 20)
    testTarget = target(testX, testY, 90)
    bullets = []
    
    # Set the width and height of the screen [width, height]
    size = (screenWidth, screenHeight)
    screen = p.display.set_mode(size)
     
    p.display.set_caption("learnGame()")
     
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
            t.rotateMe(-1)
        if (key[p.K_RIGHT] == True): 
            t.rotateMe(1)
        if (key[p.K_SPACE] == True):
            gx, gy = t.getGunTip()
            ang = t.getGunAngle()
            bullets.append(bullet(gx, gy, ang))
            
        # --- Game logic should go here
        # --- Move bullets 
        for b in bullets:
            b.moveMe()
            if (b.doIExist() == False):
                bullets.remove(b)
                print(len(bullets))
        
        # --- Check to see if the bullets hit anything
        for b in bullets:
            b.hit = collide(b.x, b.y, b.radius, testTarget.x, testTarget.y, testTarget.width, testTarget.height)
            if (b.hit == True):
                print("Hit me baby!!!")
               
                
                
            
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)
     
        # --- Drawing code should go here
        t.drawMe(screen)
        for j in range(0, len(bullets)):
            bullets[j].drawMe(screen)
            
        testTarget.drawMe(screen)
                
        # --- Go ahead and update the screen with what we've drawn.
        p.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(60)
     
    # Close the window and quit.
    p.quit()
    
    return


learnGame()