from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL
import numpy as np
import pygame
import random
import copy
import math
import launch
import game

# water movement inspired by http://usingpython.com/pygame-images/
# and terraria movement of water https://www.youtube.com/watch?v=ZXPdI0WIvw0

class System(object):
    def __init__(self):
        self.particles = []
        self.wall = []
        self.display = (600,600)
        self.paused = True
        self.mode = "normal"
        self.floorLevel = self.display[0]
        self.placing = "water"
        self.blockPic = pygame.image.load("ground.png")
        self.waterPic = pygame.image.load("water.png")

    def getPos(self):
        lst = []
        for p in self.particles:
            lst.append((p.pos[0],p.pos[1]))
        return lst
    def newBoard(self):
        self.particles = []
        self.solidBlocks = []
        self.paused = True
        self.placing = "water"

class Particle(object):
    def __init__(self, image):
        self.size = 5
        self.force = (0, -5)
        self.pos = image.get_rect()
        self.floor = False
        #True is right, False is left
        self.direction = random.choice([True,False])
    def loneSide(self, sim):
        check1 = self.pos.move(-5,0).collidelist < 0
        check2 = self.pos.move(5,0).collidelist < 0
        if check1 or check2:
            return True
        return False

def applyForce(p,sim,waterRect):
    part = p.pos
    while part[0] != sim.display[0] - 30 and part.move(5,0).collidelist(sim.wall) < 0:
        part = p.pos.move(5,0)
        if p.pos.move(5,0).collidelist(waterRect) < 0:
            p.pos = p.pos.move(5,0)
        elif p.pos.move(-5,0).collidelist(waterRect) < 0:
            p.pos = p.pos.move(-5,0)
    p.pos = p.pos.move(0,-5)

def getWaterRect(particleLst):
    lst = []
    for p in particleLst:
        lst.append(p.pos)
    return lst

def placeItem(pos,blockType, otherType, blockPic):
    block = blockPic.get_rect()
    block.center = pos
    while not block.right % 15 == 0:
        block = block.move(-1,0)
    while not block.bottom % 15 == 0:
        block = block.move(0,-1)
    waterRect = getWaterRect(otherType)
    if block.collidelist(blockType) < 0 and block.collidelist(waterRect) < 0:
        blockType.append(block)
    return blockType

def placeFluid(pos, blockType, otherType, waterPic):
    p = Particle(waterPic)
    p.pos.center = pos
    while not p.pos.right % 5 == 0:
        p.pos = p.pos.move(-1,0)
    while not p.pos.bottom % 5 == 0:
        p.pos = p.pos.move(0,-1)
    waterRect = getWaterRect(blockType)
    if p.pos.collidelist(waterRect) < 0 and p.pos.collidelist(otherType) < 0:
        blockType.append(p)
    return blockType

def render(screen,sim):
    screen.fill((255,255,255))
    for wall in sim.wall:
        screen.blit(sim.blockPic,wall)
    for p in sim.particles:
        screen.blit(sim.waterPic, p.pos)
    myFont = pygame.font.SysFont(None, 20)
    # text for number of water blocks
    text1 = myFont.render('Water Blocks: ' + \
        str(len(sim.particles)),True, (0, 125, 235), (255, 255, 255))
    waterText = text1.get_rect()
    waterText.left = 0
    #screen.get_rect().centerx
    waterText.centery = 20
    screen.blit(text1, waterText)

def pushParticles(mousePos, sim):
    for p in sim.particles:
        if (p.pos[0], p.pos[1]) == mousePos:
            randX = random.choice([-5,0,5])
            p.pos = p.pos.move(randX,5)
        elif (p.pos[0]-5 == mousePos[0] or p.pos[0] + 5 == mousePos[0]):
            if True:
                p.pos = p.pos.move(-5,-5)
                p.direction = False
            else:
                p.direction = True
                p.pos = p.pos.move(5,-5)

def update(sim,display):
    if not sim.paused:
        waterRect = getWaterRect(sim.particles)
        for p in sim.particles:
            if not p.floor:
                p.pos = p.pos.move(0,5)
                if p.pos[1] == sim.floorLevel-5 and \
                    p.pos.collidelist(waterRect) < 0:
                    p.floor = True
                elif p.pos.collidelist(sim.wall) < 0 and \
                    p.pos.collidelist(waterRect) < 0:
                    pass
                else:
                    p.pos = p.pos.move(0,-5)
                    if p.direction:
                        p.pos = p.pos.move(5,0)
                        if p.pos.collidelist(waterRect) < 0 and \
                            p.pos.collidelist(sim.wall) < 0 and \
                            p.pos[0] < display[0]:
                            pass
                        else:
                            # if not sim.floorFilled(sim.floorLevel):
                            #     p.direction = False
                            if p.pos.collidelist(waterRect) >= 0 and \
                                p.pos.move(-5,-5).collidelist(waterRect) >= 0:
                                p.direction = False
                            p.pos = p.pos.move(-5,0)

                    else:
                        p.pos = p.pos.move(-5,0)
                        if p.pos.collidelist(sim.wall) < 0 and \
                            p.pos.collidelist(waterRect) < 0 and p.pos[0] > -5:
                            pass
                        else:
                            # if not sim.floorFilled(sim.floorLevel):
                            #     p.direction = True
                            if p.pos.collidelist(waterRect) >= 0 and \
                                p.pos.move(5,-5).collidelist(waterRect) >= 0:
                                p.direction = True
                            p.pos = p.pos.move(5,0)
            else:
                if p.direction:
                    p.pos = p.pos.move(5,0)
                    if p.pos.collidelist(sim.wall) < 0 and \
                        p.pos.collidelist(waterRect) < 0 and \
                        p.pos[0] < display[0]:
                        pass
                    else:
                        # if not sim.floorFilled(sim.floorLevel):
                        #     p.direction = False
                        if p.pos.collidelist(waterRect) >= 0 and \
                            p.pos.move(-5,-5).collidelist(waterRect) >= 0 :
                            p.direction = False
                        p.pos = p.pos.move(-5,0)

                else:
                    p.pos = p.pos.move(-5,0)
                    if p.pos.collidelist(sim.wall) < 0 and \
                        p.pos.collidelist(waterRect) < 0 and \
                        p.pos[0] > -5:
                        pass
                    else:
                        # if not sim.floorFilled(sim.floorLevel):
                        #     p.direction = True
                        if p.pos.collidelist(waterRect) >= 0 and \
                            p.pos.move(5,-5).collidelist(waterRect) >= 0:
                            p.direction = True
                        p.pos = p.pos.move(5,0)

def mainLoop():
    #pygame adapted from pygame documentation and tutorial when making 3d water
	#http://pyopengl.sourceforge.net
	#https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/
    pygame.init()
    pygame.display.set_caption('Water Simulation')
    pygame.font.init()
    myfont = pygame.font.SysFont('Monaco', 30)
    display = (600,600)
    screen = pygame.display.set_mode(display)
    sim = System()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                launch.run()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if sim.placing == "water":
                        sim.placing = "wall"
                    else:
                        sim.placing = "water"
                if event.key == pygame.K_f:
                    sim.placing = "force"
                if event.key == pygame.K_p:
                    sim.paused = not sim.paused
                if event.key == pygame.K_r:
                    sim.newBoard()
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    game.mainLoop(sim.particles,sim.wall)
                    quit()

            elif event.type == pygame.MOUSEMOTION and sim.placing == "force":
                mousePos = pygame.mouse.get_pos()
                pushParticles(mousePos,sim)
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if sim.placing == "wall":
                sim.wall = placeItem(pos, sim.wall,sim.particles,sim.blockPic)
            elif sim.placing == "water":
                sim.particles = placeFluid(pos,sim.particles,sim.wall,sim.waterPic)
        update(sim,display)
        render(screen,sim)
        pygame.display.flip()


# if __name__ == "__main__":
# 	mainLoop()
