import Image
import numpy as np
from Urutu import *

@Urutu("gpu")
def colortoblack(r,g,b,black):
	def average(a,b,c):
		return (a+b+c)/3
	black[tx+bx*blockDim.x] = (r[tx+bx*blockDim.x] + b[tx+bx*blockDim.x] + g[tx+bx*blockDim.x])/3
	return black

def main():
	im = Image.open("image.jpg")
	u,v = im.size[0], im.size[1]
	r = np.zeros(u*v,dtype=np.int)
	b = np.zeros_like(r)
	g = np.zeros_like(r)
	black = np.zeros_like(r)
	for j in range(v):
		for i in range(u):
			r[i+j*u] = im.getpixel((i,j))[0]
			b[i+j*u] = im.getpixel((i,j))[1]
			g[i+j*u] = im.getpixel((i,j))[2]
	out = Image.new('RGB',(u,v),"black")
	colortoblack([u,1,1],[v,1,1],r,g,b,black)
	pixels = out.load()
	for j in range(v):
		for i in range(u):
			pixels[i,j] = (black[i+j*u],black[i+j*u],black[i+j*u])
	out.save("black_gpu.jpg")

if __name__ == '__main__':
	main()

