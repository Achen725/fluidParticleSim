from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import OpenGL
import numpy as np
import pygame
import random
import copy
import math

#totalParticles = []

class System(object):
	def __init__(self):
		self.name = random.random()
		self.getTicksLastFrame = 0
		self.movementX = 0.3
		self.movementZ = 0.1
		self.totalParticles = self.makeParticles(400)

	def solidCube(self):
		sides = [(0,1),(0,3),(0,5),(2,1),(2,3),(2,7),
				(6,1),(6,5),(6,7),(4,5),(4,7),(4,3)]
		vertex = [(-1,1,1),(1,1,1),(1,1,-1),(-1,1,-1),(-1,-1,-1),
				(-1,-1,1),(1,-1,1),(1,-1,-1)]

		glBegin(GL_LINES)
		glColor3f(1,1,1)
		for side in sides:
			for point in side:
				glVertex3fv(vertex[point])
		glEnd()
		glFlush()

	def move(self, x, y, z):
		for particle in self.totalParticles:
			particle.movePart(x,y,z)

	def makeParticles(self,num):
		lst = []
		for i in range(num):
			#randX = round(random.uniform(-0.2, 0.2),2)
			randX = round(random.uniform(-1, 1),2)
			randZ = round(random.uniform(-1, 1),2)
			randY = round(random.uniform(-1.0, -0.5), 2)
			#randZ = round(random.uniform(-0.2, 0.2),2)
			lst.append(Particle(randX, randY, randZ))
			#totalParticles[-1].drawParticle()
		return lst

flowRate = 4
elasticity = 0.4
running = True
filled = False

class Particle(object):

	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		self.prop = (self.x,self.y,self.z)
		self.mass = .5
		self.size = 3
		self.gravity = -0.02
		initialSpeed = 0.4
		self.speed = initialSpeed * random.random() / self.size
		angle = 360 * random.random()
		self.dx = self.speed * math.cos(angle)
		self.dz = self.speed * math.sin(angle)

	def __eq__(self,other):
		if self.getHashables() == other.getHashables():
			return True
		return False

	def __repr__(self):
		return "Particle (" + str(self.x) + "," + str(self.y) + str(self.z) + ")"

	def getHashables(self):
		return (self.prop, self.mass,self.size, self.dx, self.dz, self.speed)

	def movePart(self,dx, dy, dz):
		xBound = -1 <= self.x + dx <= 1
		yBound = -1 <= self.y + dy <= 1
		zBound = -1 <= self.z + dz <= 1
		if not xBound or not yBound or not zBound:
			pass
		else:
			self.x += dx
			self.y += dy
			self.z += dz

	def collides(self, totalParticles):
		if self in totalParticles:
			return True
		if  -1 > self.x > 1:
			return True
		if  -1 > self.y > 1:
			return True
		if  -1 > self.z > 1:
			return True
		return False

	def drawParticle(self):
		glBegin(GL_POINTS)
		glVertex3f(self.x, self.y, self.z)
		glColor3f(0,0.5,1)
		glEnd()

	def fillSpace(self):
		pass

# def applyBound(xy, vel, xlim, ylim, zlim, damp, i):
#     if xy[i, 0] < xlim[0]:
#         vel[i, 0] *= damp
#         xy[i, 0] = xlim[0]
#     elif xy[i, 0] > xlim[1]:
#         vel[i, 0] *= damp
#         xy[i, 0] = xlim[1]
#
#     if xy[i, 1] < ylim[0]:
#         vel[i, 1] *= damp
#         xy[i, 1] = ylim[0]
#     elif xy[i, 1] > ylim[1]:
#         vel[i, 1] *= damp
#         xy[i, 1] = ylim[1]
#
# def eulerStep(xy, vel, force, rho, dt, xlim, ylim, damp, hashmap):
#     for i in range(xy.shape[0]):
#         vel[i] += dt * force[i] / rho[i]
#         xy[i] += dt * vel[i]
#         applyBound(xy, vel, xlim, ylim, zlim, damp, i)
#         hashmap.move(i, xy[i])

def drawParticles(totalParticles):
	for particle in totalParticles:
		particle.drawParticle()

def checkFilled(x,y,z, totalParticles):
	for xPoint in range(-100,100,10):
		for zPoint in range(-100,100,10):
			if (round(xPoint/100), y, round(zPoint/100)) not in totalParticles:
				return False
	return True

def update(deltaTime, mySystem):
	totalParticles = mySystem.totalParticles
	xMove = mySystem.movementX
	zMove = mySystem.movementZ
	#if deltaTime % 1 == 0:
	for particle in totalParticles:
		x,y,z = particle.prop
		grav = particle.gravity * particle.mass
		temp = Particle(x,y+grav, z)
		if not filled and -1 <= y + grav <= 1 and not temp.collides(totalParticles):
			particle.movePart(0,grav,0)
			particle.drawParticle()

	# if deltaTime % 2:
	# 	move(xMove,0,0)
	# 	mySystem.movementX = - mySystem.movementX

	# if deltaTime % 4:
	# 	move(0,0,zMove)
	# 	mySystem.movementZ = - mySystem.movementZ

def mainLoop(simulation):
	pygame.init()
	# window size
	display = (1000,1000)
	screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	# camera
	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
	glTranslatef(0.0,0.0, -10)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					glRotatef(6,0,1,0)
				elif event.key == pygame.K_RIGHT:
					glRotatef(6,0,-1,0)
				elif event.key == pygame.K_UP:
					glRotatef(6,1,0,0)
				elif event.key == pygame.K_DOWN:
					glRotatef(6,-1,0,0)
				elif event.key == pygame.K_w:
					simulation.move(0,0.2,0)
				elif event.key == pygame.K_s:
					simulation.move(0,-0.2,0)
				elif event.key == pygame.K_a:
					simulation.move(-0.2,0,0)
				elif event.key == pygame.K_d:
					simulation.move(0.2,0,0)

		# timer to keep continuous movement
		t = pygame.time.get_ticks()
		deltaTime = (t - simulation.getTicksLastFrame)/100
		simulation.getTicksLastFrame = t

		update(deltaTime, simulation)
		# clear current frame
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		# redraw your cube
		simulation.solidCube()
		drawParticles(simulation.totalParticles)

		# size manipulation of particles
		glPointSize(3)
		#update the frame
		pygame.display.flip()

def main():
	simulation = System()
	mainLoop(simulation)
if __name__== "__main__":
	main()
