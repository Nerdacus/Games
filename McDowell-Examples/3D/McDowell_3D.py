# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 09:03:14 2023

@author:pm


This file is for experimenting with basic 3d displays.

The goal for this is to the camera features of openGL working.  (good luck buddy)

NOTE: z is height in this 3d representation.  not MAYBE, for sure.


"""

import math
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GLUT as glut

import numpy
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (64, 64, 64)
PURPLE = (128, 0, 128)

screenWidth = 1200
screenHeight = 800


def drawFloor(llx, lly, urx, ury, numDivs):
    xInc = (urx - llx) / numDivs
    x = llx
    for j in range(numDivs + 1):
        drawLine3f(x, lly, -2, x, ury, -2)
        x = x + xInc

    yInc = (ury - lly) / numDivs
    y = lly
    for j in range(numDivs + 1):
        drawLine3f(llx, y, -2, urx, y, -2)
        y = y + yInc

    return


def hiddenLineTest(sphere, x, y, z):
    # Push a matrix, enable depth testing.
    glPushMatrix();
    glEnable(GL_DEPTH_TEST)

    # Set polygon mode.
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Set_color(foreground)
    setColor(YELLOW)

    # Move to a cool spot.
    glTranslatef(x, y, z)

    # Draw a wire cube.
    gluSphere(sphere, 2.0, 32, 16)

    # Draw_object_with_filled_polygons()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0, 1.0)

    # Set_color(background)
    setColor(ORANGE)

    # Draaw a solid cube.
    # Draw a wire cube.
    gluSphere(sphere, 2.0, 32, 16)

    # Disable and pop.
    glDisable(GL_POLYGON_OFFSET_FILL)
    glPopMatrix();

    return


def makeTerrain(nrows, ncols):
    myTerrain = numpy.zeros([nrows, ncols], dtype=float)

    # Base terrain map.
    for j in range(nrows):
        for k in range(ncols):
            myTerrain[j][k] = -2

    # Put in a random number of peaks.
    nPeaks = random.randint(20, 40)
    for j in range(nPeaks):
        # Select a random position and place a peak
        myRow = random.randint(0, nrows - 1)
        myCol = random.randint(0, ncols - 1)

        # Create a peak.
        myPeak = random.randint(-2, 48)

        # Place peak into terrain.
        myTerrain[myRow][myCol] = myPeak

    # Average the terrain.
    radius = 3
    for j in range(nrows):
        for k in range(ncols):
            myTerrain[j][k] = nearGridAv(j, k, nrows, ncols, radius, myTerrain)

    return myTerrain


def nearGridAv(j, k, nrows, ncols, radius, myTerrain):
    startRow = j - radius
    endRow = j + radius
    startCol = k - radius
    endCol = k + radius

    mySum = 0
    count = 0
    for jIndex in range(startRow, endRow):
        for kIndex in range(startCol, endCol):
            if ((jIndex >= 0) and (jIndex < nrows)):
                if ((kIndex >= 0) and (kIndex < ncols)):
                    mySum = mySum + myTerrain[jIndex][kIndex]
                    count = count + 1

    height = mySum / count
    return height


def drawTerrainPolygons(llx, lly, urx, ury, nRows, nCols, myTerrain):
    xInc = (urx - llx) / nCols
    yInc = (ury - lly) / nRows

    xHalf = (urx - llx) / 2
    yHalf = (ury - lly) / 2

    setColor(YELLOW)

    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    x = llx
    y = lly

    for j in range(nRows - 1):
        x = llx
        for k in range(nCols - 1):
            glBegin(GL_POLYGON)

            glVertex3f(x, y, myTerrain[j][k])
            glVertex3f(x + xInc, y, myTerrain[j][k + 1])
            glVertex3f(x + xInc, y + yInc, myTerrain[j + 1][k + 1])
            glVertex3f(x, y + yInc, myTerrain[j + 1][k])

            glEnd()

            x = x + xInc

        y = y + yInc

    setColor(PURPLE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0, 1.0)

    x = llx
    y = lly
    z = -2
    for j in range(nRows - 1):
        x = llx
        for k in range(nCols - 1):
            glBegin(GL_POLYGON)

            glVertex3f(x, y, myTerrain[j][k])
            glVertex3f(x + xInc, y, myTerrain[j][k + 1])
            glVertex3f(x + xInc, y + yInc, myTerrain[j + 1][k + 1])
            glVertex3f(x, y + yInc, myTerrain[j + 1][k])

            glEnd()

            x = x + xInc

        y = y + yInc

    glDisable(GL_POLYGON_OFFSET_FILL)

    return


def drawFloor_In_polygons(llx, lly, urx, ury, numDivs):
    xInc = (urx - llx) / numDivs
    yInc = (ury - lly) / numDivs
    zInc = .1

    xHalf = (urx - llx) / 2
    yHalf = (ury - lly) / 2

    setColor(YELLOW)

    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    x = llx
    y = lly
    z = -2
    for j in range(numDivs + 1):
        x = llx
        for k in range(numDivs + 1):
            glBegin(GL_POLYGON)

            glVertex3f(x, y, z)
            glVertex3f(x, y + yInc, z)
            glVertex3f(x + xInc, y + yInc, z)
            glVertex3f(x + xInc, y, z)

            glEnd()

            x = x + xInc

        y = y + yInc

    setColor(PURPLE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0, 1.0)

    x = llx
    y = lly
    z = -2
    for j in range(numDivs + 1):
        x = llx
        for k in range(numDivs + 1):
            glBegin(GL_POLYGON)

            glVertex3f(x, y, z)
            glVertex3f(x, y + yInc, z)
            glVertex3f(x + xInc, y + yInc, z)
            glVertex3f(x + xInc, y, z)

            glEnd()

            x = x + xInc

        y = y + yInc

    glDisable(GL_POLYGON_OFFSET_FILL)

    return


def deg2Rad(deg):
    rad = deg / 180.0 * math.pi
    return rad


def rad2Deg(rad):
    deg = rad / math.pi * 180.0
    return deg


def dist(x0, y0, x1, y1):
    myDist = (x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)
    myDist = math.sqrt(myDist)
    return myDist


def orientXY(x0, y0):
    x = int(x0)
    y = int(screenHeight - y0)
    return x, y


def setColor(color):
    r = float(color[0]) / 255.0
    g = float(color[1]) / 255.0
    b = float(color[2]) / 255.0
    glColor3f(r, g, b)
    return


def drawLine3f(x0, y0, z0, x1, y1, z1):
    glBegin(GL_LINES)

    v0 = (x0, y0, z0)
    v1 = (x1, y1, z1)

    glVertex3fv(v0)
    glVertex3fv(v1)

    glEnd()
    return


def drawCircle3f(cx, cy, cz, radius):
    glPushMatrix()
    glTranslate(0, 0, 0)
    glBegin(GL_LINE_LOOP)
    ang = 0
    angInc = 360.0 / 20.0
    for j in range(20):
        x = cx + radius * math.cos(deg2Rad(ang))
        y = cy + radius * math.sin(deg2Rad(ang))
        z = cz
        myVertex = (x, y, z)
        glVertex3fv(myVertex)
        ang = ang + angInc
    glEnd()
    glPopMatrix()

    return


def menu():
    print("Esc - quit")
    print("Arrow keys - move forward, backward, left, right")
    print("Page Up - move up in altitude, Page Down - mvoe down in altitude")
    print()
    print("Number pad arrow keys")
    print("left - rotate left or counter clockwise")
    print("right - rotate right or clockwise")
    print("up - pitch nose down")
    print("down - pitch nose up")


class bullet():

    def __init__(self, x0, y0, z0, heading0, pitch0, velocity0):
        self.x = x0
        self.y = y0
        self.z = z0

        self.heading = heading0
        self.pitch = pitch0
        self.velocity = velocity0

        self.exists = True
        self.exploding = False

        self.sphere = gluNewQuadric()
        return

    def drawMe(self):
        # Push a matrix, enable depth testing.
        glPushMatrix();
        glEnable(GL_DEPTH_TEST)

        # Set polygon mode.
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Set_color(foreground)
        setColor(RED)

        # Move to current position.
        glTranslatef(self.x, self.y, self.z)

        # Draaw a solid sphere.
        gluSphere(self.sphere, 0.2, 32, 16)

        # Disable and pop.
        glDisable(GL_POLYGON_OFFSET_FILL)
        glPopMatrix();

        return

    def moveMe(self):
        headingRad = deg2Rad(self.heading)
        pitchRad = deg2Rad(self.pitch)
        self.x = self.x + self.velocity * math.cos(headingRad)
        self.y = self.y + self.velocity * math.sin(headingRad)
        self.z = self.z + self.velocity * math.sin(pitchRad)


def updatePosition(x0, y0, z0, heading, pitch, inc):
    headingRad = deg2Rad(heading)
    pitchRad = deg2Rad(pitch)
    x = x0 + inc * math.cos(headingRad)
    y = y0 + inc * math.sin(headingRad)
    z = z0 + inc * math.sin(pitchRad)

    return x, y, z


def main():
    print("Hello TV Land!");

    pygame.init()
    display = (screenWidth, screenHeight)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Create the window caption
    pygame.display.set_caption("OpenGL - scenery and moving around")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    myX = 0
    myY = -8
    myZ = 0
    myHeading = 90.0
    myPitch = 0.0
    gluLookAt(myX, myY, myZ, 0, 0, 0, 0, 0, 1)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()

    # Make a sphere.
    sphere = gluNewQuadric()

    # Make some terrain.
    nRows = 40
    nCols = 40
    terrain = makeTerrain(nRows, nCols)

    # Make a bullet array
    bulletExists = False
    # Show menu
    menu()

    # Main loop control
    running = True
    programTime = 0
    while running:

        # init model view matrix
        glLoadIdentity()

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        """ Check for keyboard presses. """
        key = pygame.key.get_pressed()

        # Leave window
        if (key[pygame.K_ESCAPE] == True):
            running = False

        # Translations, forward, backwards, left, right.
        if (key[pygame.K_UP] == True):
            glTranslatef(0, 0, 0.1)
            myX, myY, myZ = updatePosition(myX, myY, myZ, myHeading, myPitch, 0.1)

        if (key[pygame.K_DOWN] == True):
            glTranslatef(0, 0, -0.1)
            myX, myY, myZ = updatePosition(myX, myY, myZ, myHeading, myPitch, -0.1)
        if (key[pygame.K_LEFT] == True):
            glTranslatef(0.1, 0, 0)
            myX, myY, myZ = updatePosition(myX, myY, myZ, myHeading + 90, myPitch, 0.1)
        if (key[pygame.K_RIGHT] == True):
            glTranslatef(-0.1, 0, 0)
            myX, myY, myZ = updatePosition(myX, myY, myZ, myHeading - 90, myPitch, 0.1)

        # Translations, up, down.
        if (key[pygame.K_PAGEUP] == True):
            glTranslatef(0, -0.1, 0)
            myZ = myZ + 0.1
        if (key[pygame.K_PAGEDOWN] == True):
            glTranslatef(0, 0.1, 0)
            myZ = myZ - 0.1

        # Rotate left, right.
        if (key[pygame.K_a] == True):
            glRotatef(-0.3, 0, 1, 0)
            myHeading = myHeading + 0.3
        if (key[pygame.K_d] == True):
            glRotatef(0.3, 0, 1, 0)
            myHeading = myHeading - 0.3

        # Pitch nose down, nose up
        if (key[pygame.K_s] == True):
            glRotatef(0.3, 1, 0, 0)
            myPitch = myPitch - 0.3
        if (key[pygame.K_w] == True):
            glRotatef(-0.3, 1, 0, 0)
            myPitch = myPitch + 0.3

        if (key[pygame.K_SPACE] == True):
            print("my position: ", myX, myY, myZ)
            myBullet = bullet(myX, myY, myZ, myHeading, myPitch, 0.4)
            bulletExists = True

        # Game logic and moving.
        if (bulletExists):
            myBullet.moveMe()

        # Drawing

        # multiply the current matrix by the get the new view matrix and store the final view matrix
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        """ --- Drawing code should go here. """
        setColor(MAGENTA)

        glPushMatrix()

        # drawFloor(-20, -20, 20, 20, 40)
        # drawFloor_In_polygons(-20, -20, 20, 20, 40)
        drawTerrainPolygons(-20, -20, 20, 20, nRows, nCols, terrain)

        hiddenLineTest(sphere, 0, 5, 5)

        if (bulletExists == True):
            myBullet.drawMe()

        glPopMatrix()

        """ --- Go ahead and update the screen with what we've drawn. """
        pygame.display.flip()

        # Update program time.
        programTime = programTime + 1

        """ --- Limit to 24 frames per second. """
        clock.tick(24)

    pygame.quit()


main()