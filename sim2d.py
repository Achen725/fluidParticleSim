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
        self.blockLst = []
        self.spongeLst = []
        self.dubLst = []
        self.display = (600,600)
        self.paused = True
        self.mode = "normal"
        self.floorLevel = self.display[0]
        self.placing = "water"
        self.noBuckets = True
        self.bucketLoc = None
        self.blockPic = pygame.image.load("ground.png")
        self.waterPic = pygame.image.load("water.png")
        self.bucket = pygame.image.load("bucket.png")
        self.collect = pygame.image.load("dub.png")
        self.block = pygame.image.load("block.png")
        self.sponge = pygame.image.load("sponge.png")

    def getPos(self):
        lst = []
        for p in self.particles:
            lst.append((p.pos[0],p.pos[1]))
        return lst
    def newBoard(self):
        self.particles = []
        self.wall = []
        self.blockLst = []
        self.spongeLst = []
        self.dubLst = []
        self.noBuckets = True
        self.bucketLoc = None
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
        check1 = self.pos.move(-5,0).collidelist(sim.wall) < 0
        check2 = self.pos.move(5,0).collidelist(sim.wall) < 0
        if check1 or check2:
            return True
        return False

def applyForce(p,sim,waterRect):
    part = p.pos
    while part[0] != sim.display[0] - 15 and part.move(5,0).collidelist(sim.wall) < 0\
        and part.move(5,0).collidelist(waterRect) < 0:
        part = p.pos.move(5,0)
        if part.collidelist(waterRect) < 0 and part.collidelist(sim.wall) < 0:
            p.pos = p.pos.move(5,0)
        elif p.pos.move(-5,0).collidelist(waterRect) < 0 and part.collidelist(sim.wall) < 0:
            p.pos = p.pos.move(-5,0)
    #p.pos = p.pos.move(0,-5)

def getWaterRect(particleLst):
    lst = []
    for p in particleLst:
        lst.append(p.pos)
    return lst

def dubsCollide(sim,pos):
    obj = sim.collect.get_rect()
    obj.center = pos
    while not obj.right % 30 == 0:
        obj = obj.move(-1,0)
    while not obj.bottom % 30 == 0:
        obj = obj.move(0,-1)
    waterRect = getWaterRect(sim.particles)
    if len(sim.dubLst) == 0:
        if obj.collidelist(sim.wall)<0 and obj.collidelist(sim.spongeLst)<0 and\
            obj.collidelist(sim.blockLst)<0 and obj.collidelist(waterRect)<0:
            if  sim.bucketLoc != None and not obj.colliderect(sim.bucketLoc):
                sim.dubLst.append(obj)
            else:
                sim.dubLst.append(obj)
    else:
        if obj.collidelist(sim.wall)<0 and obj.collidelist(sim.spongeLst)<0 and\
            obj.collidelist(sim.blockLst)<0 and obj.collidelist(waterRect)<0\
            and obj.collidelist(sim.dubLst)<0 and len(sim.dubLst) <= 3:
            if  sim.bucketLoc != None and not obj.colliderect(sim.bucketLoc):
                sim.dubLst.append(obj)
            else:
                sim.dubLst.append(obj)

def bucketsCollide(sim,pos):
    obj = sim.bucket.get_rect()
    obj.center = pos
    while not obj.right % 80 == 0:
        obj = obj.move(-1,0)
    while not obj.bottom % 80 == 0:
        obj = obj.move(0,-1)
    waterRect = getWaterRect(sim.particles)
    if obj.collidelist(sim.wall)<0 and obj.collidelist(sim.spongeLst)<0\
        and obj.collidelist(sim.blockLst) < 0 and obj.collidelist(waterRect)<0 \
        and obj.collidelist(sim.dubLst) < 0 and sim.noBuckets:
        sim.bucketLoc = obj
        sim.noBuckets = False

def placeItem(sim,pos,blockType, otherType, blockPic, type):
    block = blockPic.get_rect()
    block.center = pos
    while not block.right % 15 == 0:
        block = block.move(-1,0)
    while not block.bottom % 15 == 0:
        block = block.move(0,-1)
    waterRect = getWaterRect(otherType)
    if block.collidelist(blockType)<0 and block.collidelist(sim.spongeLst) and \
        block.collidelist(sim.blockLst) and block.collidelist(waterRect) < 0:
        if type == "sponge":
            sim.spongeLst.append(block)
        elif type == "block":
            sim.blockLst.append(block)
        else:
            blockType.append(block)
            sim.wall = blockType

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
    for sponge in sim.spongeLst:
        screen.blit(sim.sponge, sponge)
    for block in sim.blockLst:
        screen.blit(sim.block, block)
    if sim.bucketLoc != None:
        screen.blit(sim.bucket, sim.bucketLoc)
    for dub in sim.dubLst:
        screen.blit(sim.collect,dub)

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
            if p.pos.collidelist(sim.spongeLst) >= 0:
                sim.particles.remove(p)
                continue
            if p.pos.collidelist(sim.dubLst) >= 0:
                sim.dubLst.remove(sim.dubLst[p.pos.collidelist(sim.dubLst)])
                continue

            if not p.floor:
                p.pos = p.pos.move(0,5)
                if p.pos[1] == sim.floorLevel-5 and \
                    p.pos.collidelist(waterRect) < 0:
                    p.floor = True
                elif (p.pos.collidelist(sim.wall)<0 and p.pos.collidelist(sim.blockLst)<0) \
                    and p.pos.collidelist(waterRect)<0:
                    pass
                else:
                    p.pos = p.pos.move(0,-5)
                    if p.direction:
                        p.pos = p.pos.move(5,0)
                        if p.pos.collidelist(waterRect) < 0 and \
                            (p.pos.collidelist(sim.wall) < 0 and \
                            p.pos.collidelist(sim.blockLst) < 0) and \
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
                        if  (p.pos.collidelist(sim.wall)<0 and p.pos.collidelist(sim.blockLst)<0) \
                            and p.pos.collidelist(waterRect) < 0 and p.pos[0] > -5:
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
                    if  (p.pos.collidelist(sim.wall)<0 and p.pos.collidelist(sim.blockLst)<0) \
                        and p.pos.collidelist(waterRect) < 0 and p.pos[0] < display[0]:
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
                    if sim.mode == "normal":
                        if sim.placing == "water":
                            sim.placing = "wall"
                        else:
                            sim.placing = "water"
                    else:
                        if sim.placing == "water":
                            sim.placing = "wall"
                        elif sim.placing == "wall":
                            sim.placing = "block"
                        elif sim.placing == "block":
                            sim.placing = "sponge"
                        elif sim.placing == "sponge" and sim.noBuckets:
                            sim.placing = "bucket"
                        elif (sim.placing == "sponge" or sim.placing == "block" \
                            or sim.placing == "bucket") and len(sim.dubLst) <= 3:
                            sim.placing = "dubs"
                        else:
                            sim.placing = "water"
                if event.key == pygame.K_f:
                    sim.placing = "force"
                if event.key == pygame.K_p and sim.mode == "normal":
                    sim.paused = not sim.paused
                if event.key == pygame.K_m:
                    if sim.mode == "normal":
                        sim.mode = "builder"
                    else:
                        sim.mode = "normal"
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
                placeItem(sim,pos,sim.wall,sim.particles,sim.blockPic,sim.placing)
            elif sim.placing == "block":
                placeItem(sim,pos,sim.wall,sim.particles,sim.block,sim.placing)
            elif sim.placing == "sponge":
                placeItem(sim,pos,sim.wall,sim.particles,sim.sponge,sim.placing)
            elif sim.placing == "water":
                sim.particles = placeFluid(pos,sim.particles,sim.wall,sim.waterPic)
            elif sim.placing == "bucket":
                bucketsCollide(sim, pos)
            elif sim.placing == "dubs":
                dubsCollide(sim, pos)
            waterRect = getWaterRect(sim.particles)
            for wall in sim.wall:
                if wall.collidepoint(mousePos):
                    sim.wall.remove(wall)
            for water in range(len(waterRect)):
                if waterRect[water].collidepoint(pos):
                    sim.particles.remove(sim.particles[water])
            if mousePos.get_rect().collideslist(sim.wall) < 0 or \
                mousePos.get_rect().collideslist(sim.blockLst) < 0 or \
                mousePos.get_rect().collideslist(sim.spongeLst) < 0 or \
                mousePos.get_rect().collideslist(waterRect) < 0 or \
                mousePos.get_rect().collideslist(sim.bucket) < 0 or \
                mousePos.get_rect().collideslist(sim.dubs) < 0:
                pos = pygame.mouse.get_pos()
                for wall in sim.wall:
                    if wall.collidepoint(pos):
                        sim.wall.remove(wall)
        update(sim,display)
        render(screen,sim)
        pygame.display.flip()
def test():
    print("hi")

# if __name__ == "__main__":
# 	mainLoop()
