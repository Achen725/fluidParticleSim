from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import OpenGL
import numpy as np
import pygame
import random
import copy
import math

def convertToIJK(x, y, z):
	i = (int((x + 0.5) * 10)) % 2
	j = (int((y + 0.5) * 10)) % 2
	k = (int((z + 0.5) * 10)) % 2
	return int((i * 5 + j) + (z * 25))

def recalulateVelocity(velocities):
	newVelocities = []
	for v in velocities:
		x = sum([pair[0] for pair in v])
		y = sum([pair[1] for pair in v])
		z = sum([pair[2] for pair in v])

		if(len(v) == 0):
			newVelocities.append((0,0,0))
		else:
			newVelocities.append((x/len(v), y/len(v), z/len(v)))
	return newVelocities

class System(object):
	def __init__(self):
		self.name = random.random()
		self.getTicksLastFrame = 0
		self.movementX = 0.3
		self.movementZ = 0.3
		self.totalParticles = self.makeParticles(10000)
		self.velocities = []*125

	def solidCube(self):
		sides = [(0,1),(0,3),(0,5),(2,1),(2,3),(2,7),
				(6,1),(6,5),(6,7),(4,5),(4,7),(4,3)]

		vertex = [(-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,0.5,-0.5),(-0.5,0.5,-0.5),(-0.5,-0.5,-0.5),
				(-0.5,-0.5,0.5),(0.5,-0.5,0.5),(0.5,-0.5,-0.5)]

		glBegin(GL_LINES)
		glColor3f(1,1,1)
		for side in sides:
			for point in side:
				glVertex3fv(vertex[point])
		glEnd()
		glFlush()

	def move(self):
		# take each particle in grid and assign to matrix
		gridVelocities =  [ [] for i in range(125) ]
		for particle in self.totalParticles:
			index = convertToIJK(particle.x, particle.y, particle.z)
			gridVelocities[index].append(particle.velocity)
		# interpolate velocities of each grid
		newVelocities = recalulateVelocity(gridVelocities)

		# add grid velocity to each particle
		# avg with total grid velocity
		for particle in self.totalParticles:
			index = convertToIJK(particle.x, particle.y, particle.z)

			velocity = (particle.velocity[0] + particle.acceleration[0], particle.velocity[1] + particle.acceleration[1], particle.velocity[2] + particle.acceleration[2])

			velocityPic = (velocity[0] - newVelocities[index][0], velocity[1] - newVelocities[index][1], velocity[2] - newVelocities[index][2])

			x = sum([pair[0] for pair in [velocity,newVelocities[index]]])
			y = sum([pair[1] for pair in [velocity,newVelocities[index]]])
			z = sum([pair[2] for pair in [velocity,newVelocities[index]]])

			avg = (x/2,y/2,z/2)
			particle.updateVelocity(avg[0],avg[1],avg[2])
			particle.movePart(1,2,3)

	def makeParticles(self,num):
		lst = []
		for i in range(num):
			randX = round(random.uniform(-0.2, 0.2),2)
			#randX = round(random.uniform(-1, 1),2)
			#randZ = round(random.uniform(-1, 1),2)
			randY = round(random.uniform(0, 0.5), 2)
			randZ = round(random.uniform(-0.2, 0.2),2)
			lst.append(Particle(randX, randY, randZ))
		return lst

class Particle(object):

	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		self.prop = (self.x,self.y,self.z)
		initialSpeed = 0.4
		self.speed = 0.0002
		self.velocity = (0, 0, 0)
		self.acceleration = (0, -9.8, 0)

	def __repr__(self):
		return "Particle (" + str(self.x) + "," + str(self.y) + str(self.z) + ")"

	def movePart(self,dx, dy, dz):
		dx = (self.velocity[0] * self.speed)
		dy = (self.velocity[1] * self.speed)
		dz = (self.velocity[2] * self.speed)

		xBound = -0.5 <= self.x + dx <= 0.5
		yBound = -0.5 <= self.y + dy <= 0.5
		zBound = -0.5 <= self.z + dz <= 0.5

		if not xBound or not yBound or not zBound:
			velocity = self.velocity
			if(self.x + dx < -0.5):
				self.velocity = (random.uniform(-100, 100),velocity[1], velocity[2])
			elif(self.x + dx > 0.5):
				self.velocity = (random.uniform(-100, 100),velocity[1], velocity[2])
			if(self.y + dy < -0.5):
				self.velocity = (velocity[0]+random.uniform(-500, 500),random.uniform(0, 500), velocity[2]+random.uniform(-500, 500))
			elif(self.y + dy > 0.5):
				self.velocity = (velocity[0]+random.uniform(-500, 500),random.uniform(-500, 0), velocity[2]+random.uniform(-500, 500))
			if(self.z + dz < -0.5):
				self.velocity = (velocity[0], velocity[1],random.uniform(-100, 100))
			elif(self.z + dz > 0.5):
				self.velocity = (velocity[0], velocity[1],random.uniform(-100, 100))
		else:
			velocity = self.velocity
			self.x += (velocity[0] * self.speed)
			self.y += (velocity[1] * self.speed)
			self.z += (velocity[2] * self.speed)

	def updateVelocity(self, dx, dy, dz):
		self.velocity = (dx, dy, dz)

	def collides(self, totalParticles):
		if self in totalParticles:
			return True
		if  -0.5 > self.x > 0.5:
			return True
		if  -0.5 > self.y > 0.5:
			return True
		if  -0.5 > self.z > 0.5:
			return True
		return False

	def drawParticle(self):
		glPointSize(5.0)
		glBegin(GL_POINTS)
		glVertex3f(self.x, self.y, self.z)
		glColor3f(0,0.5,1)
		# glPointSize(2.0)
		glEnd()

	def fillSpace(self):
		pass

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
	mySystem.move()

def mainLoop(simulation):
	pygame.init()
	# window size
	display = (1000,1000)
	screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	# camera
	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
	glTranslatef(0.0,0.0, -5)

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
		glPointSize(20)
		#update the frame
		pygame.display.flip()

def main():
	simulation = System()
	mainLoop(simulation)
if __name__== "__main__":
	main()
