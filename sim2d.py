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

#Purpose: Holds logic for 2d mode and stagebuilding code

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
        self.help = False
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

    # resets the board
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

# returns a list of the water particles rectangle position
def getWaterRect(particleLst):
    lst = []
    for p in particleLst:
        lst.append(p.pos)
    return lst

#places the "w" that the user collects
def dubsCollide(sim,pos):
    obj = sim.collect.get_rect()
    obj.center = pos
    while not obj.right % 15 == 0:
        obj = obj.move(-1,0)
    while not obj.bottom % 15 == 0:
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
            and obj.collidelist(sim.dubLst)<0 and len(sim.dubLst) < 3:
            if  sim.bucketLoc != None and not obj.colliderect(sim.bucketLoc):
                sim.dubLst.append(obj)
            else:
                sim.dubLst.append(obj)

# places the bucket
def bucketsCollide(sim,pos):
    obj = sim.bucket.get_rect()
    obj.center = pos
    while not obj.right % 40 == 0:
        obj = obj.move(-1,0)
    while not obj.bottom % 40 == 0:
        obj = obj.move(0,-1)
    waterRect = getWaterRect(sim.particles)
    if obj.collidelist(sim.wall)<0 and obj.collidelist(sim.spongeLst)<0\
        and obj.collidelist(sim.blockLst) < 0 and obj.collidelist(waterRect)<0 \
        and obj.collidelist(sim.dubLst) < 0 and sim.noBuckets:
        sim.bucketLoc = obj
        sim.noBuckets = False

# places ground, block, and  sponge tiles
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

# places the water
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

# draws everything in
def render(screen,sim):
    if not sim.help:
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
        myFont = pygame.font.SysFont("Monaco", 20)

        text1 = myFont.render('Water Blocks: ' + \
            str(len(sim.particles)),True, (0, 125, 235), (255, 255, 255))

        waterText = text1.get_rect()
        waterText.left = 0
        waterText.centery = 20
        screen.blit(text1, waterText)

        placingBlock = myFont.render('Placing Block: ' + \
            sim.placing,True, (0, 125, 235), (255, 255, 255))
        placeBlockLable = placingBlock.get_rect()
        placeBlockLable.left = 0
        placeBlockLable.centery = 35
        screen.blit(placingBlock, placeBlockLable)

        instructions = myFont.render('Press H for Instructions',True,(0, 125, 235),
                    (255, 255, 255))
        lableInstruct = instructions.get_rect()
        lableInstruct.right = 600
        lableInstruct.centery = 20
        screen.blit(instructions, lableInstruct)
    else:
        screen.fill((147,112,219))
        myFont = pygame.font.SysFont("Monaco", 30)
        rules1 = myFont.render("Press 's' to switch material",
            True,(230,230,250),(147,112,219))
        rules2 = myFont.render("Press 'f' to apply a force w/ mouse.Press again to revert back"
            ,True,(230,230,250),(147,112,219))
        rules3 = myFont.render("Press 'm' to switch to stagebuilding mode",
            True,(230,230,250),(147,112,219))
        rules4 = myFont.render("When in stagebuilding, you can't go back to normal build."
            ,True,(230,230,250),(147,112,219))
        rules5 = myFont.render("You will have access to more tiles. You can press 'e'"
            ,True,(230,230,250),(147,112,219))
        rules6 = myFont.render("to erase tiles. Press 'space' to switch to game mode.",
            True,(230,230,250),(147,112,219))
        rules7 = myFont.render("A bucket must be placed and all 3 'w' must be placed ",
            True,(230,230,250),(147,112,219))
        rules8 = myFont.render("to switch to game mode ",
            True,(230,230,250),(147,112,219))
        rules9 = myFont.render('Press H to resume build mode',True,(230,230,250),
                (147,112,219))

        instruct1 = rules1.get_rect()
        instruct2 = rules2.get_rect()
        instruct3 = rules3.get_rect()
        instruct4 = rules4.get_rect()
        instruct5 = rules5.get_rect()
        instruct6 = rules6.get_rect()
        instruct7 = rules7.get_rect()
        instruct8 = rules8.get_rect()
        instruct9 = rules9.get_rect()


        blitThatItem(screen, rules1, instruct1, -1)
        blitThatItem(screen, rules2, instruct2, 0)
        blitThatItem(screen, rules3, instruct3, 1)
        blitThatItem(screen, rules4, instruct4, 2)
        blitThatItem(screen, rules5, instruct5, 3)
        blitThatItem(screen, rules6, instruct6, 4)
        blitThatItem(screen, rules7, instruct7, 5)
        blitThatItem(screen, rules8, instruct8, 6)
        blitThatItem(screen, rules9, instruct9, 7)
# conserves code to draw rules
def blitThatItem(screen, rules, instruct, i):
    instruct.centerx = screen.get_rect().centerx
    instruct.centery = screen.get_rect().centery + 20*i
    screen.blit(rules, instruct)

# applies the force to particles
def pushParticles(mousePos, sim):
    waterRect = getWaterRect(sim.particles)
    display = sim.display
    for p in sim.particles:
        if p.pos.collidepoint(mousePos):
            randX = random.choice([-5,0,5])
            p.pos = p.pos.move(randX,5)
            if not (p.pos.collidelist(waterRect) < 0 and \
                (p.pos.collidelist(sim.wall) < 0 and \
                p.pos.collidelist(sim.blockLst) < 0) and \
                p.pos[0] < display[0]):
                p.pos = p.pos.move(-randX,-5)

        elif (p.pos[0]-5 == mousePos[0] or p.pos[0] + 5 == mousePos[0]):
            if p.direction:
                p.pos = p.pos.move(-5,-5)
                p.direction = False
                if not (p.pos.collidelist(waterRect) < 0 and \
                    (p.pos.collidelist(sim.wall) < 0 and \
                    p.pos.collidelist(sim.blockLst) < 0) and \
                    p.pos[0] < display[0]):
                    p.pos = p.pos.move(5,5)
            else:
                p.pos = p.pos.move(5,-5)
                p.direction = True
                if not (p.pos.collidelist(waterRect) < 0 and \
                    (p.pos.collidelist(sim.wall) < 0 and \
                    p.pos.collidelist(sim.blockLst) < 0) and \
                    p.pos[0] < display[0]):
                    p.pos = p.pos.move(-5,5)
                p.pos = p.pos.move(5,-5)
# logic for the code
# check if it can go down, if not then check left or check right
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
                elif (p.pos.collidelist(sim.wall)<0 and \
                    p.pos.collidelist(sim.blockLst)<0) \
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
                            if p.pos.collidelist(waterRect) >= 0 and \
                                p.pos.move(-5,-5).collidelist(waterRect) >= 0:
                                p.direction = False
                            p.pos = p.pos.move(-5,0)
                    else:
                        p.pos = p.pos.move(-5,0)
                        if  (p.pos.collidelist(sim.wall)<0 and \
                            p.pos.collidelist(sim.blockLst)<0) \
                            and p.pos.collidelist(waterRect) < 0 and p.pos[0] > -5:
                            pass
                        else:
                            if p.pos.collidelist(waterRect) >= 0 and \
                                p.pos.move(5,-5).collidelist(waterRect) >= 0:
                                p.direction = True
                            p.pos = p.pos.move(5,0)
            else:
                if p.direction:
                    p.pos = p.pos.move(5,0)
                    if  (p.pos.collidelist(sim.wall)<0 and \
                        p.pos.collidelist(sim.blockLst)<0) \
                        and p.pos.collidelist(waterRect) < 0 and p.pos[0] < display[0]:
                        pass
                    else:
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
                            or sim.placing == "bucket") and len(sim.dubLst) < 3:
                            sim.placing = "dubs"
                        else:
                            sim.placing = "water"
                if event.key == pygame.K_f:
                    sim.placing = "force"
                if event.key == pygame.K_h:
                    sim.help = not sim.help
                    if not sim.paused:
                        sim.paused
                if event.key == pygame.K_e and sim.mode == "builder":
                    if sim.placing != "erase":
                        sim.placing = "erase"
                    else:
                        sim.placing = "water"
                if event.key == pygame.K_p and sim.mode == "normal":
                    sim.paused = not sim.paused
                if event.key == pygame.K_m:
                    sim.mode = "builder"
                if event.key == pygame.K_r:
                    sim.newBoard()
                if event.key == pygame.K_SPACE and not sim.noBuckets \
                    and len(sim.dubLst) == 3:
                    pygame.quit()
                    game.mainLoop(sim.particles,sim.wall,sim.bucketLoc,
                        sim.spongeLst, sim.blockLst, sim.dubLst)
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
            elif sim.placing == "erase":
                if sim.bucketLoc != None and sim.bucketLoc.collidepoint(pos):
                    sim.bucketLoc = None
                    sim.noBuckets = True
                for wall in sim.wall:
                    if wall.collidepoint(pos):
                        sim.wall.remove(wall)
                for sponge in sim.spongeLst:
                    if sponge.collidepoint(pos):
                        sim.spongeLst.remove(sponge)
                for block in sim.blockLst:
                    if block.collidepoint(pos):
                        sim.blockLst.remove(block)
                for dub in sim.dubLst:
                    if dub.collidepoint(pos):
                        sim.dubLst.remove(dub)
        update(sim,display)
        render(screen,sim)
        pygame.display.flip()

# if __name__ == "__main__":
# 	mainLoop()
