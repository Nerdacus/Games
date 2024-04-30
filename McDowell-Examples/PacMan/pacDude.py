# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 09:09:53 2023

@author: pm


This is a first shot at a pacMan game that uses the layers built by the simple 
layer maker program.


"""

import pygame, sys

# Pallette constants
pallette_rows = 3
pallette_cols = 16

# Places pacMan can go:
canGoThere = [44, 45, 46, 47]

# Sprite constants
sprite_width = 48
sprite_height = 48

# Movement constants
moveInc = 3

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

class Player(pygame.sprite.Sprite):
    def __init__(self, filename_base, pos_x, pos_y, nSprites, sprite_width, sprite_height):
        super().__init__()
        # Turn animate off.
        self.is_animating = False
        
        # Load sprites groups.
        # Right sprites.
        fileR = filename_base + "R.png"
        rightSprites = self.loadExtraSprites(fileR, nSprites, sprite_width, sprite_height)
        self.rightSprites = rightSprites
        self.sprites = rightSprites
        
        # Left Sprites.
        fileL = filename_base + "L.png"
        leftSprites = self.loadExtraSprites(fileL, nSprites, sprite_width, sprite_height)
        self.leftSprites = leftSprites
    
        # Up Sprites.
        fileU = filename_base + "U.png"
        upSprites = self.loadExtraSprites(fileU, nSprites, sprite_width, sprite_height)
        self.upSprites = upSprites
        
        # Down Sprites.
        fileU = filename_base + "D.png"
        downSprites = self.loadExtraSprites(fileU, nSprites, sprite_width, sprite_height)
        self.downSprites = downSprites
        
            
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        print("sprite rect = ", self.rect)
        self.x = pos_x
        self.y = pos_y
        self.rect.topleft = [pos_x, pos_y]
        
        self.mode = 'r'
        
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
        if (self.mode != 'r'):
            self.mode = 'r'
            self.sprites = self.rightSprites
        self.x = self.x + moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_left(self):
        if (self.mode != 'l'):
            self.mode = 'l'
            self.sprites = self.leftSprites
        self.x = self.x - moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_up(self):
        if (self.mode != 'u'):
            self.mode = 'u'
            self.sprites = self.upSprites
        
        self.y = self.y - moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_down(self):
        if (self.mode != 'd'):
            self.mode = 'd'
            self.sprites = self.downSprites
        self.y = self.y + moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def get_sprite(self, sprite_index):
        return self.sprites[sprite_index]
    
    def add_sprite(self, mySprite):
        self.sprites.append(mySprite)
        return
    
    def loadExtraSprites(self, filename, nSprites, sprite_width, sprite_height):
        # Get the image from the file.
        spriteSheet = pygame.image.load(filename)
        
        # Load the sprites
        extra_sprites = []
        y = 0
        x = 0
        for j in range(nSprites):
            pixels = get_pixels_at(x, y, sprite_width, sprite_height, spriteSheet)
            extra_sprites.append(pixels)
            x = x + sprite_width
            
        return extra_sprites
    
    
    def getSprites(self, filename, nSprites, sprite_width, sprite_height):
        # Get the image from the file.
        spriteSheet = pygame.image.load(filename)
        
        # Load the sprites
        self.sprites = []
        y = 0
        x = 0
        for j in range(nSprites):
            pixels = get_pixels_at(x, y, sprite_width, sprite_height, spriteSheet)
            self.sprites.append(pixels)
            x = x + sprite_width
            
        return
    
    def saveSprites(self, fileName, spriteWidth, spriteHeight):
        # Make a surface to hold the game layer image.
        spriteSufaceWidth = spriteWidth * len(self.sprites)
        spriteSurfaceHeight = spriteHeight
        mySpriteSurface = pygame.Surface((spriteSufaceWidth, spriteSurfaceHeight))
        
        # Blit the sprites to the surface.
        x = 0
        y = 0
        for sprite in self.sprites:
            mySprite = pygame.transform.scale(sprite, [spriteWidth, spriteHeight])
            mySpriteSurface.blit(mySprite, [x, y])
            x = x + spriteWidth
            
        # Save the surface as .png
        pygame.image.save(mySpriteSurface, fileName)
        return
    
class grid:
    def __init__(self, x0, y0, nCols, nRows, x_pixels, y_pixels):
        self.x0 = x0
        self.xMax = x0 + (nCols * x_pixels)
        self.y0 = y0
        self.yMax = y0 + (nRows * y_pixels)
        self.nCols = nCols
        self.nRows = nRows
        self.x_pixels = x_pixels
        self.y_pixels = y_pixels
        return
    
    def drawMe(self, screen):
        drawGrid(screen, self.nRows, self.nCols, 
                 self.x_pixels, self.y_pixels, self.x0, self.y0)
        return
    
    def isMouseInGrid(self, mx, my):
        inThere = False
        if (((mx >= self.x0) and (mx <= self.xMax)) and
            ((my >= self.y0) and (my <= self.yMax))):
            inThere = True
        return inThere
    
    def get_mouse_rowAndCol(self, mx, my):
        mCol = int((mx - self.x0)/self.x_pixels)
        mRow = int((my - self.y0)/self.y_pixels)
        return mRow, mCol
    
    def getPacManrowAndCol(self, mx, my):
        # Note that mx, my are at the upper left
        # corner of the sprite, we want to know
        # where the middle of the sprite is.
        myX = mx + self.x_pixels/2
        myY = my + self.y_pixels/2
        mCol = int((myX - self.x0)/self.x_pixels)
        mRow = int((myY - self.y0)/self.y_pixels)
        return mRow, mCol
    
    
def drawGrid(screen, nRows, nCols, x_size, y_size, x0, y0):
    x = x0
    y = y0
    for j in range(nRows):
        x = x0
        for k in range(nCols):
            # Make a rectangle.
            rect = pygame.Rect(x, y, x_size, y_size)
            # Draw it
            pygame.draw.rect(screen, ORANGE, rect, width = 1)
            # Increment x
            x = x + x_size
        y = y + y_size
        
    return

def readTilemapFile(filename):
    f = open(filename, "r")
    nRows = int(f.readline())
    nCols = int(f.readline())
    print("nRows = ", nRows, " nCols = ", nCols)
    tilemap = []
    
    for j in range(nRows):
        myLine = f.readline()
        myNumbers = []
        myNumbers = myLine.split()
        row = []
        for stringX in myNumbers:
            x = int(stringX)
            row.append(x)
        tilemap.append(row)
        
    print("tileMap = ", tilemap)
            
    return nRows, nCols, tilemap

def get_pixels_at(x, y, width, height, image0):
    rect = pygame.Rect(x, y, width, height)
    pixels = pygame.Surface((width, height))
    pixels.blit(image0, (0, 0), rect)
    
    return pixels

def loadTiles(filename, nRows, nCols):
    # Get the image from the file.
    tileSheet = pygame.image.load(filename)
    # Show the size of the sheet
    size = tileSheet.get_size()
    sheet_width = int(size[0])
    sheet_height = int(size[1])
    print("tileSheet size is: ", sheet_width, sheet_height)
    
    # Get tile dimensions.
    tile_width = sheet_width/nCols
    tile_height = sheet_height/nRows
    
    # Load the tiles.
    myPallette = []
    y = 0
    for j in range(nRows):
        myRow = []
        x = 0
        for k in range(nCols):
            pixels = get_pixels_at(x, y, tile_width, tile_height, tileSheet)
            myRow.append(pixels)
            x = x + tile_width
            
        myPallette.append(myRow)
        y = y + tile_height
        
    return myPallette, tile_width, tile_height
            
    
    
    return tileSheet

def showPallette(screen, x0, y0, pixelTiles, nRows, nCols, tile_width, tile_height):
    x = x0
    y = y0
    for j in range(nRows):
        for k in range(nCols):
            myTile = pixelTiles[j][k]
            myRect = pygame.Rect(x, y, tile_width, tile_height)
            screen.blit(myTile, myRect)
            x = x + tile_width
        y = y + tile_height
        x = x0
        
    return

def showGame(screen, x0, y0, tilemap, nRows, nCols, pixelTiles, tile_width, tile_height):
    x = x0
    y = y0
    for j in range(nRows):
        for k in range(nCols):
            tileNumber = tilemap[j][k]
            tRow = int(tileNumber/pallette_cols)
            tCol = tileNumber - (tRow * pallette_cols)
            myTile = pixelTiles[tRow][tCol]
            myRect = pygame.Rect(x, y, tile_width, tile_height)
            screen.blit(myTile, myRect)
            x = x + tile_width
        y = y + tile_height
        x = x0
        
    return

def canIgoThatWay(myRow, myCol, nRows, nCols, direction, tilemap):
    canDo = False
    print("myRow = ", myRow, " myCol = ", myCol, " direction = ", direction)
    if (direction == "up"):
        upRow = myRow - 1
        if (upRow >= 0):
            print("tilemap value = ", tilemap[upRow][myCol])
            if (tilemap[upRow][myCol] in canGoThere):
                canDo = True
    elif (direction == "down"):
        downRow = myRow + 1
        if (downRow < nRows):
            if (tilemap[downRow][myCol] in canGoThere):
                canDo = True
    elif (direction == "left"):
        leftCol = myCol - 1
        if (leftCol >= 0):
            if (tilemap[myRow][leftCol] in canGoThere):
                canDo = True
    elif (direction == "right"):
        rightCol = myCol + 1
        if (rightCol < nCols):
            if (tilemap[myRow][rightCol] in canGoThere):
                canDo = True
                
    return canDo
            
    
    
    
def pacDude(tileFile, palletteFile, gameFile):
    nRows, nCols, tilemap = readTilemapFile(tileFile)
    pixelTiles, tile_width, tile_height = loadTiles(palletteFile, pallette_rows, pallette_cols)
    
    # Pygame setup.
    pygame.init()
    clock = pygame.time.Clock()
    
    # Game Screen
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode([screen_width, screen_height])
    
    # Upper left corner of game.
    x0 = 3 * tile_width
    y0 = 3 * tile_height
    
    # Set caption on window frame
    pygame.display.set_caption("PacDude!")
    
    # Create grid for location and mapping purposes.
    gameGrid = grid(x0, y0, nCols, nRows, tile_width, tile_height)
    
    # Make a pacMan.
    pacMan = Player("pacMan", 9 * sprite_width, 4 * sprite_height, 3, sprite_width, sprite_height)
    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(pacMan)
    pacMan.animate_me()
    
    running = True
    direction = None
    count = 0

    while(running):
        # Handle events
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
                
            if (event.type == pygame.MOUSEBUTTONDOWN):
                pass
                        
        key = pygame.key.get_pressed()
        if (key[pygame.K_ESCAPE]  == True):
            running = False
        
        # This may look odd, but we are checking for user input at one tile 
        # intervals so that pacman does not get out of a row or column. 
        if ((count % 48) == 0):
            if (key[pygame.K_UP] == True): 
                direction = "up"
            if (key[pygame.K_DOWN] == True): 
                direction = "down"
            if (key[pygame.K_LEFT] == True):
                direction = "left"
            if (key[pygame.K_RIGHT] == True):
                direction = "right"
            
        if (key[pygame.K_SPACE] == True):
            pass
        
        
        
        # Game logic
        # Handle keyboard input for pacman's movement.  Check at one tile
        # intervals.
        if ((count % 48) == 0):
            myRow, myCol = gameGrid.getPacManrowAndCol(pacMan.x, pacMan.y) 
            go = canIgoThatWay(myRow, myCol, nRows, nCols, direction, tilemap)

        if (go == True):
            if (direction == "up"):
                pacMan.move_up()
            elif (direction == "down"):
                pacMan.move_down()
            elif (direction == "right"):
                pacMan.move_right()
            elif (direction == "left"):
                pacMan.move_left()
       
        # Draw the tile pallet from the sprite sheet to the screen.
        showGame(screen, x0, y0, tilemap, nRows, nCols, pixelTiles, tile_width, tile_height)
        gameGrid.drawMe(screen)
        
        # Draw characters.
        moving_sprites.update(.10)
        moving_sprites.draw(screen)
        
        # Put surface to video memory
        pygame.display.flip()
        # Make sure we get 60 or frames per second
        clock.tick(60)
        
        # Update count for keyboard consistency.
        count = count + moveInc
        
    pygame.quit()
    sys.exit()
    
    

pacDude("tileMap1.txt", "myGamePallette1.png", "baff")