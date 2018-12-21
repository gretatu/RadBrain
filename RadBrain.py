import numpy 
import cv2
import os
from PIL import Image, ImageFont, ImageDraw
import random
import math
import datetime

date = str(datetime.datetime.now())
date_str = date.replace(' ','-')
date_str = date_str.replace(':','.')
date_str = date_str[:-10]


def distance(a,b):

	hyp=math.sqrt(math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2))

	return hyp

textstr = input("Please type your brain word:")
if len(textstr) < 7:
    print("Awesome, the gyri are cooking, please wait")
if len(textstr) > 7:
    textstr = input("Please type a shorter word. Our brains are not big enough:")
    while len(textstr) > 7:
        textstr = input("Omg did you not listen, please type a shorter word:")
    else:
        print("Awesome, the gyri are cooking, please wait")


img = cv2.imread('template.png',0)
edges = cv2.Canny(img,180,250)
cv2.imwrite('edges.png',edges)
edges = Image.open('edges.png')


cur_dir = os.path.dirname(__file__)

brain1 = Image.open('template.png')
brain_orig=brain1
rois = Image.open('ROIs.png')



fill_col=(120,120,120)
fill_col2y=fill_col
fill_col2x=fill_col

brain_w, brain_h = brain1.size
brain = Image.new('RGBA', (brain_w, brain_h), (255, 255, 255, 255))
brain.paste(brain1, (0,0))

maskedge=[]
maskedges=[]
maskedge2=[]

xcutoffs=[('a',999),('b',999),('c',999),('d',999),('e',999),('f',999),('g',999),('h',999),
('i',999),('j',999),('k',999),('l',999),('m',999),('n',999),('o',999),('p',999),('q',999),
('r',999),('s',999),('t',999),('u',999),('v',999),('w',999),('x',999),('y',999),('z',999)]

ycutoffs=[('a',999),('b',999),('c',999),('d',999),('e',999),('f',999),('g',999),('h',999),
('i',999),('j',999),('k',999),('l',999),('m',999),('n',999),('o',999),('p',999),('q',999),
('r',999),('s',999),('t',999),('u',999),('v',999),('w',999),('x',999),('y',999),('z',999)]

xhole_cutoffs=[('a',(18,48)),('b',(15,45)),('c',(999,999)),('d',(999,999)),('e',(25,45)),('f',(999,999)),('g',(999,999)),('h',(999,999)),
('i',(999,999)),('j',(999,999)),('k',(999,999)),('l',(999,999)),('m',(999,999)),('n',(999,999)),('o',(999,999)),('p',(999,999)),('q',(999,999)),
('r',(999,999)),('s',(999,999)),('t',(999,999)),('u',(999,999)),('v',(38,68)),('w',(999,999)),('x',(999,999)),('y',(999,999)),('z',(999,999))]

yhole_cutoffs=[('a',(20,72)),('b',(112,170)),('c',(999,999)),('d',(999,999)),('e',(7,33)),('f',(999,999)),('g',(999,999)),('h',(999,999)),
('i',(999,999)),('j',(999,999)),('k',(999,999)),('l',(999,999)),('m',(999,999)),('n',(999,999)),('o',(999,999)),('p',(999,999)),('q',(999,999)),
('r',(999,999)),('s',(999,999)),('t',(999,999)),('u',(999,999)),('v',(20,72)),('w',(999,999)),('x',(999,999)),('y',(999,999)),('z',(999,999))]


#GET ROIS
frontal=[]
temporal=[]
roi_w, roi_h = rois.size
for x in range(0,roi_w):
	for y in range(0,roi_h):

		pp=rois.getpixel((x,y))

		if pp[1]-pp[0] > 20:
			frontal.append((x,y))	

		elif pp[0]-pp[1] > 20:
			temporal.append((x,y))	

roi=frontal

restart=0
stop=0

while stop==0:

	restart=0

	brain = Image.open('template.png')
	brain.save('brain_temp.png')

	fill=[]
	edge=[]

	let_i=0

	for let in textstr:

		# brain.show()

		brain_prev=brain

		edge=[]
		edge_int=[]

		print(let)

		xcut=[xcutoffs[i][1] for i, j in enumerate(xcutoffs) if j[0] == let]
		ycut=[ycutoffs[i][1] for i, j in enumerate(ycutoffs) if j[0] == let]

		xhole_cut=[xhole_cutoffs[i][1] for i, j in enumerate(xhole_cutoffs) if j[0] == let]
		yhole_cut=[yhole_cutoffs[i][1] for i, j in enumerate(yhole_cutoffs) if j[0] == let]

		let_i=let_i+1

		let1 = "vectorized/" + let + ".png"
		let2 = Image.open(os.path.join(cur_dir, let1))

		letcv=cv2.imread(os.path.join(cur_dir, let1))

		let=let2.resize((700, 394), Image.ANTIALIAS)

		let_w, let_h = let.size

		got_letpos=0
		c=0
		while got_letpos==0:

			edge=[]
			edge_int=[]

			brain = Image.open('brain_temp.png')

			if let_i > 1:
				mx1=mx
				my1=my

			c=c+1
			
			if c > 299:
				restart=1
				break


			if let_i==1:
				mx=random.randint(-300,-150)
				my=random.randint(-100,100)
				mx1=mx
				my1=my

			else:
				mx1=mx+60+random.randint(0,80)
				my1=my+random.randint(-80,80)


			letx=[]
			lety=[]
			for x in range(0,let_w):
				for y in range(0,let_h):
					if let.getpixel((x,y))==(255,255,255,255):
						letx.append(x)
						lety.append(y)


			maxlx=numpy.max(letx)+mx1
			minlx=numpy.min(letx)+mx1
			maxly=numpy.max(lety)+my1
			minly=numpy.min(lety)+my1

			if (minlx,minly) not in roi or (minlx,maxly) not in roi or (maxlx,minly) not in roi or (maxlx,maxly) not in roi:
				continue
			else:

				mort=0

			brain.paste(let, (mx1,my1), mask=let)

			brain1, zz1, zz2 = brain.split()

			lim=5
			masklim=10

			if restart==1:
				break

			edge_col=(85, 85, 85)

			#DRAW EDGE
			for x in range(minlx-10,maxlx+10):
				for y in range(minly-10,maxly+10):

					restart=0
					if brain1.getpixel((x+1,y)) > 250 and brain1.getpixel((x,y)) < 250:

						if  x > minlx+xcut or y > minly+ycut:
							continue

						if (x+1,y) not in roi:
							restart=1
							break

						edge.append((x-3,y))

						for k in range(0,lim):
							brain.putpixel((x-k,y),edge_col)
							edge.append((x-k,y))

						for k in range(0,masklim):
							maskedge.append((x-k,y))

					elif brain1.getpixel((x-1,y)) > 250 and brain1.getpixel((x,y)) < 250:

						if  x > minlx+xcut or y > minly+ycut:
							continue

						if (x-1,y) not in roi:
							restart=1
							break

						edge.append((x+3,y))

						for k in range(0,lim):
							brain.putpixel((x+k,y),edge_col)

							edge.append((x+k,y))

						for k in range(0,masklim):
							maskedge.append((x+k,y))

					elif brain1.getpixel((x,y-1)) > 250 and brain1.getpixel((x,y)) < 250:

						if  x > minlx+xcut or y > minly+ycut:
							continue

						if (x,y-1) not in roi:
							restart=1
							break

						edge.append((x,y+3))

						for k in range(0,lim):
							brain.putpixel((x,y+k),edge_col)
							brain.putpixel((x+1,y+k),edge_col)
							brain.putpixel((x-1,y+k),edge_col)
							brain.putpixel((x+2,y+k),edge_col)
							brain.putpixel((x-2,y+k),edge_col)

							edge.append((x,y+k))
							edge.append((x+1,y+k))
							edge.append((x-1,y+k))
							edge.append((x+2,y+k))
							edge.append((x-2,y+k))

						for k in range(0,masklim):
							maskedge.append((x,y+k))
							maskedge.append((x+1,y+k))
							maskedge.append((x-1,y+k))
							maskedge.append((x+2,y+k))
							maskedge.append((x-2,y+k))


					elif brain1.getpixel((x,y+1)) > 250 and brain1.getpixel((x,y)) < 250:

						#edge_int.append((x,y-k))

						if  x > minlx+xcut or y > minly+ycut:
							continue

						if (x,y+1) not in roi:
							restart=1
							break

						edge.append((x,y-3))

						for k in range(0,lim):
							brain.putpixel((x,y-k),edge_col)
							brain.putpixel((x+1,y-k),edge_col)
							brain.putpixel((x-1,y-k),edge_col)
							brain.putpixel((x+2,y-k),edge_col)
							brain.putpixel((x-2,y-k),edge_col)

							edge.append((x,y-k))
							edge.append((x+1,y-k))
							edge.append((x-1,y-k))
							edge.append((x+2,y-k))
							edge.append((x-2,y-k))

						for k in range(0,masklim):
							maskedge.append((x,y-k))
							maskedge.append((x+1,y-k))
							maskedge.append((x-1,y-k))
							maskedge.append((x+2,y-k))
							maskedge.append((x-2,y-k))

					
		
					if restart==1:
						break

				if restart==1:
					break

			if restart==1:
				break

			#get_fill_pixels
			fill_pix=[]
			for x in range(0,brain_w):
				for y in range(0,brain_h):

					if sum(brain_orig.getpixel((x,y)))>450 and (sum(brain.getpixel((x,y)))>700 or brain.getpixel((x,y))==edge_col):
						fill_pix.append((x,y))


			edge=set(edge)

			hit_edge=0

			edge_overlap=[]

			for edge1 in edge:

				if edges.getpixel(edge1) == 255:
					hit_edge=hit_edge+1

					edge_overlap.append(edge1)

			#print('edge: '+str(hit_edge/len(edge))[:5])

			if hit_edge > len(edge)/(10+c/100):
				#brain.show()
				mx=mx1
				my=my1


				for x in range(minlx-10,maxlx+10):


					for y in range(minly-10,maxly+10):

						if sum(brain.getpixel((x,y)))>700:

							if sum(brain_orig.getpixel((x,y)))<450:

								if x < minlx+xcut and y < minly+ycut:#==(255,255,255):
			

									fill_pix_chk=[fill_pix[i] for i, j in enumerate(fill_pix) if abs(x-j[0])<30 and abs(y-j[1])<30]

									nearest=min(fill_pix_chk, key=lambda z: distance(z, (x,y)))

									hyp=distance((x,y),nearest)

									nearest_fill_col = brain_orig.getpixel(nearest)

						
									brain.putpixel((x,y),(int(nearest_fill_col[0]+10*hyp),int(nearest_fill_col[1]+10*hyp),int(nearest_fill_col[2]+10*hyp)))

							else:

								brain.putpixel((x,y),brain_orig.getpixel((x,y)))

								fill_col=brain_orig.getpixel((x,y))


						elif brain.getpixel((x,y))==edge_col:

							nearest = min(edge_overlap, key=lambda z: distance(z, (x,y)))

							hyp=distance((x,y),nearest)
							#print(hyp)

							
							if hyp>2.8:
								

								if x > minlx+xhole_cut[0][0] and x < minlx+xhole_cut[0][1] and y > minly+yhole_cut[0][0] and y < minly+yhole_cut[0][1]:
									
									continue
								else:
									brain.putpixel((x,y),brain_orig.getpixel((x,y)))

									for k in range(0,8):
										maskedge2.append((x-k,y))
										maskedge2.append((x+k,y))
										maskedge2.append((x,y+k))
										maskedge2.append((x,y-k))


				brain.save('brain_temp.png')
				maskedges=maskedges+maskedge
				break

			else:
				edge=[]
				maskedge=[]
				brain=brain_prev
				continue
				

		if restart==1:
			break
		

	if restart==1:
		print('went off ROI')
		continue

	else:
		break

#brain.show()
brain.save('./input/brain.png')
#brain.save('./input/brain_' + str(date_str) + '.png')

maskedge=list(set(maskedges) - set(maskedge2))

mask = Image.open('black.jpg')
h, w = brain.size

for m in maskedge:

	m1=m[0]
	m2=m[1]

	for k in range(0,6):

		mask.putpixel((m1-k,m2-k),(255, 255, 255))
		mask.putpixel((m1+k,m2+k),(255, 255, 255))
		mask.putpixel((m1+k,m2-k),(255, 255, 255))
		mask.putpixel((m1-k,m2+k),(255, 255, 255))
		

#mask.show()
mask.save('./input/brain_mask.png')

# Let's go, deep art
os.system('python NeuralStyle.py --content_img brain.png --style_imgs carpet_big.png --max_size 500 --max_iterations 100 --original_colors --style_mask --style_mask_imgs brain_mask.png --device /cpu:0 --verbose')










