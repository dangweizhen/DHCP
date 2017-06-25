import matplotlib.pyplot as plt  
import numpy as np
def drawCDF(dict, start, end, step, save = False, filename = 'figure.png'):
	for label, l in dict.iteritems():
		l = sorted(l)
		length = len(l)
		last = 0
		count = 0
		x = []
		y = []
		st = start
		ed = end
		while st <= ed:
			x.append(st)
			while last < length and l[last] < st:
				last += 1
			y.append(1.0*last/length)
			st += step
		plt.plot(x,y,label=label)
	plt.figure(1)
	plt.grid()
	plt.legend(loc = 'lower right')
	if save:
		plt.savefig(filename)
	plt.show()
	return 
"""
def drawCDF(l, st, step, ed, save = False, filename = 'figure.png'):
	l = sorted(l)
	length = len(l)
	last = 0
	count = 0
	x = []
	y = []
	while st <= ed:
		x.append(st)
		while last < length and l[last] < st:
			last += 1
		y.append(1.0*last/length)
		st += step
	plt.plot(x,y)
	cur = 1
	curList = []
	'''
	for i in range(0,len(y)):
		while y[i] >= 1.0*cur/10000:
			curList.append((1.0*cur/10000,x[i]))
			cur+=1
		else:
			continue
	for item in curList:
		print item
	'''
	plt.figure(1)
	plt.grid()
	if save:
		plt.savefig(filename)
	plt.show()

"""
if __name__ == '__main__':
	l = range(0,100)
	for i in range(0,100):
		l.append(50)
	drawCDF(l, 0, 1, 100)