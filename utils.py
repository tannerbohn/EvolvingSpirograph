import numpy as np
import random
import noise
import itertools

def apply_noise(img, box=None, octaves=10, persistence=0.7, magnitude=30):

	img_size = img.size
	img_pix = img.load()
	#print(img_pix[0,0])

	if box == None:
		box = (0,0, img.size[0], img.size[1])

	start_x = int(box[0])
	start_y = int(box[1])

	width = int(box[2] - box[0])#+1
	height = int(box[3] - box[1])#+1


	# add some perlin noise to filled area
	z_seed_offset = 30*random.random()

	# for lighter backgrounds, need to bias noise to be more negative

	for xpix, ypix in itertools.product(range(start_x, start_x+width), range(start_y, start_y+height)):
		r, g, b, a = img_pix[xpix,ypix]
		a = a/255

		if a == 0: continue

		brightness = ((r+g+b)/3)/255
		# convert brightness to [-1, 1]
		brightness = 2*brightness - 1
		#m = abs((r+g+b)//3 - 127.5)/127.7
		#m = (m*2)+1

		xf = xpix/1000#min(img_size)
		yf = ypix/1000#min(img_size)

		# pnoise returns values between -1 and 1 (sorta)
		z = noise.pnoise2(xf+z_seed_offset, yf+z_seed_offset, octaves=octaves, persistence=persistence)

		zmin = -1 - brightness
		zmax = 1 - brightness


		z = (z + 1)/2
		z = z*(zmax - zmin) + zmin
		z = z * magnitude

		

		#if random.random() < 0.01:
		#	print(a)

		#pix[xp,yp] = (int(r*z), int(g*z), int(b*z))
		img_pix[xpix,ypix] = (int(r+z), int(g+z), int(b+z), int(a*255))

# supply vector of n colours and their centers and linearly combine them
def shadeN(colours, centers, v):

	if len(colours) == 1:
		return colours[0]
	elif len(colours) == 0:
		return (0,0,0)

	# centers must be sorted

	if v < min(centers): v = min(centers)

	if v > max(centers): v = max(centers)

	# figure out which range v is in
	r = (0,1)
	rIndex=0
	for i in range(len(centers)-1):
		m = centers[i]
		M = centers[i+1]

		if v >= m and v <= M:
			r = (m, M)
			rIndex=i
			break

	# now just return the shade in that range
	vp = (1.0*v - 1.0*r[0])/(1.0*r[1]-1.0*r[0])
	
	colour = np.array(colours[rIndex])*(1-vp) + np.array(colours[rIndex+1])*(vp)
	colour = [int(c) for c in colour]
	return tuple(colour)
