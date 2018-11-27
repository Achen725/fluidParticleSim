from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import OpenGL
import numpy as np
import pygame
import random
import copy
import math

class System(object):
    def __init__(self):
        self.particles = []
        self.particleRects = []
        self.wall = []
        self.paused = True
        self.placing = "water"
        self.blockPic = pygame.image.load("sand.png")
        self.waterPic = pygame.image.load("water.png")

    def newBoard(self):
        self.particles = []
        self.solidBlocks = []
        self.paused = True
        self.placing = "water"

class Particle(object):
    def __init__(self, image):
        self.speed = 1
        self.mass = 5
        self.r = 4
        self.velocity = (0, 0)
        self.pos = image.get_rect()
        self.floor = False
        #True is right, False is left
        self.direction = random.choice([True,False])

    # def checkValid(self, size):
    #     if

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
    while not p.pos.right % 15 == 0:
        p.pos = p.pos.move(-1,0)
    while not p.pos.bottom % 15 == 0:
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
        #pygame.draw.circle(screen, blue, p.pos,8)

def pushParticles(mousePos, sim):
    for p in sim.particles:
        if (p.pos[0], p.pos[1]) == mousePos:
            randX = random.choice([-15,0,15])
            p.pos = p.pos.move(randX,15)
        elif (p.pos[0]-15 == mousePos[0] or p.pos[0] + 15 == mousePos[0]):
            if True:
                p.pos = p.pos.move(-15,15)
                p.direction = False
            else:
                p.direction = True
                p.pos = p.pos.move(15,15)

def update(sim,display):
    if not sim.paused:
        updatedParticles = []
        waterRect = getWaterRect(sim.particles)

        # for p in sim.particles:
        #     print(p.pos)
        #     if not p.floor:
        #         p.pos = p.pos.move(0,15)
        #         if p.pos[1] >= display[1] - 30:
        #             p.floor = True
        #             updatedParticles.append(p)
        #         elif p.pos.collidelist(sim.wall) < 0 and p.pos.collidelist(waterRect) < 0:
        #             updatedParticles.append(p)
        #         else:
        #             p.pos = p.pos.move(0,-15)
        #             if p.direction:
        #                 p.pos = p.pos.move(15,0)
        #                 if p.pos.collidelist(sim.wall) < 0 and p.pos.collidelist(waterRect) < 0:
        #                     updatedParticles.append(p)
        #                 else:
        #                     p.direction = False
        #                     p.pos = p.pos.move(-15,0)
        #                     updatedParticles.append(p)
        #             else:
        #                 p.pos = p.pos.move(-15,0)
        #                 if p.pos.collidelist(sim.wall) < 0 and p.pos.collidelist(waterRect) < 0:
        #                     updatedParticles.append(p)
        #                 else:
        #                     p.pos = p.pos.move(15,0)
        #                     p.direction = True
        #                     updatedParticles.append(p)
        #     else:
        #         if p.direction:
        #             p.pos = p.pos.move(15,0)
        #             if p.pos.collidelist(sim.wall) < 0 and p.pos.collidelist(waterRect) < 0  and p.pos[0] < display[0] - 30:
        #                 updatedParticles.append(p)
        #             else:
        #                 p.pos = p.pos.move(-15,0)
        #                 p.direction = False
        #                 updatedParticles.append(p)
        #         else:
        #             p.pos = p.pos.move(-15,0)
        #             if p.pos.collidelist(sim.wall) < 0 and p.pos.collidelist(waterRect) < 0  and p.pos[0] > -30:
        #                 updatedParticles.append(p)
        #             else:
        #                 p.pos = p.pos.move(15,0)
        #                 p.direction = True
        #                 updatedParticles.append(p)
        #
        #     if p.direction and (p.pos.move(15,0).collidelist(sim.wall):
        #
        #
        #
        # sim.particles = updatedParticles

def mainLoop():
    pygame.init()
    display = (500,500)
    screen = pygame.display.set_mode(display)
    clock = pygame.time.Clock()
    delay = 5
    sim = System()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
            elif event.type == pygame.MOUSEMOTION and sim.placing == "force":
                mousePos = pygame.mouse.get_pos()
                pushParticles(mousePos,sim)
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if sim.placing == "wall":
                sim.wall = placeItem(pos, sim.wall,sim.particles,sim.blockPic)
            elif sim.placing == "water":
                sim.particles = placeFluid(pos, sim.particles, sim.wall, sim.waterPic)

        update(sim,display)
        render(screen,sim)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
	mainLoop()
