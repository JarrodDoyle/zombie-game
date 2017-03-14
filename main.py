import pygame
import sys
from random import randint
from classes import *
from level import *


pygame.init()
clock = pygame.time.Clock()
FPS = 60
SCREENSIZE = SCREENWIDTH, SCREENHEIGHT = 1000, 800
screen = pygame.display.set_mode(SCREENSIZE)


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)

gameState = "running"

wallColour = (218, 212, 94)

def generateLevel():
    level = Level((50, 40), "w", " ")
    placeAllEntities(level)
    return level.board

def loadLevel(objects, zombies, fileName):
    fileHandle = open(fileName, "r")
    level = []
    for y in range(int(SCREENHEIGHT / 20)):
        fileRow = fileHandle.readline()
        levelRow = []
        for x in range(int(SCREENWIDTH / 20)):
            char = fileRow[x]
            
def buildLevel(level, objects, zombies, player):
     for y in range(len(level)):
         for x in range(len(level[y])):
            char = level[y][x]
            
            if char == "w":
                obj = Object(x * 20, y * 20, wallColour, 20, 20)
                objects.append(obj)

            elif char == "z":
                obj = Zombie(x * 20, y * 20, 1, 1, green, 5, 5)
                zombies.append(obj)

            elif char == "p":
                player.x = x * 20
                player.y = y * 20
                


player = Player(2, 2, red, 10, 10)
objects = []
zombies = []

#loadLevel(objects, zombies, "testLevel.txt")
level = generateLevel()
buildLevel(level, objects, zombies, player)

redraw = True

while gameState != "exit":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameState = "exit"
    
    player.move(screen)
    
    for i in zombies:
        i.move(player, screen)
    
    screen.fill(black)
    for i in objects:
        screen.blit(i.surface, (i.x, i.y))

    screen.blit(player.surface, (player.x, player.y))
    
    for i in zombies:
        screen.blit(i.surface, (i.x, i.y))

    player.shoot(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
