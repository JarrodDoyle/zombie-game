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

    def collideY(self, newY, surface):
        if newY > self.y:
            maxY = newY + self.height
            minY = maxY - (newY - self.y)
        else:
            maxY = self.y
            minY = newY
        for x in range(self.x, self.x + self.width):
            for y in range(minY, maxY):
                if surface.get_at((x, y)) != (0, 0, 0):
                    return self.y
        return newY

    def collideX(self, newX, surface):
        if newX > self.x:
            maxX = newX + self.width
            minX = maxX - (newX - self.x)
        else:
            maxX = self.x
            minX = newX
        
        for x in range(minX, maxX):
            for y in range(self.y, self.y + self.height):
                if surface.get_at((x, y)) != (0, 0, 0, 255):
                    return self.x
        return newX

class Player(Object):
    def __init__(self, dx, dy, color, width, height):
        Object.__init__(self, 0, 0, color, width, height)
        self.dx = dx
        self.dy = dy
        self.shootCounter = 0

    def shoot(self, screen):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.shootCounter % 60 == 0:
                return True
            self.shootCounter += 1

        else:
            self.shootCounter = 0
            
    def move(self, surface):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            newY = self.y - self.dy
            self.y = self.collideY(newY, surface)

        elif keys[pygame.K_s]:
            newY = self.y + self.dy
            self.y = self.collideY(newY, surface)

        if keys[pygame.K_a]:
            newX = self.x - self.dx
            self.x = self.collideX(newX, surface)

        elif keys[pygame.K_d]:
            newX = self.x + self.dx
            self.x = self.collideX(newX, surface)


class Zombie(Object):
    def __init__(self, x, y, dx, dy, color, width, height):
        Object.__init__(self, x, y, color, width, height)
        self.dx = dx
        self.dy = dy
        
    def move(self, player, surface):
        if player.x > self.x:
            newX = self.x + self.dx
            self.x = self.collideX(newX, surface)
            
        elif player.x < self.x:
            newX = self.x - self.dx
            self.x = self.collideX(newX, surface)
            
        if player.y > self.y:
            newY = self.y + self.dy
            self.y = self.collideY(newY, surface)
           
        elif player.y < self.y:
            newY = self.y - self.dy
            self.y = self.collideY(newY, surface)

class Bullet(Object):
    def __init__(self, x, y, mousePos, color, width, height, velocity):
        self.velocity = velocity
        self.getAngle((x, y), mousePos)
        self.getSpeeds(velocity)
        Object.__init__(self, x, y, color, width, height)


    
    # DOESNT WORK

    def getAngle(self, bulletPos, mousePos):
        x1, y1 = bulletPos
        x2, y2 = mousePos

        x, y = (x2 - x1, y2 - y1)

        if x > 0:
            if y > 0:
                self.angle = atan(x / y)
            else:
                self.angle = 0.5 * pi + atan(-y / x)

        else:
            if y > 0:
                self.angle = 2 * pi - atan(-x / y)
            else:
                self.angle = pi + atan(-x / -y + 1)

        print(degrees(self.angle))
        
    
    def getSpeeds(self, vel):
        if self.angle >= 0 and self.angle < 0.5 * pi:
            self.dx = vel * sin(self.angle)
            self.dy = vel * cos(self.angle)

        elif self.angle >= 0.5 * pi and self.angle < pi:
            self.dx = vel * cos(pi - self.angle)
            self.dy = -(vel * sin(pi - self.angle))

        elif self.angle >= pi and self.angle < 1.5 * pi:
            self.dx = -(vel * sin(self.angle - pi))
            self.dy = -(vel * cos(self.angle - pi))

        elif self.angle >= 1.5 * pi and self.angle < 2 * pi:
            self.dx = -(vel * sin(2 * pi - self.angle))
            self.dy = vel * cos(2 * pi - self.angle)

        else:
            print(1)
            
        

    def move(self, surface):
        newX = int(self.x + self.dx)
        newY = int(self.y + self.dy)

        self.x = self.collideX(newX, surface)
        self.y = self.collideY(newY, surface)
