from numpy import sin, cos, exp, sqrt, log, tan, arccos, arcsin, arctan, sinc, pi

def vx(x,y,t):
	v = y*sin(10*t)
	return v