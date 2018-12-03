from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL
import numpy as np
import pygame
import random
import copy
import math

ground = []
block = []
particle  = []
tileMap = createTileMap([])

waterPic = pygame.image.load("water.png")
groundPic = pygame.image.load("ground.png")
obstacle = pygame.image.load("block.png")
collect = pygame.image.load("dub.png")
bucket = pygame.image.load("bucket.png")
# numGround = 7000
# numCollect = 3
# numObstacle = 3000
#
# def createTileMap(tileMap):
#     for x in range(-15,300,15):
#         for y in range(90,150,15):
#             block.append(pygame.Rect(x,y,15,15))
#
#
#             random.choice(["block","ground"])
#             ground.append(pygame.Rect(x, y, 15,15))
#     return tileMap



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

def createGenericWall():
    if ground == []:
        for x in range (-15, 615, 15):
            for y in range(90, 450, 15):
                ground.append(pygame.Rect(x, y, 15,15))

particle = []

def createGenericWater():
    if particle == []:
        for x in range(-15,615,5):
            for y in range(75, 90, 5):
                water = Particle(waterPic)
                water.pos.center = (x,y)
                particle.append(water)

def getBlock(num):
    createGenericWall()
    return block

def getWater(num):
    createGenericWater()
    return particle
