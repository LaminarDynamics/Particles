# 2-18-22


import math
import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Vectors')
#######################################################################

particle_pos = [0, 0]
mass_poss = [400, 300]

# Vectors
vector_line_scaler = 50 # Makes vectors longer for viewing (Don't effect physics)
vector_inertia = [90, 15] # Direction / Magnatude
vector_gravity = [180, 1]

vector_resultant = [0, 0]


######################################################################

def VectorToCartesian(magnatude, direction):
	x = magnatude * math.cos(math.radians(direction))
	y = magnatude * math.sin(math.radians(direction))
	return [round(x, 1), round(y, 1)]


def AdjustVectorEnd(particle_pos, direction, magnatude):
	direction -= 90 # For pygame issues
	line_end = VectorToCartesian(magnatude, direction)
	line_end[0] += particle_pos[0] # Adjust for starting point
	line_end[1] += particle_pos[1]
	return int(line_end[0]), int(line_end[1]) # Change to int else pygame freaks out

def GetResultantVector(vector_a, vector_b): # Get resultant vector from two vectors
	### Get Vector Components
	Ax = vector_a[1] * math.cos(math.radians(vector_a[0]))
	Ay = vector_a[1] * math.sin(math.radians(vector_a[0]))
	Bx = vector_b[1] * math.cos(math.radians(vector_b[0]))
	By = vector_b[1] * math.sin(math.radians(vector_b[0]))
	### Polar Form
	Rx = Ax + Bx
	Ry = Ay + By
	length = math.sqrt(Rx**2 + Ry**2)
	radians = math.atan2(Ry, Rx) # Use atan2() NOT atan()!!!
	degrees = math.degrees(radians)
	degrees %= 360
	return degrees, length


def Locomotion(starting_point, direction, magnatude): # Locomotion(start[x, y], headingFromThere, speed-howfar)
		direction -= 90 # Otherwise heading is 90 degress off
		direction %= 360

		x_stuff = math.cos(math.radians(direction))
		y_stuff = math.sin(math.radians(direction))

		x_dif = magnatude * x_stuff
		y_dif = magnatude * y_stuff

		new_x = starting_point[0] + x_dif
		new_y = starting_point[1] + y_dif

		return int(new_x), int(new_y) # Change to int else pygame freaks out


def AngleBetweenPoints(point1, point2):  
	dx = point2[0] - point1[0]
	dy = point2[1] - point1[1]
	rads = math.atan2(dy,dx)
	rads %= 2*math.pi
	degs = math.degrees(rads) + 90
	degs %= 360
	return degs



while True:

	events = pygame.event.get() # Need this stuff else it freezes
	for event in events:                     
		if event.type != pygame.QUIT:

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					particle_pos[0] += 1
					print ("RIGHT Key")
				elif event.key == pygame.K_LEFT:
					particle_pos[0] -= 1
					print ("LEFT Key")

		else:
			sys.exit()


	# vector_inertia[0] += 1
	# vector_gravity[0] += 2

	resultant_vector = GetResultantVector(vector_inertia, vector_gravity)
	

	vector_inertia_line_end = AdjustVectorEnd(particle_pos, vector_inertia[0], vector_inertia[1] + vector_line_scaler)
	vector_gravity_line_end = AdjustVectorEnd(particle_pos, vector_gravity[0], vector_gravity[1] + vector_line_scaler) # Can add scaler (vector_gravity[1] + 50) to make more visible


	resultant_vector_line_end = AdjustVectorEnd(particle_pos, resultant_vector[0], resultant_vector[1])

	

	### Draw Masses
	pygame.draw.circle(gameDisplay, (255, 0, 0), particle_pos, 5)
	pygame.draw.circle(gameDisplay, (23, 212, 255), mass_poss, 10) # Mass


	### Draw Vector Lines
	pygame.draw.line(gameDisplay, (0, 255, 100), particle_pos, vector_inertia_line_end, 1)
	pygame.draw.line(gameDisplay, (199, 119, 50), particle_pos, vector_gravity_line_end, 1)
	pygame.draw.line(gameDisplay, (255, 0, 100), particle_pos, resultant_vector_line_end, 1)



	### Move Particle
	particle_pos = Locomotion(particle_pos, resultant_vector[0], resultant_vector[1])


	### Adjust Inertia Vector
	vector_inertia = GetResultantVector(vector_inertia, vector_gravity) # Does cooooool stuff (Adds much realizm)
	

	### Get new gravity vecctor
	particle_to_mass_angle = AngleBetweenPoints(particle_pos, mass_poss)
	print (particle_to_mass_angle)
	vector_gravity[0] = particle_to_mass_angle # Gravity pulls towards mass


	clock.tick(60) 
	pygame.display.update()
	pygame.display.flip()
	# gameDisplay.fill((0,0,0)) # Clears screen