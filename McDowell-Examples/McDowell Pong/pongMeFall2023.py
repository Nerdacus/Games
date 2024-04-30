# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 18:37:41 2023

@author: patrick

Here we will use pygame to make a basic pong game.
"""
import pygame as p
import math as m
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

screenWidth = 700
screenHeight = 500

def orientXY(x0, y0):
    x = x0
    y = screenHeight - y0
    return x, y

def makePongTable(screen, width, height, xul, yul):
    x, y = orientXY(xul, yul)
    myRect = p.Rect(xul, yul, width, height)
    p.draw.rect(screen, GREEN, myRect, width= 2)
    return
class Turret:
    def __init__(self, x0, y0):
        self.x = x0
        self.y = y0
        self.radius = 10
        self.gunLength = 20
        self.gunAngle = 0
        self.bullets = []
        self.bulletSpeed = 1
        self.cooldown = 0
        return

    def drawTurret(self, screen):
        x, y = orientXY(self.x, self.y)
        p.draw.circle(screen, RED, [x, y], self.radius)
        angRad = m.radians(self.gunAngle)
        x2 = x + self.gunLength * m.cos(angRad)
        y2 = y - self.gunLength * m.sin(angRad)
        p.draw.line(screen, RED, [x, y], [x2, y2], 2)
        return

    def rotateTurret(self, angle):
        self.gunAngle += angle
        if self.gunAngle > 359:
            self.gunAngle = 0
        elif self.gunAngle <= 0:
            self.gunAngle = 359

    def shootBullet(self):
        if self.cooldown == 0:
            angRad = m.radians(self.gunAngle)
            xVel = self.bulletSpeed * m.cos(angRad)
            yVel = self.bulletSpeed * m.sin(angRad)
            self.bullets.append(Bullet(self.x, self.y, xVel, yVel))
            self.cooldown = 5  # Cooldown in frames


    def updateBullets(self, screen):
        bullets_to_remove = []
        for bullet in self.bullets:
            bullet.move()
            if bullet.x < 0 or bullet.x > screenWidth or bullet.y < 0 or bullet.y > screenHeight:
                bullets_to_remove.append(bullet)
            else:
                bullet.drawMe(screen, YELLOW)

        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)

        if self.cooldown > 0:
            self.cooldown -= 1

class Bullet:
    def __init__(self, x0, y0, xVel, yVel):
        self.x = x0
        self.y = y0
        self.radius = 3
        self.xVel = xVel
        self.yVel = yVel

    def move(self):
        self.x += self.xVel
        self.y += self.yVel

    def drawMe(self, screen, color):
        x, y = orientXY(self.x, self.y)
        p.draw.circle(screen, color, [x, y], self.radius)

class Paddle:
    def __init__(self, x0, y0, width, height, has_gun=False):  # Add a has_gun parameter
        self.x = x0
        self.y = y0
        self.width = width
        self.height = height
        self.halfW = int(width / 2)
        self.halfH = int(height / 2)
        self.has_gun = has_gun  # Store whether the paddle has a gun
        if self.has_gun:
            self.turret = Turret(x0, y0)  # Add a turret to the paddle
        return

    def drawPaddle(self, screen):
        xul = self.x - self.halfW
        yul = self.y + self.halfH
        x, y = orientXY(xul, yul)
        myRect = p.Rect(x, y, self.width, self.height)
        p.draw.rect(screen, YELLOW, myRect, width=2)

        if self.has_gun:
            self.turret.drawTurret(screen)  # Draw the turret if the paddle has a gun

        return
    
    def moveMe(self, yInc, botY, topY):
        
        self.x = self.x 
        self.y = self.y + yInc
        
        pTop = self.y + self.halfH
        pBot = self.y - self.halfH
        
        if (pTop > topY):
            self.y = self.y - (pTop - topY)
            
        if (pBot < botY):
            self.y = self.y + (botY - pBot)
        
        return
    
    def autoTrack(self, bX, bY, inc, botY, topY):
        if (bY > self.y):
            self.moveMe(inc, botY, topY)
        elif (bY < self.y):
            self.moveMe((-1 * inc), botY, topY)
        return
    
    def getPaddleXY(self):
        return self.x, self.y
    
    def didBallHit(self, bX, bY, bRad, side):
        hit = False
        if (side == 'l'):
            if ((bX - bRad) < (self.x + self.halfW)):
                if ( (bY >= (self.y - self.halfH)) and 
                   (bY <= (self.y + self.halfH)) ):
                    hit = True
        
        elif (side == 'r'):
            if ((bX + bRad) > (self.x - self.halfW)):
                if ( (bY >= (self.y - self.halfH)) and 
                   (bY <= (self.y + self.halfH)) ):
                    hit = True
         
        return hit
            
                
    
class ball:
    def __init__(self, x0, y0, radius, xVel0, yVel0):
        self.x = x0
        self.y = y0
        self.radius = radius
        self.xVel = xVel0
        self.yVel = yVel0
        return
    
    def drawMe(self, screen, color):
        x, y = orientXY(self.x, self.y)
        p.draw.circle(screen, color, [x, y], self.radius, 2)
        return
    
    def moveMe(self, xLeft, xRight, yLow, yHi):
        self.x = self.x + self.xVel
        self.y = self.y + self.yVel
        
        if ((self.x - self.radius) < xLeft):
            self.x = xLeft + self.radius
            self.xVel = -1 * self.xVel
            
        if ((self.x + self.radius) > xRight):
            self.x = xRight - self.radius
            self.xVel = -1 * self.xVel
            
        if ((self.y - self.radius) < yLow):
            self.y = yLow + self.radius
            self.yVel = -1 * self.yVel 
            
        if ((self.y + self.radius) > yHi):
            self.y = yHi - self.radius
            self.yVel = -1 * self.yVel 
            
        return
    
    def getXYRad(self):
        return self.x, self.y, self.radius
    
    def xBounce(self):
        self.xVel = self.xVel * -1
        return

def collide(bx, by, bRad, tx, ty, tw, th):
    collision = False
    if ((bx >= tx-tw/2-bRad) and (bx <= (tx+tw/2+bRad))) and ((by >= ty-th/2-bRad) and (by <= (ty+th/2+bRad))):
        collision = True
    return collision

def pongMe():
    
    p.init()
    
    
    # Set the width and height of the screen [width, height]
    size = (screenWidth, screenHeight)
    screen = p.display.set_mode(size)
     
    p.display.set_caption("pongMe()")
    
    # Set up random number generator.
    random.seed()
     
    # Loop until the user clicks the close button.
    running = True
     
    # Used to manage how fast the screen updates
    clock = p.time.Clock()
    
    # Set up some game objects.
    border = 50
    xMargin = 20
    gameHeight = 400
    gameWidth = 600
    
    leftX = border
    rightX = leftX + gameWidth
    yLow = border
    yHi = yLow + gameHeight
    
    midBoardX = border + int(gameWidth/2)
    midBoardY = border + int(gameHeight/2)
    
    leftPx = border + xMargin
    rightPx = border + gameWidth - xMargin
    paddleWidth = 20
    paddleHeight = 80
    paddleYinc = 3
    leftPaddle = Paddle(leftPx, midBoardY, paddleWidth, paddleHeight, has_gun=True)
    rightPaddle = Paddle(rightPx, midBoardY, paddleWidth, paddleHeight, has_gun=False)
    
    ballRad = 20
    xVel = random.randint(0, 2) + 2
    yVel = random.randint(0, 2) + 1
    duhBall = ball(midBoardX, midBoardY, ballRad, xVel, yVel)
    
    # -------- Main Program Loop -----------
    while running:
        # --- Main event loop
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False


        """ Check for keyboard presses. """
        key = p.key.get_pressed()
        
        # Handle keypresses.
        if (key[p.K_ESCAPE] == True): 
            running = False
        if (key[p.K_UP] == True): 
            leftPaddle.moveMe(paddleYinc, yLow, yHi)
        if (key[p.K_DOWN] == True): 
            leftPaddle.moveMe(-paddleYinc, yLow, yHi)
        if (key[p.K_LEFT] == True):
            pass
        if (key[p.K_RIGHT] == True):
            pass
        if key[p.K_d]:  # Rotate turret left
            leftPaddle.turret.rotateTurret(-2)
        if key[p.K_a]:  # Rotate turret right
            leftPaddle.turret.rotateTurret(2)
        if key[p.K_SPACE]:  # Fire turret bullet
            leftPaddle.turret.shootBullet()
        # --- Game logic should go here
        
        # Move the ball
        duhBall.moveMe(leftX, rightX, yLow, yHi)
        
        # Get Ball position.
        bX, bY, bRad = duhBall.getXYRad()
        
        # Move right paddle.
        rightPaddle.autoTrack(bX, bY, paddleYinc, yLow, yHi)
        
        # Check for a hit on the left paddle.
        hit = leftPaddle.didBallHit(bX, bY, bRad, 'l')
        # If there was a hit, do a bounce.
        if (hit == True):
            duhBall.xBounce()
        else:
            # Check for a hit on the right paddle.
            hit = rightPaddle.didBallHit(bX, bY, bRad, 'r')
            if (hit == True):
                duhBall.xBounce()
        
            
        # --- Screen-clearing code goes here
        leftPaddle.turret.updateBullets(screen)  # Pass the 'screen' argument here
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)

        # --- Drawing code should go here
        makePongTable(screen, 600, 400, 50, 50)
        leftPaddle.turret.updateBullets(screen)  # Pass the 'screen' argument here as well
        leftPaddle.turret.drawTurret(screen)
        rightPaddle.drawPaddle(screen)
        duhBall.drawMe(screen, ORANGE)
              
        # --- Go ahead and update the screen with what we've drawn.
        p.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(60)
     
    # Close the window and quit.
    p.quit()
    
    return

pongMe()
