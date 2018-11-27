from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import OpenGL
import numpy as np
import pygame
import random
import sys
import math
import copy
from pygame.locals import *

class System(object):
    def __init__(self):
        self.getTicksLastFrame = 0
        self.dim = 500
        self.getTicksLastFrame = 0
        self.grid = self.makeGrid(1000)
        self.squareDim = self.dim / len(self.grid)
        self.totalParticles = self.makeParticles(1000)

    def makeGrid(self, size):
        col = [0] * size
        grid = []
        for i in range(size):
            grid.append(copy.deepcopy(col))
        return grid

    def drawParticles(self,screen):
        for p in self.totalParticles:
            p.draw(screen)

    def makeParticles(self,num):
        lst = []
        while len(lst) <= num:
            randX = random.randint(0,self.dim)
            randY = random.randint(0,self.dim)
            if self.grid[randX][randY] >= 5:
                continue
            self.grid[randX][randY] += 1
            lst.append(Particle(randX, randY))
        return lst

	def move(self, t):
		for particle in self.totalParticles:
			particle.movePart(self.dim, self, t)

# gridVelocities =  [[] for i in range(125000)]
# for particle in self.totalParticles:
# 	gridVelocities[index].append(particle.velocity)
# self.gridVelocities = gridVelocities

class Particle(object):
    def __init__(self,x,y):
        self.pos = (x,y)
        self.speed = 1
        self.mass = 5
        self.r = 4
        self.r2 = self.r ** 2
        self.velocity = (0, 0)
        self.acceleration = (0, -9.8)


    def movePart(self,dim, system, t = 0):

        dx = (self.velocity[0] * self.speed)
        dy = 0.5 * self.mass * t

        xBound =  self.r <= self.x + dx <= dim -self.r
        yBound =  self.r <= self.y + dy <= dim -self.r

        if not xBound or not yBound:
            velocity = self.velocity
        else:
            self.pos = (self.pos[0]+dx, self.pos[1]+dy)

    def collides(self):
        for particle in totalParticles:
            pass

    def draw(self,screen):
        pygame.draw.circle(screen,(0,0,255),self.pos,self.r)

def update(t, sim):
    totalParticles = sim.totalParticles
    sim.move(deltaTime)

def mainLoop(simulation):
    pygame.init()
    # window size
    display = (800,800)
    screen = pygame.display.set_mode(display)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        t = pygame.time.get_ticks()
        deltaTime = (t - simulation.getTicksLastFrame)/100
        simulation.getTicksLastFrame = t

        update(deltaTime, simulation)
        simulation.drawParticles(screen)
        pygame.display.flip()


def main():
	simulation = System()
	mainLoop(simulation)
if __name__== "__main__":
	main()
