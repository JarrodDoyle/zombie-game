import pygame
import sys
from random import randint
from classes import *


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


def loadLevel(objects, zombies, fileName):
    fileHandle = open(fileName, "r")
    for y in range(int(SCREENHEIGHT / 20)):
        row = fileHandle.readline()
        for x in range(int(SCREENWIDTH / 20)):
            char = row[x]
            if char == "w":
                obj = Object(x * 20, y * 20, wallColour, 20, 20)
                objects.append(obj)

            elif char == "z":
                obj = Zombie(x * 20, y * 20, 1, 1, green, 10, 10)
                zombies.append(obj)


player = Player(100, 100, 3, 3, red, 20, 20)
objects = []
zombies = []

loadLevel(objects, zombies, "testLevel.txt")

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
