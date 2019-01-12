from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL
import numpy as np
import pygame
import random
import copy
import math
import maps
import launch

# water movement inspired by http://usingpython.com/pygame-images/
# and terraria movement of water https://www.youtube.com/watch?v=ZXPdI0WIvw0

# Purpose: Facilitates game capabilities and is the game mode method that is
# launched

class System(object):
    def __init__(self):
        self.particles = []
        self.wall = []
        self.blockLst = []
        self.spongeLst = []
        self.dubLst = []
        self.display = (600,600)
        self.floorLevel = self.display[0]
        self.removable = 150
        self.paused = False
        self.bucketLoc = None
        self.gameWon = False
        self.amountInBucket = 0
        self.winningAmount = int(len(self.particles)//2)
        self.blockPic = pygame.image.load("ground.png")
        self.waterPic = pygame.image.load("water.png")
        self.bucket = pygame.image.load("bucket.png")
        self.collect = pygame.image.load("dub.png")
        self.block = pygame.image.load("block.png")
        self.sponge = pygame.image.load("sponge.png")
        self.collectHit1 = 0
        self.collectHit2 = 0
        self.collectHit3 = 0

class Particle(object):
    def __init__(self, image):
        self.size = 5
        self.force = (0, -5)
        self.pos = image.get_rect()
        self.floor = False
        #True is right, False is left
        self.direction = random.choice([True,False])

# get the list of rectangles that represent water
def getWaterRect(particleLst):
    lst = []
    for p in particleLst:
        lst.append(p.pos)
    return lst

# draws everything
def render(screen,sim):
    # if the game is won go immediately to congratulations
    if sim.gameWon:
        screen.fill((0,125,200))
        myFont = pygame.font.SysFont("Monaco", 40)
        winStatement = myFont.render('Congratulations! You Win',True,(255,255,255))
        winLable = winStatement.get_rect()
        winLable.centerx = screen.get_rect().centerx
        winLable.centery = screen.get_rect().centery
        screen.blit(winStatement,winLable)
    else:
        if not sim.paused:
            screen.fill((255,255,255))
            for wall in sim.wall:
                screen.blit(sim.blockPic,wall)
            for p in sim.particles:
                screen.blit(sim.waterPic, p.pos)
            for sponge in sim.spongeLst:
                screen.blit(sim.sponge, sponge)
            for block in sim.blockLst:
                screen.blit(sim.block, block)
            for dub in sim.dubLst:
                screen.blit(sim.collect,dub)
            if sim.bucketLoc == None:
                sim.bucketLoc = pygame.Rect(screen.get_rect().centerx-40,
                                                sim.display[0]-60,80,80)
            else:
                screen.blit(sim.bucket, sim.bucketLoc)

            myFont = pygame.font.SysFont("Monaco", 20)
            # text for number of water blocks
            text1 = myFont.render('Water Blocks: ' + \
                str(len(sim.particles)),True, (0, 0, 0), (255, 255, 255))
            waterText = text1.get_rect()
            waterText.left = 0
            waterText.centery = 20

            waterInBucket = myFont.render('Water in Bucket: ' + \
                str(sim.amountInBucket),True, (0, 0, 0), (255, 255, 255))
            bucketText = waterInBucket.get_rect()
            bucketText.left = 0
            bucketText.centery = 35
            # text for number of s allowed to remove (Game mode only)
            text2 = myFont.render('Block Allowed to Remove Blocks: ' + \
            str(sim.removable),True, (0, 0, 0), (255, 255, 255))
            blockText = text2.get_rect()
            blockText.left = 0
            blockText.centery = 50
            text3 = myFont.render('Press H For Help and Instructions',
                                True, (0, 0, 0), (255, 255, 255))
            instruction = text3.get_rect()
            instruction.right = sim.display[0]
            instruction.centery = 20
            screen.blit(text1, blockText)
            screen.blit(text2, waterText)
            screen.blit(waterInBucket, bucketText)
            screen.blit(text3, instruction)
        else:
            screen.fill((147,112,219))
            myFont = pygame.font.SysFont("Monaco", 30)
            rules1 = myFont.render('Objective:Get half of the starting water in the bucket',
                    True,(230,230,250),(147,112,219))
            rules2 = myFont.render("and also collect all the Dubs in order to win!"
                ,True,(230,230,250),(147,112,219))
            rules3 = myFont.render('Click the mouse to erase the ground tiles (brown).You'
                    ,True,(230,230,250),(147,112,219))
            rules4 = myFont.render(" can not break the black tiles, but they behave like ground"
                ,True,(230,230,250),(147,112,219))
            rules5 = myFont.render("The sponge tiles(yellow) absorb water so avoid "
                ,True,(230,230,250),(147,112,219))
            rules6 = myFont.render('them if possible',True,(230,230,250),
                    (147,112,219))
            rules7 = myFont.render('Press H to resume the game',True,(230,230,250),
                    (147,112,219))

            instruct1 = rules1.get_rect()
            instruct2 = rules2.get_rect()
            instruct3 = rules3.get_rect()
            instruct4 = rules4.get_rect()
            instruct5 = rules5.get_rect()
            instruct6 = rules6.get_rect()
            instruct7 = rules7.get_rect()

            blitThatItem(screen, rules1, instruct1, -1)
            blitThatItem(screen, rules2, instruct2, 0)
            blitThatItem(screen, rules3, instruct3, 1)
            blitThatItem(screen, rules4, instruct4, 2)
            blitThatItem(screen, rules5, instruct5, 3)
            blitThatItem(screen, rules6, instruct6, 4)
            blitThatItem(screen, rules7, instruct7, 5)

def blitThatItem(screen, rules, instruct, i):
    instruct.centerx = screen.get_rect().centerx
    instruct.centery = screen.get_rect().centery + 20*i
    screen.blit(rules, instruct)

# contains logic for water movement
# check if it can go down, if not then check left or check right

def update(sim,display):
    if not sim.paused:
        if len(sim.dubLst) == 0 and sim.winningAmount <= sim.amountInBucket:
            sim.gameWon = True
        waterRect = getWaterRect(sim.particles)
        for p in sim.particles:
            # if the water falls in bucket then remove and count it as contribution
            #to win
            if sim.bucketLoc != None and p.pos.colliderect(sim.bucketLoc):
                sim.particles.remove(p)
                sim.amountInBucket += 1
                continue
            if p.pos.collidelist(sim.spongeLst) >= 0:
                sim.particles.remove(p)
                continue
            if p.pos.collidelist(sim.dubLst) >= 0:
            # experimenting with multiple hits on the dubs to make it dissapear

                # if p.pos.collidelist(sim.dubLst) == 0:
                #     sim.collectHit1 += 1
                #     if sim.collectHit1 == 5:
                #         sim.dubLst.remove(sim.dubLst[p.pos.collidelist(sim.dubLst)])
                # elif p.pos.collidelist(sim.dubLst) == 1:
                #     sim.collectHit2 += 1
                #     if sim.collectHit2 == 5:
                #         sim.dubLst.remove(sim.dubLst[p.pos.collidelist(sim.dubLst)])
                # elif p.pos.collidelist(sim.dubLst) == 2:
                #     sim.collectHit3 += 1
                #     if sim.collectHit2 == 5:
                #         sim.dubLst.remove(sim.dubLst[p.pos.collidelist(sim.dubLst)])

                sim.dubLst.remove(sim.dubLst[p.pos.collidelist(sim.dubLst)])
                sim.particles.remove(p)
                continue
            # if the particle goes off the screen remove it
            if p.pos[1] >= display[0]:
                sim.particles.remove(p)
            p.pos = p.pos.move(0,5)
            # case that the water doesn't collide then just let it be
            if (p.pos.collidelist(sim.wall)<0 and p.pos.collidelist(sim.blockLst)<0)\
                and p.pos.collidelist(waterRect) < 0:
                pass
            else:
                p.pos = p.pos.move(0,-5)
                if p.direction:
                    p.pos = p.pos.move(5,0)
                    if p.pos.collidelist(waterRect) < 0 and \
                        (p.pos.collidelist(sim.wall)<0 and \
                        p.pos.collidelist(sim.blockLst)<0) and \
                        p.pos[0] < display[0]:
                        pass
                    else:
                        p.direction = not p.direction
                        p.pos = p.pos.move(-5,0)
                else:
                    p.pos = p.pos.move(-5,0)
                    if(p.pos.collidelist(sim.wall)<0 and \
                        p.pos.collidelist(sim.blockLst)<0)\
                        and p.pos.collidelist(waterRect) < 0 and p.pos[0] > -5:
                        pass
                    else:
                        p.direction = not p.direction
                        p.pos = p.pos.move(5,0)


#pygame adapted from pygame documentation and tutorial when making 3d water
#http://pyopengl.sourceforge.net
#https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/
def mainLoop(lstWater, ground,bucket = None, sponge = [],block = [],collect = []):
    pygame.init()
    pygame.display.set_caption('Water Simulation')
    pygame.font.init()
    myfont = pygame.font.SysFont('Monaco', 30)
    display = (600,600)
    screen = pygame.display.set_mode(display)
    sim = System()
    sim.particles = copy.deepcopy(lstWater)
    sim.wall = copy.deepcopy(ground)
    sim.blockLst = copy.deepcopy(block)
    sim.dubLst = copy.deepcopy(collect)
    sim.bucketLoc = copy.deepcopy(bucket)
    sim.spongeLst = copy.deepcopy(sponge)
    sim.winningAmount = int(len(sim.particles)//2)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sim.particles = copy.deepcopy(lstWater)
                sim.wall = copy.deepcopy(ground)
                sim.blockLst = copy.deepcopy(block)
                sim.dubLst = copy.deepcopy(collect)
                sim.bucketLoc = copy.deepcopy(bucket)
                sim.spongeLst = copy.deepcopy(sponge)
                # sim.collectHit1 = 0
                # sim.collectHit2 = 0
                # sim.collectHit3 = 0
                sim.amountInBucket = 0
                launch.run()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    sim.paused = not sim.paused
                if event.key == pygame.K_r:
                    sim.particles = copy.deepcopy(lstWater)
                    sim.wall = copy.deepcopy(ground)
                    sim.blockLst = copy.deepcopy(block)
                    sim.dubLst = copy.deepcopy(collect)
                    sim.bucketLoc = copy.deepcopy(bucket)
                    sim.spongeLst = copy.deepcopy(sponge)
                    # sim.collectHit1 = 0
                    # sim.collectHit2 = 0
                    # sim.collectHit3 = 0
                    sim.amountInBucket = 0
        if pygame.mouse.get_pressed()[0] and sim.removable > 0:
            pos = pygame.mouse.get_pos()
            for wall in sim.wall:
                if wall.collidepoint(pos):
                    sim.wall.remove(wall)
                    sim.removable -= 1
        update(sim,display)
        render(screen,sim)
        pygame.display.flip()

# if __name__ == "__main__":
# 	mainLoop()
