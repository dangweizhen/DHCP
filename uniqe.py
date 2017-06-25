if __name__ == '__main__':
	date = ['0519','0520','0521','0522','0523','0524','0525','0526']
	#date = ['0519']
	for day in date:
		print day
		file_name = '../dataset/JG/' + day + '.csv'
		file_out = '../dataset/JG_uniqe/' + day + '.csv'
		f = open(file_name)
		fout = open(file_out,'w')
		lines = f.readlines()
		for i in range(len(lines)):
			#print i
			r = True
			for j in range(i+1, i + 1000):
				if j == len(lines):
					break
				if lines[j] == lines[i]:
					r = False
					break
			if r:
				fout.write(lines[i])

		f.close()
		fout.close()