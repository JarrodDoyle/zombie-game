import pygame
import sys
from random import randint
from classes import *
from level import *


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60
SCREENSIZE = SCREENWIDTH, SCREENHEIGHT = 1000, 800
screen = pygame.display.set_mode(SCREENSIZE)
font = pygame.font.SysFont("Arial", 24)


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

def startNewGame():
    player = Player(2, 2, red, 10, 10)
    objects = []
    zombies = []
    bullets = []
    level = generateLevel()
    buildLevel(level, objects, zombies, player)
    return level, objects, zombies, player, bullets

winText = font.render("All zombies are dead. You Win.", True, (0, 0, 0))
loseText = font.render("A zombie killed you.", True, (0, 0, 0))

#loadLevel(objects, zombies, "testLevel.txt")

startGame = True
redraw = True

while gameState != "exit":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameState = "exit"

    if startGame:
        level, objects, zombies, player, bullets = startNewGame()
        win = True
        startGame = False
    
    if len(zombies) > 0:

        screen.fill(black)

        for i in objects:
            screen.blit(i.surface, (i.x, i.y))
        
        for i in zombies:
            screen.blit(i.surface, (i.x, i.y))

        for i in bullets:
            screen.blit(i.surface, (int(i.x), int(i.y)))

        screen.blit(player.surface, (player.x, player.y))
        
        player.move(screen)
        
        for i in zombies:
            collide = i.move(player, screen)
            if collide == "die":
                zombies.pop(zombies.index(i))

        for i in bullets:
            collide = i.move(screen)
            if collide:
                bullets.pop(bullets.index(i))

        if player.shoot():
            bullet = Bullet(player.x + (player.width - 4) // 2, player.y + (player.height - 4) // 2, pygame.mouse.get_pos(), (0, 0, 255), 4, 4, 5)
            bullets.append(bullet)

        if not player.alive:
            zombies = []
            win = False

    else:
        screen.fill((255, 0, 0))

        if win:
            text = winText
        else:
            text = loseText
            
        screen.blit(text, (SCREENWIDTH // 2 - text.get_width() // 2, SCREENHEIGHT // 2 - text.get_height() // 2))

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            startGame = True
    
        
        

    pygame.display.flip()
    clock.tick(FPS)

pygame.font.quit()
pygame.quit()
sys.exit()
