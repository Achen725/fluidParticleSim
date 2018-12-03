from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import OpenGL
import numpy as np
import pygame
import random
import copy
import math
import launch


class Obstacle(object):
	def __init__(self):
		self.property = "ground"

class Ramp(Obstacle):
	def __init__(self):
		super().__init__()
	def draw(self, dim):
		glBegin(GL_LINES)
		glEnd()
		glFlush()

class Cube(Obstacle):
	def __init__(self):
		super().__init__()
		self.density = 10

class System(object):
	def __init__(self):
		self.getTicksLastFrame = 0
		self.totalParticles = self.makeParticles(10000)
		self.velocities = []*125000
		self.dim = 0.5
		self.floor = -0.5
		self.gridVelocities = []

	def grid(self):
		lines = []
		glBegin(GL_LINES)
		glColor3f(1,0,0)
		for i in range(1,50):
			w = -0.5+0.02*i
			for j in range(1, 50):
				h = -0.5+0.02*j
				glVertex3fv((w, h, 0.5))
				glVertex3fv((w, h, -0.5))
				glVertex3fv((w, 0.5, h))
				glVertex3fv((w, -0.5, h))
				glVertex3fv((0.5, w, h))
				glVertex3fv((-0.5, w, h))
		glEnd()
		glFlush()

	# cube template adapted from tutorial
	#https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/
	def solidCube(self, dim):
		sides = [(0,1),(0,3),(0,5),(2,1),(2,3),(2,7),
				(6,1),(6,5),(6,7),(4,5),(4,7),(4,3)]

		vertex = [(-dim,dim,dim),(dim,dim,dim),(dim,dim,-dim),(-dim,dim,-dim),
				(-dim,-dim,-dim),
				(-dim,-dim,dim),(dim,-dim,dim),(dim,-dim,-dim)]
		glBegin(GL_LINES)
		glColor3f(1,1,1)
		for side in sides:
			for point in side:
				glVertex3fv(vertex[point])
		glEnd()
		glFlush()

	def checkCollision(self, x, y, z):
		return len(self.gridVelocities[convertToIJK(x,y,z)]) > 5


	# method for calculating movement adapted from Austin Eng documentation
	# https://github.com/austinEng/WebGL-PIC-FLIP-Fluid
	def move(self, t):
		# take each particle in grid and assign to matrix
		gridVelocities =  [[] for i in range(125000)]
		for particle in self.totalParticles:
			index = convertToIJK(particle.x, particle.y, particle.z)
			# print(index)
			gridVelocities[index].append(particle.velocity)

		self.gridVelocities = gridVelocities
		# interpolate velocities of each grid
		# newVelocities = recalulateVelocity(gridVelocities)
		# add grid velocity to each particle
		# avg with total grid velocity
		for particle in self.totalParticles:
			# index = convertToIJK(particle.x, particle.y, particle.z)
			# velocity = (particle.velocity[0] + particle.acceleration[0], particle.velocity[1] + particle.acceleration[1], particle.velocity[2] + particle.acceleration[2])
			# velocityPic = (velocity[0] - newVelocities[index][0], velocity[1] - newVelocities[index][1], velocity[2] - newVelocities[index][2])
			# x = sum([pair[0] for pair in [velocityPic,newVelocities[index]]])
			# y = sum([pair[1] for pair in [velocityPic,newVelocities[index]]])
			# z = sum([pair[2] for pair in [velocityPic,newVelocities[index]]])
			# avg = (x/2,y/2,z/2)
			# # particle.updateVelocity(avg[0],avg[1],avg[2])
			particle.movePart(self.dim, self, t)

	def makeParticles(self,num):
		lst = []
		for i in range(num):
			randX = round(random.uniform(-0.2, 0.2),2)
			randZ = round(random.uniform(-0.2, 0.2),2)
			#randX = round(random.uniform(-0.5,0.5),2)
			#randZ = round(random.uniform(-0.5, 0.5),2)
			randY = round(random.uniform(0, 0.5), 2)
			lst.append(Particle(randX, randY, randZ))
		return lst

	def particleAtPos(self, y):
		for particle in self.totalParticles:
			if particle.y == y:
				return True
		return False


class Particle(object):

	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		self.prop = (self.x,self.y,self.z)
		self.speed = 1
		self.mass = 0.05
		self.velocity = (0, 0, 0)
		self.acceleration = (0, -9.8, 0)
		self.appliedForce = False
		self.collided = 0
		self.stopDrop = False

	def __repr__(self):
		return "Particle (" + str(self.x) + "," + str(self.y) + str(self.z) + ")"

	def movePart(self,dim, system, t = 0):

		dx = (self.velocity[0] * self.speed)
		dy = (-0.05 * self.speed)
		dz = (self.velocity[2] * self.speed)

		xBound = -dim <= self.x + dx <= dim
		yBound =  -dim <= self.y + dy <= dim
		zBound = -dim <= self.z + dz <= dim

		if not xBound or not yBound or not zBound:
			velocity = self.velocity
			# if(self.x + dx < -dim):
			# 	self.velocity = (random.uniform(-2, 2),velocity[1], velocity[2])
			# elif(self.x + dx > dim):
			# 	self.velocity = (random.uniform(-2, 2),velocity[1], velocity[2])
			if(self.y + dy < system.floor):
				# self.y = -dim;
				#check for collision
				if(system.checkCollision(self.x, self.y, self.z)):
					self.collided+=1
					if(self.collided > 100):
						self.y += 0.05
						self.floor+= 0.1
						self.collided = 0
						self.stopDrop = True
					else:
						self.x += (random.uniform(-0.06, 0.06)*self.speed)
						self.z += (random.uniform(-.06, .06)*self.speed)
				if(self.x>=0.5):
					self.x = 0.5
				elif(self.x<=-0.5):
					self.x = -0.5
				if(self.z>=0.5):
					self.z=0.5
				elif(self.z<=-0.5):
					self.z = -0.5
				if(self.y>=0.5):
					self.y= 0.5
				elif(self.y<=-0.5):
					self.y = system.floor

				# self.velocity = (random.uniform(-5, 5),0, random.uniform(-5, 5))
				# self.acceleration = (self.acceleration[0], min(self.acceleration[1] + random.uniform(0,t*3),0), self.acceleration[2])
			# elif (self.y + dy > dim):
			# 	self.velocity = (velocity[0]+random.uniform(-50, 50),random.uniform(-10, 30), velocity[2]+random.uniform(-50, 50))
			# if(self.z + dz < -dim) :
			# 	self.velocity = (velocity[0], velocity[1],random.uniform(-2, 2))
			# elif(self.z + dz > dim) :
			# 	self.velocity = (velocity[0], velocity[1],random.uniform(-2, 2))
		else:
			if(not self.stopDrop):
				self.y-=(0.05*self.speed)
				if(self.y<=-0.5):
					self.y= self.floor
			else:
				if(system.checkCollision(self.x, self.y, self.z)):
					self.collided+=1
					if(self.collided > 100):
						self.y += 0.05
						self.collided = 0
						self.stopDrop = True
					else:
						self.x += (random.uniform(-0.06, 0.06)*self.speed)
						self.z += (random.uniform(-.06, .06)*self.speed)
				if(self.x>=0.5):
					self.x = 0.5
				elif(self.x<=-0.5):
					self.x = -0.5
				if(self.z>=0.5):
					self.z=0.5
				elif(self.z<=-0.5):
					self.z = -0.5
				if(self.y>=0.5):
					self.y=0.5
				elif(self.y<=-0.5):
					self.y = -0.5

			# velocity = self.velocity
			# if self.appliedForce:
			# 	self.velocity = (velocity[0] + random.uniform(0, 10),random.uniform(0, 10), velocity[2])
			# self.x += (velocity[0] * self.speed)
			# self.y += (velocity[1] * self.speed)
			# self.z += (velocity[2] * self.speed)

	def updateVelocity(self, dx, dy, dz):
		self.velocity = (dx, dy, dz)

	def drawParticle(self):
		glPointSize(5.0)
		glBegin(GL_POINTS)
		glVertex3f(self.x, self.y, self.z)
		glColor3f(0,0.5,1)
		glEnd()

def drawParticles(totalParticles):
	for particle in totalParticles:
		particle.drawParticle()

# convert x,y,z coordinate system to i,j,k so we can find the index of particle
def convertToIJK(x, y, z):
	i = (int((x + 0.5) * 99)) // 2
	j = (int((y + 0.5) * 99)) // 2
	k = (int((z + 0.5) * 99)) // 2
	return int((i * 50 + j) + (k * 2500))

def recalulateVelocity(velocities):
	newVelocities = []
	for v in velocities:
		x = sum([pair[0] for pair in v])
		y = sum([pair[1] for pair in v])
		z = sum([pair[2] for pair in v])

		if(len(v) == 0):
			newVelocities.append((0,0,0))
		else:
			# average velocity
			newVelocities.append((x/len(v), y/len(v), z/len(v)))
	return newVelocities

def normalize(mouseX, mouseY):
	x = (mouseX) / 1000 - 0.5
 	y = 0.5 - (mouseY) / 1000
 	z = 0.5
	return np.array([x, y, z])

def update(deltaTime, mySystem):
	totalParticles = mySystem.totalParticles
	mySystem.move(deltaTime)

def mainLoop(simulation):
	# camera and pygame adapted from pyopengl documentation and previous tutorial
	#http://pyopengl.sourceforge.net
	#https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/
	pygame.init()
	# window size
	display = (1000,1000)
	screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	# camera
	camera = gluPerspective(45, (display[0]/display[1]), 0.1, 20.0)
	glTranslatef(0.0,0.0, -5)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				launch.run()
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
		simulation.solidCube(simulation.dim)
		# simulation.grid()
		drawParticles(simulation.totalParticles)
		# size manipulation of particles
		# glPointSize(1)
		#update the frame
		pygame.display.flip()

def main():
	simulation = System()
	mainLoop(simulation)
# if __name__== "__main__":
# 	main()
