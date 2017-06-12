import time
class Record:
	def __init__(self, rList = None):
		if rList == None or len(rList) < 11:
			self.id = -1
			self.date = time.strptime('05/01/17', "%m/%d/%y")
			self.time = time.strptime('00:00:01', "%H:%M:%S")
			self.description = 'default'
			self.ip_addr = ''
			self.mac_addr = ''
			self.host_name = ''
			self.vender_class = ''
			self.machine_type = ''
			self.os_type = ''
			self.location = ''
			self.auth1 = ''
			self.auth2 = ''
			self.user_agent_os = ''
			self.user_agent_machine = ''
		else:
			self.id = int(rList[0])
			self.date = time.strptime(rList[1], "%m/%d/%y")
			self.time = time.strptime(rList[2], "%H:%M:%S")
			self.description = rList[3]
			self.ip_addr = rList[4]
			self.mac_addr = rList[5]
			self.host_name = rList[6]
			self.vender_class = rList[7]
			self.machine_type = rList[8]
			self.os_type = rList[9]
			self.location = rList[10]
			self.auth1 = rList[11]
			self.auth2 = rList[12]
			self.user_agent_os = rList[13]
			self.user_agent_machine = rList[14]

	def printRecord():
		print '----------start print----------'
		print 'id: ' + str(self.id)
		print 'time: ' + time.strftime("%Y-%m-%d ",self.date) + time.strftime("%H:%M:%S",self.time)
		print 'description: ' + self.description
		print 'ip: ' + self.ip_addr
		print 'mac: ' + seif.mac_addr
		print 'host: ' + self.host_name
		print 'vender: ' + self.vender_class
		print 'machine: ' + self.machine_type
		print 'os: ' + self.os_type
		print 'location' + self.location
		print '---------- end print ----------'

def readList(file_name):
	f = open(file_name)
	rList = []
	for line in f:
		line = line.strip().split(',')
		record = Record(line)
		rList.append(record)
	f.close()
	return rList

def analyseID(rList,target_id):
	idList = []
	locDict = {}
	for record in rList:
		if record.id == target_id:
			idList.append(record)
			if record.location not in locDict.keys():
				locDict[record.location] = 1
			else:
				locDict[record.location] += 1
	print len(idList)
	for key, value in locDict.iteritems():
		print key + ':' + str(value)
def traverse(rList):
	'''
	osDict = {}
	i = 0
	for record in rList:
		if record.user_agent_machine != '':
			if (record.user_agent_machine == 'iPhone' or record.user_agent_machine == 'IOS-Client') and record.os_type == 'android':
				i += 1
	print i
	'''
	locDict = {}
	for record in rList:
		if record.location != '':
			if record.location not in locDict.keys():
				locDict[record.location] = 1
			else:
				locDict[record.location] += 1
	tot = 0
	tot_v = 0
	for key, value in locDict.iteritems():
		#print str(key) + ' ' + str(value)
		tot += value
		if 'AP' not in key:
			tot_v += value
			print str(key) + ' ' + str(value)
	print tot
	print tot_v


if __name__ == '__main__':
	rList = readList('../dataset/JG/0519.csv')
	#analyseID(rList, 14)
	traverse(rList)
	'''
	date = ['0519','0520','0521','0522','0523','0524','0525']
	for name in date:
		print name
		file_name = '../dataset/JG/' + name + '.csv'
		rList = readList(file_name)
		traverse(rList)
	'''
