# Creator: Tanner Bohn


from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np
import random
import itertools
from dotted_dict import DottedDict

from utils import apply_noise, shadeN
from GearSystem import GearSystem



def draw(final_size, draw_scale, palette, use_noise, seed):
	
	np_rand_state = np.random.get_state()
	rand_state = random.getstate()
	np.random.seed(seed)
	random.seed(seed)



	img = Image.new('RGBA', draw_size, palette.background)


	max_t = random.choice([100, 200, 400, 600])

	G = GearSystem(palette)

	path = []
	speeds = []
	colours = []

	t = 0
	dt = 0.01
	while t < max_t*math.pi*2:

		path.append(G.cur_loc)
		speeds.append(G.current_speed)
		colours.append(G.current_colour)

		G.step(dt)
		t += dt

	img_draw = ImageDraw.Draw(img, "RGBA")

	s = min(draw_size)

	pix_x = draw_size[0]/2 + path[0][0]*s/2
	pix_y = draw_size[1]/2 + path[0][1]*s/2

	pix_x = int(pix_x)
	pix_y = int(pix_y)
	prev_loc = (pix_x, pix_y)

	lines = []

	# draw shadow points (with lines connecting)
	for i_p in range(len(path)):
		if i_p == 0: continue


		pix_x = draw_size[0]/2 + path[i_p][0]*s/2
		pix_y = draw_size[1]/2 + path[i_p][1]*s/2

		pix_x = int(pix_x)
		pix_y = int(pix_y)

		new_loc = (pix_x, pix_y)

		# make line a bit thicker when it moves slowly
		rad = 1 + draw_scale*0.2/(speeds[i_p]**1.5+0.05)

		img_draw.line((prev_loc, new_loc), width=int(rad)+draw_scale, fill=palette.line_shadow)

		lines.append((prev_loc, new_loc, int(rad), colours[i_p]))

		prev_loc = new_loc


	# sort lines by draw order
	#lines = sorted(lines, key=lambda k: lines[3])[::-1]
	for p1, p2, rad, colour in lines:
		img_draw.line((p1, p2), width=rad, fill=colour)

	del img_draw

	img = img.resize(final_size, Image.LANCZOS)
	
	if use_noise:
		apply_noise(img, octaves=10, persistence=1, magnitude=20)



	img_draw = ImageDraw.Draw(img, "RGBA")
	FONT_SIZE = max(10, int(15*min(img.size)/1000))
	FONT = ImageFont.truetype("Roboto-Light.ttf", FONT_SIZE)
	
	text = "{}".format(seed)
	
	brightness = np.average(img.getpixel((0, img.size[1]-1)))

	if brightness >= 100:
		text_colour = (0,0,0)
	else:
		text_colour = (255,255,255)

	img_draw.text((5, img.size[1]-FONT_SIZE-5), text, fill=text_colour, font=FONT)
	del img_draw


	np.random.set_state(np_rand_state)
	random.setstate(rand_state)
			
	return img





final_size = (600, 600) # how large the final square should be
draw_scale = 5 # probably don't need to touch this
palette_name = "ink"

for seed in range(10):

	draw_size = (final_size[0]*draw_scale, final_size[1]*draw_scale)


	palette = DottedDict()
	if palette_name == "browns":
		palette.background = "#E2D9A6"
		palette.line_shadow = "#231811"
		palette.line_options = [("#402F18", "#6E5538"), ("#A68E5E", "#6E5538")]
		use_noise = False
	elif palette_name == "ink":
		palette.background = "#ffffff"
		palette.line_shadow = "#ffffff" #"#011017"
		palette.line_options = [("#021a24", "#011017"), ("#062330", "#011017")]
		use_noise= False
	elif palette_name == "blue_brown":
		# https://www.colourlovers.com/palette/4777762/Dawn2Dark
		palette.background = "#E5D2A4"
		palette.line_shadow = "#272935" #"#011017"
		palette.line_options = [("#253A6A", "#12839E"), ("#6AC6AA", "#272935")]
		use_noise= False
	elif palette_name == "architect":
		# https://www.colourlovers.com/palette/7583/our_own_architects
		palette.background = "#1A4C63"
		palette.line_shadow = "#072645" #"#011017"
		palette.line_options = [("#072645", "#D1CCB6"), ("#072645", "#A3B5A5")]
		use_noise= False
	elif palette_name == "genius":
		# https://www.colourlovers.com/palette/14537/genius_laureate
		palette.background = "#FEFFFE"
		palette.line_shadow = "#111111"
		palette.line_options = [("#ADDED0", "#E6E6E5"), ("#CDEFAB", "#DDDDDD")]
		use_noise= False
	elif palette_name == "undecided":
		# https://www.colourlovers.com/palette/1041410/undecided
		palette.background = "#DAD6CA"
		palette.line_shadow = "#42413c"
		palette.line_options = [("#6A5E72", "#563444"), ("#1BB0CE", "#4F8699")]
		use_noise= False


	img = draw(final_size, draw_scale, palette, use_noise, seed)

	img.save("tests/{}_{}.png".format(seed, palette_name))

	print("done ", seed)