# 2-18-22
import math
import random



class Particles:
	def __init__(self, particle_pos, size, vector_inertia, vector_gravity, ident):
		self.particle_pos = particle_pos
		self.size = size
		self.vector_inertia = vector_inertia
		self.vector_gravity = vector_gravity
		self.ident = ident
		self.color = random.choice(
            [
                (255, 0, 0),
                (66, 135, 245),
                (66, 245, 239),
                (227, 245, 66),
                (245, 66, 203),
                (81, 66, 245),
                (255, 255, 255),
                (255, 132, 0),
            ]
        )


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


def CheckParticleCollisions(this_particle, all_particles):
		for particle in all_particles:
			distance = Distance(this_particle.particle_pos, particle.particle_pos)
			hit = False
			if distance != 0 and distance < this_particle.size: # Sometimes distance returns 0
				hit = True
				#### Remove smaller particle
				remove_id = 0
				if this_particle.size > particle.size:
					remove_id = particle
				else:
					remove_id = this_particle

				all_particles.remove(remove_id)
		return all_particles, hit



def CheckMassCollisions(all_particles, this_particle, mass_pos):
		distance = Distance(this_particle.particle_pos, mass_pos)
		hit = False
		if distance != 0 and distance < 10: # Sometimes distance returns 0
			#### Remove particle
			all_particles.remove(this_particle)
			hit = True

		return all_particles, hit



def Distance(point1, point2):
		dist = math.sqrt( (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 )
		return dist


def GetClosestParticle(this_particle, all_particles):
	dict_of_distances = {}
	for particle in all_particles:
		distance = Distance(this_particle.particle_pos, particle.particle_pos)
		if distance != 0: # Don't add self to dict
			dict_of_distances[distance] = particle.ident

	closest_particle = min(dict_of_distances)
	id_of_closest = dict_of_distances[closest_particle]
	# print ("Id of closest = ", id_of_closest)
	# print ("length ", len(all_particles))
	# return all_particles[id_of_closest - 1].ident
	return id_of_closest