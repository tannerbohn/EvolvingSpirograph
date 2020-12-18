import random
import numpy as np 
import math
from PIL import ImageColor
from utils import shadeN

class GearSystem:

	def __init__(self, palette):

		self.n_gears = random.choice([2, 3, 4, 5, 6])

		self.speeds = 1.*np.random.choice([-1, 1], self.n_gears)*np.random.choice([0, 0, 1, 2, 4, 8, 16], self.n_gears)

		radii = np.random.uniform(0.05, 1, self.n_gears)
		# this will lead to a strong bias towards smaller gears, while keeping the largest ones:
		#radii = radii**4 
		radii = radii/np.sum(radii)
		self.radii = radii*0.9 #make it take up *most* of the image

		self.cur_loc = np.array([sum(self.radii), 0])
		self.current_speed = 0

		self.colour_options = [[ImageColor.getcolor(v, "RGB") for v in colour_pair] for colour_pair in palette.line_options]


		self.cur_color_range = self.colour_options[0]
		self.current_colour = None 
		self.performed_regime_switch = False

		self.cur_angles = np.zeros(len(self.speeds))

	def step(self, dt):

		self.cur_angles += self.speeds*dt

		# compute displacement vectors of each gear
		compounded_delta = (0,0)
		for rad, theta in zip(self.radii, self.cur_angles):
			dx = rad*math.cos(theta)
			dy = rad*math.sin(theta)
			#vectors.append((dx, ))
			compounded_delta = (compounded_delta[0]+dx, compounded_delta[1]+dy)

		# compute speed
		dx = compounded_delta[0] - self.cur_loc[0]
		dy = compounded_delta[1] - self.cur_loc[1]
		v = ((dx**2 + dy**2)**0.5)/dt
		self.current_speed = v

		self.cur_loc = compounded_delta

		angle = (math.atan2(dy, dx) - math.pi/4)%(2*math.pi)
		# scale angle to 0 -> 1
		angle = angle/(2*math.pi)

		self.current_colour = shadeN(colours=(self.cur_color_range[0], self.cur_color_range[1], self.cur_color_range[0]), centers=(0, 0.5, 1), v=angle)

		if random.random() < dt*0.005:
			if random.random() < 0.5:
				self.speeds += np.random.normal(0, np.random.choice([0.002, 0.01, 0.05]), self.n_gears)
				#if random.random() < 0.25:
				#	self.current_colour = random.choice(self.colour_options)
			else:
				mask = np.random.choice([0, 1], self.n_gears)
				self.speeds = 1.*self.speeds*mask + (1-mask)*np.random.choice([-1, 1], self.n_gears)*np.random.choice([0, 0, 1, 2, 4, 8, 16], self.n_gears)

				self.performed_regime_switch = True

				#self.current_colour = random.choice(self.colour_options)
				self.cur_color_range = random.choice(self.colour_options)

			

		else:
			self.performed_regime_switch = False