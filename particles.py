import math
from pandas import show_versions
import pygame
import sys
import random
import particle_functions as P2


pygame.init()
clock = pygame.time.Clock()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Particles')
#######################################################################

mass_pos = [400, 300]

# Vectors
vector_line_scaler = 50 # Makes vectors longer for viewing (Don't effect physics)
# vector_inertia = [90, 5] # Direction / Magnatude
# vector_gravity = [180, .1] # Direction / Magnatude
# vector_resultant = [0, 0]

particles = []

############################## SELECTABLE STUFFS #################
particle_count = 100
allow_mass_collision = True
allow_particle_collision = True
show_vectors = False


######################################################################

### Create x number of particles
for x in range(particle_count):
	rand_x = random.randint(0, display_width)
	rand_y = random.randint(0, display_height)
	rand_speed = random.randint(1, 3)
	rand_hdg = random.randint(1, 360)
	gravity_strength = .1 # If this is too small orbits get blocky curves
	rand_size = random.randint(1, 5)
	particles.append(P2.Particles([rand_x, rand_y], rand_size, [rand_hdg, rand_speed], [0, gravity_strength], x))




while True:

	events = pygame.event.get() # Need this stuff else it freezes
	for event in events:                     
		if event.type != pygame.QUIT:

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					mass_pos[0] += 1
					print ("RIGHT Key")
				elif event.key == pygame.K_LEFT:
					mass_pos[0] -= 1
					print ("LEFT Key")

		else:
			sys.exit()



	### Do all particles in list
	for this_particle in particles:
		resultant_vector = P2.GetResultantVector(this_particle.vector_inertia, this_particle.vector_gravity)
		

		### Vector Line Lengths
		vector_inertia_line_end = P2.AdjustVectorEnd(this_particle.particle_pos, this_particle.vector_inertia[0], this_particle.vector_inertia[1] + vector_line_scaler)
		vector_gravity_line_end = P2.AdjustVectorEnd(this_particle.particle_pos, this_particle.vector_gravity[0], this_particle.vector_gravity[1] + vector_line_scaler) # Can add scaler (vector_gravity[1] + 50) to make more visible
		resultant_vector_line_end = P2.AdjustVectorEnd(this_particle.particle_pos, resultant_vector[0], resultant_vector[1] + vector_line_scaler)

		

		### Draw Masses
		pygame.draw.circle(gameDisplay, this_particle.color, this_particle.particle_pos, this_particle.size) # Particle
		pygame.draw.circle(gameDisplay, (23, 212, 255), mass_pos, 10) # Mass


		### Draw Vector Lines
		if show_vectors:
			pygame.draw.line(gameDisplay, (0, 255, 100), this_particle.particle_pos, vector_inertia_line_end, 1) # Inertia
			pygame.draw.line(gameDisplay, (199, 119, 50), this_particle.particle_pos, vector_gravity_line_end, 1) # Gravity
			pygame.draw.line(gameDisplay, (255, 0, 100), this_particle.particle_pos, resultant_vector_line_end, 1) # Resultant



		### Move Particle
		this_particle.particle_pos = P2.Locomotion(this_particle.particle_pos, resultant_vector[0], resultant_vector[1])


		### Check for collisions
		if allow_particle_collision == False:
			particles, hit = P2.CheckParticleCollisions(this_particle, particles)
			if hit:
				pygame.draw.circle(gameDisplay, (255, 0, 0), this_particle.particle_pos, 100) # BOOM


		if allow_mass_collision == False:
			particles, hit = P2.CheckMassCollisions(particles, this_particle, mass_pos)
			if hit:
				pygame.draw.circle(gameDisplay, (255, 0, 0), mass_pos, 50) # BOOM



		### Adjust Inertia Vector
		this_particle.vector_inertia = P2.GetResultantVector(this_particle.vector_inertia, this_particle.vector_gravity) # Does cooooool stuff (Adds much realizm)


		### Get closest particle
		closest_particle_id = P2.GetClosestParticle(this_particle, particles)
		for item in particles:
			if closest_particle_id == item.ident:
				closest_cords = item.particle_pos
		
		### Gravity towards closest particle
		particle_to_mass_angle = P2.AngleBetweenPoints(this_particle.particle_pos, closest_cords)
		

		### Get new gravity vector
		particle_to_mass_angle = P2.AngleBetweenPoints(this_particle.particle_pos, mass_pos)
		this_particle.vector_gravity[0] = particle_to_mass_angle # Gravity pulls towards mass


	clock.tick(60) 
	pygame.display.update()
	pygame.display.flip()
	gameDisplay.fill((0,0,0)) # Clears screen