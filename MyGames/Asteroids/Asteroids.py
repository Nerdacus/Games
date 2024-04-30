import pygame as p
import random
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
NeonBlue = (50, 50, 255)

colorPalette = [WHITE, RED, ORANGE, YELLOW, CYAN, MAGENTA, NeonBlue]
nColors = len(colorPalette)

screenWidth = 1200
screenHeight = 800

gameMidX = screenWidth / 2
gameMidY = screenHeight / 2

# General constants and variables defined.
# Space rock variables.
maxRockVelocity = 2
maxRockScaleFactor = 40
maxRockTypes = 3

rock0 = [[[1, 1], [1, -1], [-1, -1], [-1, 1], [1, 1]]]
rock1 = [[[1, 2], [3, 1], [3, -1], [1, -2], [-1, -2],
          [-3, -1], [-3, 1], [-1, 2], [1, 2]]]
rock2 = [[[1, 1], [1, 0], [1, -1], [-2, -1], [-2, 1], [1, 1]]]
rock3 = [[[0, 1], [-1, 0], [1, 0], [0, 1]]]  # triangle

spaceRocks = rock0 + rock1 + rock2
nRockTypes = len(spaceRocks)
nAsteroids = 5

maxExplodeCount = 30
maxMissileCount = 100
maxShootingDelay = 30
maxFFDelay = 300
maxIFrameTime = 120
mCount = 5
active_asteroids = nAsteroids

basicShip = [[2, 0], [0, 3], [6, 0], [0, -3], [2, 0], [6, 0]]

# Utility functions.

def orientXY(x0, y0):
    x = x0
    y = screenHeight - y0
    return x, y

def deg2Rad(degrees):
    rad = (math.pi / 180.0) * degrees
    return rad

def getDist(x0, y0, x1, y1):
    dist = (x1 - x0) ** 2 + (y1 - y0) ** 2
    dist = math.sqrt(dist)
    return dist

def rotatePoint(xc, yc, x, y, deg):
    currentAng = math.atan2(y - yc, x - xc)
    angRad = deg2Rad(deg)
    totalAng = currentAng + angRad
    dist = getDist(xc, yc, x, y)
    xNew = xc + math.cos(totalAng) * dist
    yNew = yc + math.sin(totalAng) * dist

    return xNew, yNew

def boxes_intersect(box1, box2):
    # Check x and y ranges
    return (box1[0] < box2[2] and box1[2] > box2[0] and
            box1[1] < box2[3] and box1[3] > box2[1])

# Objects.
class spaceRock:
    def __init__(self):
        self.x = random.randint(0, screenWidth - 1)
        self.y = random.randint(0, screenHeight - 1)
        self.heading = random.randint(0, 359)
        self.xVel = random.randint(-maxRockVelocity, maxRockVelocity)
        self.yVel = random.randint(-maxRockVelocity, maxRockVelocity)
        self.scaleFactorX = random.randint(1, maxRockScaleFactor)
        self.scaleFactorY = random.randint(1, maxRockScaleFactor)
        index = random.randint(0, nRockTypes - 1)
        self.myPoints = spaceRocks[index]

        # Find center of rotation.
        xSum = ySum = 0
        for myPoint in self.myPoints:
            xSum = xSum + myPoint[0]
            ySum = ySum + myPoint[1]

        self.xc = xSum / len(self.myPoints)
        self.yc = ySum / len(self.myPoints)

        # Find a bounding box for this asteroid.
        xs = []
        ys = []
        for myPoint in self.myPoints:
            x = myPoint[0]
            y = myPoint[1]
            # Rotate and scale these points.
            xr, yr = rotatePoint(self.xc, self.yc, x, y, self.heading)
            xScale = xr * self.scaleFactorX
            yScale = yr * self.scaleFactorY
            xs.append(xScale)
            ys.append(yScale)

        self.minX = min(xs)
        self.maxX = max(xs)
        self.minY = min(ys)
        self.maxY = max(ys)

        index = random.randint(0, nColors - 1)
        self.color = colorPalette[index]

        self.isActive = True

    def moveMe(self):
        # Calculate new positon of space rock based on it's velocity.
        self.x = self.x + self.xVel
        self.y = self.y + self.yVel

        # If rock is outside of game space wrap it to other side.
        if (self.x < 0):
            self.x = screenWidth - 1
        elif (self.x > screenWidth):
            self.x = 0

        if (self.y < 0):
            self.y = screenHeight - 1
        elif (self.y > screenHeight):
            self.y = 0

        return

    def drawMe(self, screen):
        if (self.isActive):
            points = []
            for myPoint in self.myPoints:
                # Get coords of point.
                x0 = float(myPoint[0])
                y0 = float(myPoint[1])

                # Rotate the point.
                myRadius = getDist(self.xc, self.yc, x0, y0)
                theta = math.atan2(y0 - self.yc, x0 - self.xc)
                radAng = deg2Rad(self.heading)
                xr = self.xc + myRadius * math.cos(radAng + theta)
                yr = self.yc + myRadius * math.sin(radAng + theta)

                # Scale.
                xs = xr * self.scaleFactorX
                ys = yr * self.scaleFactorY

                # Translate.
                xt = xs + self.x
                yt = ys + self.y

                # Orient to 0,0 being upper left.
                x, y = orientXY(xt, yt)

                # Put point into polygon point list.
                points.append([x, y])

            p.draw.polygon(screen, self.color, points, width=2)
        return

    def checkCollision(self, x, y):
        smack = False
        if ((x >= self.minX + self.x) and (x <= self.maxX + self.x)):
            if ((y >= self.minY + self.y) and (y <= self.maxY + self.y)):
                smack = True
                global active_asteroids
                active_asteroids -= 1
        return smack

class BossAsteroid(spaceRock):
    # Spacerock but bigger and with health element added
    def __init__(self):
        super().__init__()
        self.scaleFactorX = 100
        self.scaleFactorY = 100
        self.health = 200
        self.max_health = 200

    def drawMe(self, screen):
        if self.isActive:
            super().drawMe(screen)

    def checkCollision(self, x, y):
        smack = False

        # Increase collision bounding box size to allow for better collision detection
        bbox_pad = 90
        minX = self.minX - bbox_pad
        maxX = self.maxX + bbox_pad
        minY = self.minY - bbox_pad
        maxY = self.maxY + bbox_pad

        if (x >= self.x + minX and
                x <= self.x + maxX and
                y >= self.y + minY and
                y <= self.y + maxY):
            smack = True

        return smack

class bullet:
    def __init__(self, x0, y0, heading, radius, velocity):
        self.x = x0
        self.y = y0
        self.heading = heading
        self.radius = radius
        self.velocity = velocity
        self.isActive = True
        self.exploding = False
        self.explodeCount = 20

    def drawMe(self, surface, color):
        # Draw active bullets.
        if (self.isActive == True):
            x0 = self.x
            y0 = self.y
            x, y = orientXY(x0, y0)
            center = [x, y]

            if (self.exploding):
                p.draw.circle(surface, color, center, self.explodeCount)
                self.explodeCount = self.explodeCount + 1
                if (self.explodeCount == maxExplodeCount):
                    self.isActive = False
            else:
                p.draw.circle(surface, color, center, self.radius, width=0)

    def moveMe(self):
        if ((self.isActive) and (self.exploding == False)):
            # Calculate new positon of bullet based on it's velocity.
            radAng = deg2Rad(self.heading)
            self.x = self.x + self.velocity * math.cos(radAng)
            self.y = self.y + self.velocity * math.sin(radAng)
            # If bullet is outside of game space set it to inactive.
            if ((self.x < 0) or (self.x > screenWidth)):
                self.isActive = False
            elif ((self.y < 0) or (self.y > screenHeight)):
                self.isActive = False
        return

    def setExplosion(self):
        self.exploding = True

class spaceShip:
    def __init__(self, x0, y0, heading0, scaleFactor0, points):
        self.x = x0
        self.y = y0
        self.heading = heading0
        self.scaleFactor = scaleFactor0
        self.forcefield = None

        # Find center of rotation.
        xSum = ySum = 0
        for myPoint in points:
            xSum = xSum + myPoint[0]
            ySum = ySum + myPoint[1]

        self.xc = xSum / len(points)
        self.yc = ySum / len(points)

        self.gunSpot = []
        self.gunX = 0
        self.gunY = 0

        return

    def setGunSpot(self, gunSpot):
        self.gunSpot = gunSpot
        return

    def getGunSpot(self):
        return self.gunX, self.gunY

    def initializeForcefield(self):
        # Assign a Forcefield instance
        self.forcefield = Forcefield(self)

    def moveMe(self, inc):
        # Move ship along current course.
        radAng = deg2Rad(self.heading)
        self.x = self.x + inc * math.cos(radAng)
        self.y = self.y + inc * math.sin(radAng)
        # If ship goes out of screen, wrap it other side.
        if (self.x < 0):
            self.x = screenWidth - 1
        elif (self.x > screenWidth):
            self.x = 0

        if (self.y < 0):
            self.y = screenHeight - 1
        elif (self.y > screenHeight):
            self.y = 0

        return

    def drawMe(self, screen, color, myShip):
        points = []
        isTheGunSpot = False
        for myPoint in myShip:
            if (myPoint == self.gunSpot):
                isTheGunSpot = True

            # Get coords of point.
            x0 = float(myPoint[0])
            y0 = float(myPoint[1])

            # Rotate the point.
            myRadius = getDist(self.xc, self.yc, x0, y0)
            theta = math.atan2(y0 - self.yc, x0 - self.xc)
            radAng = deg2Rad(self.heading)
            xr = self.xc + myRadius * math.cos(radAng + theta)
            yr = self.yc + myRadius * math.sin(radAng + theta)

            # Scale.
            xs = xr * self.scaleFactor
            ys = yr * self.scaleFactor

            # Translate.
            xt = xs + self.x
            yt = ys + self.y

            # Save gun position.
            if (isTheGunSpot == True):
                self.gunX = xt
                self.gunY = yt
                isTheGunSpot = False

            # Orient to 0,0 being upper left.
            x, y = orientXY(xt, yt)

            # Put point into polygon point list.
            points.append([x, y])

        p.draw.polygon(screen, color, points, width=2)
        return

    def turn(self, inc):
        self.heading = self.heading + inc

        if (self.heading > 359):
            self.heading = 0
        elif (self.heading < 0):
            self.heading = 359
        return

class missile:  # Bigger than a bullet, but slower
    def __init__(self, x0, y0, heading, radius, velocity):
        self.x = x0
        self.y = y0
        self.heading = heading
        self.radius = radius
        self.velocity = velocity
        self.isActive = True
        self.exploding = False
        self.explodeCount = 20
        self.timer = 80

    def drawMe(self, surface, color):
        if (self.isActive is True):
            x0 = self.x
            y0 = self.y
            x, y = orientXY(x0, y0)
            center = [x, y]

            if (self.exploding):
                p.draw.circle(surface, color, center, self.explodeCount)
                self.explodeCount = self.explodeCount + 1
                if (self.explodeCount == maxMissileCount):
                    self.isActive = False
            else:
                p.draw.circle(surface, color, center, self.radius, width=0)

    def moveMe(self):
        if ((self.isActive) and (self.exploding == False)):
            # Calculate position of missile based on velocity
            radAng = deg2Rad(self.heading)
            self.x = self.x + self.velocity * math.cos(radAng)
            self.y = self.y + self.velocity * math.sin(radAng)
            # If missile leaves, set it to inactive
            if ((self.x < 0) or (self.x > screenWidth)):
                self.isActive = False
            elif ((self.y < 0) or (self.y > screenHeight)):
                self.isActive = False

            # Decrease the timer
            self.timer -= 1
            # If the timer reaches zero, trigger the explosion
            if self.timer <= 0:
                self.setExplosion()

    def checkCollision(self, asteroid):
        dist = getDist(self.x, self.y, asteroid.x, asteroid.y)
        if dist < (self.radius + max(asteroid.scaleFactorX, asteroid.scaleFactorY)):
            return True
        return False

    def setExplosion(self):
        self.exploding = True

class Forcefield:  # Forcefield around ship, will deflect asteroids into random directions
    def __init__(self, ship):
        self.ship = ship
        self.radius = 50
        self.x = ship.x
        self.y = ship.y
        self.isActive = False

    def draw(self, screen):
        x0 = self.ship.x + 15
        y0 = self.ship.y

        x, y = orientXY(x0, y0)
        center = [x, y]

        p.draw.circle(screen, GREEN,
                      (x, y),
                      self.radius, 5)

    def get_area(self):
        x1 = self.ship.x - self.radius
        x2 = self.ship.x + self.radius
        y1 = self.ship.y - self.radius
        y2 = self.ship.y + self.radius

        return (x1, y1, x2, y2)

def asteroidMe():
    # Initialize pygame.
    p.init()

    # Set the width and height of the screen [width, height]
    size = (screenWidth, screenHeight)
    screen = p.display.set_mode(size)

    p.display.set_caption("asteroidMe()")

    # Set up random number generator.
    random.seed()

    # Loop until the user clicks the close button.
    running = True

    # Used to manage how fast the screen updates
    clock = p.time.Clock()

    # Set up some game objects.
    # Spaceship stuff.
    initialHeading = 90
    scaleFactor = 6
    ship = spaceShip(gameMidX, gameMidY, initialHeading, scaleFactor, basicShip)
    ship.forcefield = Forcefield(ship)
    shipSpeed = 5
    ship.setGunSpot([6, 0])
    score = 0

    # Bullet stuff
    bullets = []
    bulletSize = int(0.5 * scaleFactor)
    bulletSpeed = 3 * shipSpeed
    shotCount = 0
    ffCount = 0

    # Missile stuff
    missiles = []
    missileSize = int(2.5 * scaleFactor)
    missileSpeed = 1.2 * shipSpeed

    # Make some asteroids - that is space rocks.
    myAsteroids = []
    for j in range(nAsteroids):
        myAsteroids.append(spaceRock())

    # Clock/game frame things.
    tickTock = 0
    lives = 5
    iFrameTimer = 0
    mCount = 5

    # Gun shooting bar
    charging_time = 0
    max_charging_time = maxShootingDelay
    charging_speed = 1
    charging_timer = 0

    # Boosting bar
    boost_time = 0
    max_boost_time = 120
    boost_charge = 1
    boost_charging_timer = 0
    can_boost = True

    # Font stuff
    font = p.font.Font(None, 32)
    flash_count = 0
    final_display_timer = 0
    final_display_time = 180

    # Boss stuff
    boss = None
    boss_spawned = False
    win_message = font.render(f"You win!", True, WHITE)

    # -------- Main Program Loop -----------
    while running:
        # --- Main event loop
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        """ Check for keyboard presses. """
        key = p.key.get_pressed()

        # Handle keypresses.
        if (key[p.K_ESCAPE] is True):
            running = False
        if (key[p.K_UP] or key[p.K_w] is True):
            if (key[p.K_b] is True and boost_time > 0 and can_boost):
                ship.moveMe(shipSpeed * 2)
                boost_time -= 2
            else:
                ship.moveMe(shipSpeed)
        if (key[p.K_DOWN] or key[p.K_s] is True):
            ship.moveMe(-.5 * shipSpeed)
        if (key[p.K_LEFT] or key[p.K_a] is True):
            ship.turn(3)
        if (key[p.K_RIGHT] or key[p.K_d] is True):
            ship.turn(-3)
        if (key[p.K_f]):
            ship.forcefield.isActive = True
        if (key[p.K_x]):
            ship.forcefield.isActive = False
        if (key[p.K_SPACE] is True and shotCount == 0 and charging_time == max_charging_time):
            gunX, gunY = ship.getGunSpot()
            myBullet = bullet(gunX, gunY, ship.heading, bulletSize, bulletSpeed)
            bullets.append(myBullet)
            shotCount = maxShootingDelay
            charging_time = 0
        if (key[p.K_m] is True and shotCount == 0 and mCount != 0):
            gunX, gunY = ship.getGunSpot()
            myMissile = missile(gunX, gunY, ship.heading, missileSize, missileSpeed)
            missiles.append(myMissile)
            shotCount = maxShootingDelay
            mCount -= 1
            charging_time = 0
        # --- Game logic should go here
        # Move bullets, missiles, and asteroids.
        for b in bullets:
            b.moveMe()

        for a in myAsteroids:
            a.moveMe()

        for m in missiles:
            m.moveMe()

        # Check to see if a bullet hit an asteroid.
        for a in myAsteroids:
            for b in bullets:
                if (a.isActive and b.isActive and not boss):
                    smacked = a.checkCollision(b.x, b.y)
                    if (smacked == True):
                        b.setExplosion()
                        if a.color == RED:
                            score += 5
                        elif a.color == ORANGE:
                            score += 10
                        elif a.color == MAGENTA:
                            score += 15
                        elif a.color == WHITE:
                            score += 20
                        elif a.color == CYAN:
                            score += 25
                        elif a.color == NeonBlue:
                            score += 30
                        elif a.color == YELLOW:
                            score += 35
                        a.isActive = False

        for a in myAsteroids:
            for b in bullets:
                if (a.isActive and b.isActive and boss):
                    smacked = boss.checkCollision(b.x, b.y)
                    if smacked == True:
                        b.setExplosion()
                        boss.health -= random.randint(10, 20)
                        b.isActive = False
                    if boss.health <= 0:
                        print("You win!")
                        boss.isActive = False
                        score += 1000

        for a in myAsteroids:
            for m in missiles:
                if (a.isActive and m.isActive and not boss):
                    smacked = a.checkCollision(m.x, m.y)
                    if (smacked == True):
                        m.setExplosion()
                        if a.color == RED:
                            score += 10
                        elif a.color == ORANGE:
                            score += 20
                        elif a.color == MAGENTA:
                            score += 30
                        elif a.color == WHITE:
                            score += 40
                        elif a.color == CYAN:
                            score += 50
                        elif a.color == NeonBlue:
                            score += 60
                        elif a.color == YELLOW:
                            score += 70
                        a.isActive = False

        for a in myAsteroids:
            for m in missiles:
                if (a.isActive and m.isActive and boss):
                    smacked = boss.checkCollision(m.x, m.y)
                    if smacked == True:
                        m.setExplosion()
                        boss.health -= random.randint(25, 50)
                        m.isActive = False
                    if boss.health <= 0:
                        print("You win!")
                        score += 750
                        boss.isActive = False

        # Forcefield hit, reflects asteroid to random direction
        for a in myAsteroids:
            if (a.isActive and ship.forcefield.isActive):
                ff_area = ship.forcefield.get_area()
                asteroid_box = (a.x + a.minX, a.y + a.minY,
                                a.x + a.maxX, a.y + a.maxY)
                if boxes_intersect(ff_area, asteroid_box):
                    a.xVel = random.randint(-1, 1)
                    a.yVel = random.randint(-1, 1)
                    ship.forcefield.isActive = False

        # If asteroid hits ship, take one life away, print in console, activate 2 sec of I frames
        for a in myAsteroids:
            if (a.isActive and ship.forcefield.isActive is False):
                smacked = a.checkCollision(ship.x, ship.y)
                if (smacked and iFrameTimer == 0):
                    iFrameTimer = maxIFrameTime
                    print("Hit")
                    if not boss:
                        lives -= 1
                        a.isActive = False
                        score += 5
                    else:
                        lives -= 2
                        lucky = random.randint(1, 100)
                        if lucky > 95:
                            boss.health -= 500
                        else:
                            boss.health -= 5
                        # boss.health -= random.randint(1,10)
                        if boss.health <= 0:
                            print("You win!")
                            score += 10000
                            boss.isActive = False

                    print("Lives remaining:", lives)
                smacked = False

        charging_timer += 1
        if charging_timer >= charging_speed:
            charging_time += 1
            charging_timer = 0

        if charging_time >= max_charging_time:
            charging_time = max_charging_time

        boost_charging_timer += 1
        if boost_charging_timer >= boost_charge:
            boost_time += boost_charge
            if boost_time > max_boost_time:
                boost_time = max_boost_time
            boost_charging_timer = 0

        if flash_count < 30:
            flash_color = RED
        else:
            flash_color = BLACK

        flash_count = (flash_count + 1) % 60

        if (lives <= 0):
            print("Game over")
            running = False

        shipSpeed = 3 if ship.forcefield.isActive is True else 5
        # --- Screen-clearing code goes here
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)

        if mCount != 0:
            missile_text = font.render(f"Missiles: {mCount}", True, WHITE)
        else:
            missile_text = font.render(f"Out of Missiles", True, flash_color)

        if lives > 1:
            lives_text = font.render(f"Lives: {lives}", True, WHITE)
        else:
            lives_text = font.render(f"Final Life", True, flash_color)

        score_text = font.render(f"Score: {score}", True, WHITE)
        if active_asteroids <= 0:
            final_display_timer += 1
            if final_display_timer >= 0 and final_display_timer < final_display_time:
                final_text = font.render(f"Final Boss Approaching", True, flash_color)
                screen.blit(final_text, (500, 400))
            if (final_display_timer == final_display_time and not boss_spawned):
                boss = BossAsteroid()
                myAsteroids.append(boss)
                if boss.isActive:
                    boss_spawned == True
                    boss_health_width = (boss.health / boss.max_health) * 100
                    boss_health_rect = p.Rect(1090, 80, boss_health_width, 15)
                    p.draw.rect(screen, RED, boss_health_rect)

        screen.blit(missile_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(score_text, (10, 90))

        if boss and not boss.isActive:
            final_score = score
            final_message = font.render(f"Final Score: {final_score}", True, WHITE)
            screen.blit(win_message, (550, 400))
            screen.blit(final_message,(510, 435))

        charging_bar_width = (charging_time / max_charging_time) * 100
        charging_bar_rect = p.Rect(1090, 10, charging_bar_width, 15)

        boosting_bar_width = (boost_time / max_boost_time) * 100
        boost_bar_rect = p.Rect(1090, 30, boosting_bar_width, 15)

        p.draw.rect(screen, GREEN, charging_bar_rect)
        p.draw.rect(screen, CYAN, boost_bar_rect)

        if boss:
            boss_text = font.render(f"Boss Health: ", True, WHITE)
            if not boss.isActive:
                boss_text = font.render(f"Boss Health: ", True, BLACK)
            screen.blit(boss_text, (400, 765))
            boss_health_width = (boss.health / boss.max_health) * 100
            boss_health_rect = p.Rect(555, 760, boss_health_width, 30)
            p.draw.rect(screen, RED, boss_health_rect)

        if boss and not boss.isActive:
            boss_text = font.render(f"Boss Health: ", True, BLACK)
            screen.blit(boss_text, (400, 765))

        # --- Drawing code should go here

        # Flashing spaceship if hit
        if (iFrameTimer % 6 == 0):
            hitColor = GREEN
        else:
            hitColor = BLACK
        ship.drawMe(screen, hitColor, basicShip)

        # Bullets
        for b in bullets:
            b.drawMe(screen, RED)

        # Asteroids
        for a in myAsteroids:
            a.drawMe(screen)

        for m in missiles:
            m.drawMe(screen, RED)

        if (ship.forcefield.isActive):
            ship.forcefield.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        p.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

        # Update frame count.
        tickTock = tickTock + 1

        # Implement shooting delay to keep bullet count lower.
        if (shotCount > 0):
            shotCount = shotCount - 1
        # Forcefield timer, can only activate every 5 seconds
        if (ffCount > 0):
            ffCount = ffCount - 1
            # Invincibility frames = 2 seconds after getting hit
        if (iFrameTimer > 0):
            iFrameTimer = iFrameTimer - 1

        # Do some bookkeeping on arrays.
        # Remove inactive elements of bullets array.
        # Remove inactive elements of asteroids array.

    # Close the window and quit.
    p.quit()

    return

asteroidMe()