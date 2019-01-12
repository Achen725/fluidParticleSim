from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL
import numpy as np
import pygame
import random
import copy
import math

# hardcoded map for testing purposes --> also the default map for game mode

ground = []
waterPic = pygame.image.load("water.png")

class Particle(object):
    def __init__(self, image):
        self.size = 5
        self.force = (0, -5)
        self.pos = image.get_rect()
        self.floor = False
        #True is right, False is left
        self.direction = random.choice([True,False])
# hard coded wall design
def createGenericWall():
    if ground == []:
        for x in range (-15, 615, 15):
            for y in range(90, 450, 15):
                ground.append(pygame.Rect(x, y, 15,15))

particle = []
# hard coded water design
def createGenericWater():
    if particle == []:
        for x in range(-15,615,5):
            for y in range(75, 90, 5):
                water = Particle(waterPic)
                water.pos.center = (x,y)
                particle.append(water)
# returns the list of given rect locations
def getBlock(num):
    createGenericWall()
    return ground
def getWater(num):
    createGenericWater()
    return particle
