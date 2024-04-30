# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 18:48:50 2023

@author: patrick

pacMan maze builder
"""

import pygame, sys
import numpy

user_input = False

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLUE = (0, 0, 255)

class grid:
    def __init__(self, x0, y0, scaleFactor, nCols, nRows, x_pixels, y_pixels):
        self.x0 = x0
        self.xMax = x0 + (scaleFactor * (nCols * x_pixels))
        self.y0 = y0
        self.yMax = y0 + (scaleFactor * (nRows * y_pixels))
        self.scaleFactor = scaleFactor
        self.nCols = nCols
        self.nRows = nRows
        self.x_pixels = x_pixels
        self.y_pixels = y_pixels
        return
    
    def drawMe(self, screen):
        drawGrid(screen, self.scaleFactor, self.nRows, self.nCols, 
                 self.x_pixels, self.y_pixels, self.x0, self.y0)
        return
    
    def isMouseInGrid(self, mx, my):
        inThere = False
        if (((mx >= self.x0) and (mx <= self.xMax)) and
            ((my >= self.y0) and (my <= self.yMax))):
            inThere = True
        return inThere
    
    def get_mouse_rowAndCol(self, mx, my):
        mCol = int((mx - self.x0)/(self.x_pixels * self.scaleFactor))
        mRow = int((my - self.y0)/(self.y_pixels * self.scaleFactor))
        return mRow, mCol
        

class textLineObject():
    def __init__(self, x0, y0, font_size, myMessage, textColor, backGroundColor):
        self.x = x0
        self.y = y0
        self.message = myMessage
        self.font_size = font_size
        self.textColor = textColor
        self.backGroundColor = backGroundColor
        # Make a program status display.
        font = pygame.font.Font("freesansbold.ttf", font_size)
        text = font.render(self.message, True, textColor, backGroundColor)
        textRect = text.get_rect()
        textRect.topleft = (self.x, self.y)
        
        self.messageBox = text
        self.messageLocation = textRect
        return
    
    def drawMe(self, screen):
        screen.blit(self.messageBox, self.messageLocation)
        return
    
    def setMessage(self, myMessage):
        self.message = myMessage
        font = pygame.font.Font("freesansbold.ttf", self.font_size)
        text = font.render(self.message, True, self.textColor, self.backGroundColor)
        textRect = text.get_rect()
        textRect.topleft = (self.x, self.y)
        
        self.messageBox = text
        self.messageLocation = textRect
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

def drawGrid(screen, scaleFactor, nRows, nCols, x_size, y_size, x0, y0):
    width = x_size * scaleFactor
    height = y_size * scaleFactor
    x = x0
    y = y0
    for j in range(nRows):
        x = x0
        for k in range(nCols):
            # Make a rectangle.
            rect = pygame.Rect(x, y, width, height)
            # Draw it
            pygame.draw.rect(screen, ORANGE, rect, width = 1)
            # Increment x
            x = x + width
        y = y + height
        
    return

def saveTileMap(fileName, tiles, nRows, nCols):
    out = open(fileName, "w")
    out.write(str(nRows))
    out.write("\n")
    out.write(str(nCols))
    out.write("\n")
    
    for j in range(nRows):
        for k in range(nCols):
            out.write(str(tiles[j][k]))
            out.write(" ")
        out.write("\n")
    out.close()
    return
    


# Pygame setup.
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])

# Set caption on window frame
pygame.display.set_caption("Pac Man maze builder")

# Snag the maze parts sprite sheet.
fileName = "Arcade - Pac-Man - Maze Parts.png"
tileSheet = pygame.image.load(fileName)
# Show the size of the sheet
size = tileSheet.get_size()
width = int(size[0])
height = int(size[1])
print("tileSheet size is: ", width, height)

# Get pixel locations from the user - will need to read these off a pixel edit program.
if (user_input):
    x_start, y_start = input("Enter the pixel location where the tiles start, x and y.").split()
    x_start = int(x_start)
    y_start = int(y_start)
    tile_group_width, tile_group_height = input("Enter the width and height of the tile group. (144 by 27 is a good start. ").split()
    tile_group_width = int(tile_group_width)
    tile_group_height = int(tile_group_height)
else:
    x_start = 225
    y_start = 0
    tile_group_width = 144
    tile_group_height = 27




# Snag the parts sprites from the maze parts image.
mazeParts = get_pixels_at(x_start, y_start, tile_group_width, tile_group_height,
                          tileSheet)

# Get tiles from maze parts, start at 0, 0, typical read is 8 by 8, skip border
# of one, read 8 by 8.  Do this 16 times.
tiles = []
nRows = 3
tiles_per_row = 16
x = 0
y = 0
xinc = 9
yinc = 9
x_size = 8
y_size = 8
scaleFactor = 6
for j in range(nRows):
    x = 0
    for k in range(tiles_per_row):
        mySprite = get_pixels_at(x, y, x_size, y_size, mazeParts)
        scaledSprite = rescale_Sprite(mySprite, scaleFactor)
        tiles.append(scaledSprite)
        x = x + xinc
        
        y = y
    y = y+yinc
    
# Draw the pallete into a surface.
pallette_width = tiles_per_row * x_size * scaleFactor
pallette_height = nRows * y_size * scaleFactor
palletteImage = pygame.Surface([pallette_width, pallette_height])
# Draw the tile pallet from the sprite sheet to the palletteImage.
xSpot = 0
ySpot = 0
j = 0
for t in tiles:
    palletteImage.blit(t, [xSpot, ySpot])
    xSpot = xSpot + (x_size*scaleFactor)
    j = j+1
    if ((j % tiles_per_row) == 0):
        xSpot = 0
        ySpot = ySpot + (y_size*scaleFactor)

# Make a grid object to hold the pallet.    
palletGrid = grid(0, 0, scaleFactor, tiles_per_row, nRows, x_size, y_size)
# Make a grid object to hold the game layer.
gameWidth_in_tiles = 20
gameHeight_in_tiles = 12
# Make a grid object to hold the game layer data.
xSpot = 0
ySpot = ((nRows+1) * y_size) * scaleFactor   
gameGrid = grid(xSpot, ySpot, scaleFactor, gameWidth_in_tiles, gameHeight_in_tiles,
                x_size, y_size)

# Make a surface to hold the game layer image.
gameSufaceWidth = scaleFactor * (gameWidth_in_tiles * x_size)
gameSurfaceHeight = scaleFactor * (gameHeight_in_tiles * y_size)
myGameSurface = pygame.Surface((gameSufaceWidth, gameSurfaceHeight))
myGameSurface.fill(MAGENTA)

# Make a program text displays.
x_left = (tiles_per_row + 1) * x_size * scaleFactor
y_left = 0
font_size = 20
welcomeMessage = textLineObject(x_left, y_left, font_size, "Welcome to the Sprite Layer Builder", GREEN, BLUE)
statusMessage = textLineObject(x_left, y_left + (2*font_size), font_size, "No sprite selected", GREEN, BLACK)

# Create a 2D aray to hold the tile map.
tile_map = numpy.zeros((gameHeight_in_tiles, gameWidth_in_tiles), dtype = int)
# Default fill the array with -1's to indicate no filled array cells
for j in range(gameHeight_in_tiles):
    for k in range(gameWidth_in_tiles):
        tile_map[j][k] = -1
    
running = True
pallette_select = False
while(running):
    # Handle events
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
            
        if (event.type == pygame.MOUSEBUTTONDOWN):
            print("pressed mouse button down!")
            # Find mouse position.
            mx, my = pygame.mouse.get_pos()
            # Determine if mouse is in pallette grid, game grid, or somewhere else.
            inPalletteGrid = palletGrid.isMouseInGrid(mx, my)
            if (inPalletteGrid == True):
                print("Mouse is in pallette grid!!!!")
                # Find the row and column that the mouse is in.
                mRow, mCol = palletGrid.get_mouse_rowAndCol(mx, my)
                print("Mouse's (row, col) position is ", mRow, ", ", mCol)
                # Translate row and col to array index of tiles.
                tile_number = (mRow * tiles_per_row) + mCol
                # Get the tile pixels.
                myTile = tiles[tile_number]
                # Set boolean to indicate tile is selected.
                pallette_select = True
                # Set status bar to indicate tile has been selected.
                statusMessage.setMessage("Sprite      Selected")
            elif (gameGrid.isMouseInGrid(mx, my) == True):
                print("Mouse is in game grid!!!!")
                # Find the row and column that the mouse is in.
                mRow, mCol = gameGrid.get_mouse_rowAndCol(mx, my)
                print("Mouse's (row, col) position is ", mRow, ", ", mCol)
                if (pallette_select == True):
                    # Place earlier selected tile to the game grid in row, col position.
                    myTileRectSpot = pygame.Rect(mCol*x_size*scaleFactor, mRow*y_size*scaleFactor,
                                                 x_size*scaleFactor, y_size*scaleFactor)
                    myGameSurface.blit(myTile, myTileRectSpot)
                    # Set status bar to indicate sprite has been placed.
                    statusMessage.setMessage("Sprite  put  in  grid")
                    # Place index of tile into the tile_map array
                    tile_map[mRow][mCol] = tile_number
            else:
                print("Mouse is not in a grid!")
                pallette_select = False
                # Set status bar to indicate tile has been selected.
                statusMessage.setMessage("No sprite selected.")
                    
            
    key = pygame.key.get_pressed()
    if (key[pygame.K_ESCAPE]  == True):
        running = False
    if (key[pygame.K_UP] == True): 
        pass
    if (key[pygame.K_DOWN] == True): 
        pass
    if (key[pygame.K_LEFT] == True):
        pass
    if (key[pygame.K_RIGHT] == True):
        pass
    if (key[pygame.K_SPACE] == True):
        pass
        
    
    # Game logic
    
    
    # Draw 
    
    # Draw the tile pallet from the sprite sheet to the screen.
    screen.blit(palletteImage, [0, 0])

    # Draw a grid to seperate the tiles. 
    palletGrid.drawMe(screen)
    
    # Draw the game surface
    screen.blit(myGameSurface, [gameGrid.x0, gameGrid.y0])
    
    # Draw the game grid
    gameGrid.drawMe(screen)
    
    # Draw the program status text.
    welcomeMessage.drawMe(screen)
    statusMessage.drawMe(screen)
    
    
    
    # Put surface to video memory
    pygame.display.flip()
    # Make sure we get 60 or frames per second
    clock.tick(60)
    
    
# Save the things we made.
saveTileMap("tileMap.txt", tile_map, gameHeight_in_tiles, gameWidth_in_tiles)
pygame.image.save(palletteImage, "myGamePallette.png")
pygame.image.save(myGameSurface, "myGameSurface.png")

pygame.quit()
sys.exit()