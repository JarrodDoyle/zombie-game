import pygame

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

    def shoot(self, screen):
        mx, my = pygame.mouse.get_pos()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (mx, my), 5)

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
