import pygame
from math import pi, atan, sin, cos, degrees

class Object:
    def __init__(self, x, y, color, width, height):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)

    def move(self, surface):
        return False

    def collideY(self, newY, surface, blockedObjects):
        if newY > self.y:
            maxY = newY + self.height
            minY = maxY - (newY - self.y)
        else:
            maxY = self.y
            minY = newY
        for x in range(self.x, self.x + self.width):
            for y in range(minY, maxY):
                if surface.get_at((x, y)) in blockedObjects:
                    return self.y, surface.get_at((x, y))
        return newY, None

    def collideX(self, newX, surface, blockedObjects):
        if newX > self.x:
            maxX = newX + self.width
            minX = maxX - (newX - self.x)
        else:
            maxX = self.x
            minX = newX
        
        for x in range(minX, maxX):
            for y in range(self.y, self.y + self.height):
                if surface.get_at((x, y)) in blockedObjects:
                    return self.x, surface.get_at((x, y))
        return newX, None

class Player(Object):
    def __init__(self, dx, dy, color, width, height):
        Object.__init__(self, 0, 0, color, width, height)
        self.dx = dx
        self.dy = dy
        self.shootCounter = 0
        self.alive = True

    def shoot(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.shootCounter += 1
            if self.shootCounter % 8 == 0:
                self.shootCounter = 0
                return True
        else:
            self.shootCounter = 0

            
    def move(self, surface):
        blockedObjects = [(218, 212, 94)]
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            newY = self.y - self.dy
            self.y, colX = self.collideY(newY, surface, blockedObjects)

        elif keys[pygame.K_s]:
            newY = self.y + self.dy
            self.y, colX = self.collideY(newY, surface, blockedObjects)

        if keys[pygame.K_a]:
            newX = self.x - self.dx
            self.x, colY = self.collideX(newX, surface, blockedObjects)

        elif keys[pygame.K_d]:
            newX = self.x + self.dx
            self.x, colY = self.collideX(newX, surface, blockedObjects)


class Zombie(Object):
    def __init__(self, x, y, dx, dy, color, width, height):
        Object.__init__(self, x, y, color, width, height)
        self.dx = dx
        self.dy = dy
        
    def move(self, player, surface):
        blockedObjects = [(218, 212, 94), (255, 0, 0), (0, 255, 0), (0, 0, 255)]

        colX = None
        colY = None

        if player.x > self.x:
            newX = self.x + self.dx
            self.x, colX = self.collideX(newX, surface, blockedObjects)
            
        elif player.x < self.x:
            newX = self.x - self.dx
            self.x, colX = self.collideX(newX, surface, blockedObjects)
            
        if player.y > self.y:
            newY = self.y + self.dy
            self.y, colY = self.collideY(newY, surface, blockedObjects)
           
        elif player.y < self.y:
            newY = self.y - self.dy
            self.y, colY = self.collideY(newY, surface, blockedObjects)
            
        if colX == blockedObjects[3] or colY == blockedObjects[3]:
            return "die"

        if colX == blockedObjects[1] or colY == blockedObjects[1]:
            player.alive = False

class Bullet(Object):
    def __init__(self, x, y, mousePos, color, width, height, velocity):
        self.velocity = velocity
        self.getAngle((x, y), mousePos)
        self.getSpeeds(velocity)
        Object.__init__(self, x, y, color, width, height)

    def getAngle(self, bulletPos, mousePos):
        x1, y1 = bulletPos
        x2, y2 = mousePos

        x, y = (x2 - x1, y2 - y1)

        if x > 0:
            if y < 0:
                self.angle = atan(x / -y)
            else:
                self.angle = 0.5 * pi + atan(y / x)

        else:
            if y <= 0:
                if x == 0:
                    self.angle = 2 * pi
                else:
                    self.angle = 1.5 * pi + atan(-y / -x)
            else:
                self.angle = pi + atan(-x / y)        
    
    def getSpeeds(self, vel):
        if self.angle > 0 and self.angle <= 0.5 * pi:
            self.dx = vel * sin(self.angle)
            self.dy = -(vel * cos(self.angle))

        elif self.angle > 0.5 * pi and self.angle <= pi:
            self.dx = vel * cos(self.angle - 0.5 * pi)
            self.dy = vel * sin(self.angle - 0.5 * pi)

        elif self.angle > pi and self.angle <= 1.5 * pi:
            self.dx = -(vel * sin(self.angle - pi))
            self.dy = vel * cos(self.angle - pi)

        elif self.angle > 1.5 * pi and self.angle <= 2 * pi:
            self.dx = -(vel * sin(2 * pi - self.angle))
            self.dy = -(vel * cos(2 * pi - self.angle))

    def move(self, surface):
        blockedObjects = [(218, 212, 94), (0, 255, 0)]
        
        newX = self.x + self.dx
        newY = self.y + self.dy

        self.x, colX = self.collideX(int(newX), surface, blockedObjects)
        self.y, colY = self.collideY(int(newY), surface, blockedObjects)

        if colX in blockedObjects or colY in blockedObjects:
            return True
