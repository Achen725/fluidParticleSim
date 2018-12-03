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

class System(object):
    def __init__(self):
        self.particles = []
        self.wall = []
        self.display = (600,600)
        self.floorLevel = self.display[0]
        self.removable = 150
        self.paused = False
        self.blockPic = pygame.image.load("ground.png")
        self.waterPic = pygame.image.load("water.png")
        self.bucket = pygame.image.load("bucket.png")


    def getPos(self):
        lst = []
        for p in self.particles:
            lst.append((p.pos[0],p.pos[1]))
        return lst

class Particle(object):
    def __init__(self, image):
        self.size = 5
        self.force = (0, -5)
        self.pos = image.get_rect()
        self.floor = False
        #True is right, False is left
        self.direction = random.choice([True,False])

def getWaterRect(particleLst):
    lst = []
    for p in particleLst:
        lst.append(p.pos)
    return lst

def render(screen,sim):
    if not sim.paused:
        screen.fill((255,255,255))
        for wall in sim.wall:
            screen.blit(sim.blockPic,wall)
        for p in sim.particles:
            screen.blit(sim.waterPic, p.pos)

        bucketLoc = pygame.Rect(screen.get_rect().centerx-40,
                                            sim.display[0]-60,80,80)
        screen.blit(sim.bucket, bucketLoc)


        myFont = pygame.font.SysFont(None, 20)
        # text for number of water blocks
        text1 = myFont.render('Water Blocks: ' + \
            str(len(sim.particles)),True, (0, 0, 0), (255, 255, 255))
        waterText = text1.get_rect()
        waterText.left = 0
        waterText.centery = 20
        # text for number of blocks allowed to remove (Game mode only)
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
        screen.blit(text3, instruction)
    else:
        screen.fill((170,170,170))
        myFont = pygame.font.SysFont("Monaco", 30)
        rules = myFont.render('Objective: Get as much water in the bucket as possible.\
                        \nClick the mouse to erase the ground tiles and avoid \
                        \nthe grey tiles since you will not be able to erase thse\
                        \nPress H to resume the game',True,(0,0,0),(170,170,170))
        instruct = rules.get_rect()
        instruct.centerx = screen.get_rect().centerx
        instruct.centery = screen.get_rect().centery
        screen.blit(rules, instruct)

def update(sim,display):
    if not sim.paused:
        waterRect = getWaterRect(sim.particles)
        for p in sim.particles:
            if p.pos[1] >= display[0]:
                sim.particles.remove(p)
            p.pos = p.pos.move(0,5)
            if p.pos.collidelist(sim.wall) < 0 and \
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
                        # if p.pos.collidelist(waterRect) >= 0 and \
                        #     p.pos.move(-5,-5).collidelist(waterRect) >= 0:
                        p.direction = not p.direction
                        p.pos = p.pos.move(-5,0)

                else:
                    p.pos = p.pos.move(-5,0)
                    if p.pos.collidelist(sim.wall) < 0 and \
                        p.pos.collidelist(waterRect) < 0 and p.pos[0] > -5:
                        pass
                    else:
                        # if p.pos.collidelist(waterRect) >= 0 and \
                        #     p.pos.move(5,-5).collidelist(waterRect) >= 0:
                        p.direction = not p.direction
                        p.pos = p.pos.move(5,0)

            # else:
            #     if p.direction:
            #         p.pos = p.pos.move(5,0)
            #         if p.pos.collidelist(sim.wall) < 0 and \
            #             p.pos.collidelist(waterRect) < 0 and \
            #             p.pos[0] < display[0]:
            #             pass
            #         else:
            #             # if p.pos.collidelist(waterRect) >= 0 and \
            #             #     p.pos.move(-5,-5).collidelist(waterRect) >= 0 :
            #             p.direction =  not p.direction
            #             p.pos = p.pos.move(-5,0)
            #
            #     else:
            #         p.pos = p.pos.move(-5,0)
            #         if p.pos.collidelist(sim.wall) < 0 and \
            #             p.pos.collidelist(waterRect) < 0 and \
            #             p.pos[0] > -5:
            #             pass
            #         else:
            #             # if p.pos.collidelist(waterRect) >= 0 and \
            #             #     p.pos.move(5,-5).collidelist(waterRect) >= 0:
            #             p.direction =  not p.direction
            #             p.pos = p.pos.move(5,0)

def mainLoop(lstWater, block):
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
    sim.particles = copy.deepcopy(lstWater)
    sim.wall = copy.deepcopy(block)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sim.particles = copy.deepcopy(lstWater)
                sim.wall = copy.deepcopy(block)
                launch.run()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    sim.paused = not sim.paused
                if event.key == pygame.K_r:
                    sim.particles = copy.deepcopy(lstWater)
                    sim.wall = copy.deepcopy(block)
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
