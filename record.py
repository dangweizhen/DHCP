import time
from draw import * 
def readLoc():
	locDict = {}
	f = open('location_dict.txt')
	for line in f:
		line = line.strip().split(':')
		AP_loc = line[0]
		loc_info = line[1]
		locDict[AP_loc] = loc_info
	f.close()
	return locDict

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

	def printRecord(self):
		print '----------start print----------'
		print 'id: ' + str(self.id)
		print 'time: ' + time.strftime("%Y-%m-%d ",self.date) + time.strftime("%H:%M:%S",self.time)
		print 'description: ' + self.description
		print 'ip: ' + self.ip_addr
		print 'mac: ' + self.mac_addr
		print 'host: ' + self.host_name
		print 'vender: ' + self.vender_class
		print 'machine: ' + self.machine_type
		print 'os: ' + self.os_type
		print 'location: ' + self.location
		print '---------- end print ----------'

def extractLease(rList):
	'''
	given a list of record sorted by time, return all leaseList in a dict, key is ip,mac tunple, value is a list of leases
	'''
	ipDict = {}
	leaseDict = {}
	'''
	construct a dict, ip addr is key and an record list is value
	'''
	for record in rList:
		if record.ip_addr != '':
			ip = record.ip_addr
			if not ipDict.has_key(ip):
				ipDict[ip] = [record]
			else:
				ipDict[ip].append(record)
	'''
	there are only 5 id we concern:
	10(assign):must be start of a lease. When meet, save current lease(if exist) and start to record a new lease
	11(renew):can be start of a lease. When meet, compare mac to decide if it is start
	12(release)16(delete)18(expire):must be end of a lease. When meet, save current lease(if exist) and delete current record
	we do not take 16 into account at 2017.6.7
	'''
	for ip, ipList in ipDict.iteritems():
		currentMac = ''
		recordList = []
		for record in ipList:
			if record.id == 10:
				if len(recordList) != 0 and currentMac != '':
					if leaseDict.has_key((ip, currentMac)):
						leaseDict[(ip, currentMac)].append(recordList)
					else:
						leaseDict[(ip, currentMac)] = [recordList]
				recordList = [record]
				currentMac = record.mac_addr
			elif record.id == 11:
				if record.mac_addr == currentMac:
					recordList.append(record)
				else:
					if len(recordList) != 0 and currentMac != '':
						if leaseDict.has_key((ip, currentMac)):
							leaseDict[(ip, currentMac)].append(recordList)
						else:
							leaseDict[(ip, currentMac)] = [recordList]
					recordList = [record]
					currentMac = record.mac_addr
			elif record.id == 12 or record.id == 18:
				if len(recordList) == 0 or currentMac == '':
					continue
				if record.id == 12 and currentMac != record.mac_addr:
					print 'release error!'
					currentMac = ''
					recordList = []
					continue
				recordList.append(record)
				if leaseDict.has_key((ip, currentMac)):
					leaseDict[(ip, currentMac)].append(recordList)
				else:
					leaseDict[(ip, currentMac)] = [recordList]
				currentMac = ''
				recordList = []
			else:
				continue
		if len(recordList) != 0 and currentMac != '':
			if leaseDict.has_key((ip, currentMac)):
				leaseDict[(ip, currentMac)].append(recordList)
			else:
				leaseDict[(ip, currentMac)] = [recordList]
	return leaseDict

def getTime(record1, record2):
	t1 = record1.time
	t2 = record2.time
	delta = (t2.tm_hour-t1.tm_hour)*3600+(t2.tm_min-t1.tm_min)*60+(t2.tm_sec-t1.tm_sec)
	if delta < 0:
		delta += 24*3600
	if delta < 0:
		record1.printRecord()
		record2.printRecord()
	return 1.0*delta/60

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

def getLeaseLife(leaseDict):
	lengthDict = {}
	for ip, leaseList in leaseDict.iteritems():
		l = len(leaseList)
		if lengthDict.has_key(l):
			lengthDict[l] += 1
		else:
			lengthDict[l] = 1
	for key, value in lengthDict.iteritems():
		print str(key) + ':' + str(value)

def readLocDict(file_name):
	f = open(file_name)
	locDict = {}
	for line in f:
		line = line.strip().split(':')
		loc = line[0]
		place = line[1].split(',')
		for p in place:
			locDict[p] = loc
	return locDict


def getLeaseTime(lease):
	t = getTime(lease[0], lease[-1])
	if lease[-1].id == 10 or lease[-1].id == 11:
		t += 35
	return t

def getLeaseLife(leaseDict):
	timeList = []
	for ip, leaseList in leaseDict.iteritems():
		for lease in leaseList:
			t = getLeaseTime(lease)
			timeList.append(t)
	return timeList


def getLeaseLife_withLoc(leaseDict):
	res = {}
	for ip, leaseList in leaseDict.iteritems():
		for lease in leaseList:
			locList = []
			for record in lease:
				if record.location != '' and locDict.has_key(record.location):
					locList.append(locDict[record.location])
			locList = list(set(locList))
			t = getLeaseTime(lease)
			if len(locList) != 0:
				if res.has_key(locList[0]):
					res[locList[0]].append(t)
				else:
					res[locList[0]] = [t]
	drawCDF(res, 0, 300, 0.01)
	return 

if __name__ == '__main__':
	#rList = readList('../dataset/JG/0520.csv')
	#analyseID(rList, 14)
	#traverse(rList)
	#date = ['0519','0520','0521','0522','0523','0524','0525','0526']
	date = ['0522']
	locDict = readLocDict('location.txt')
	for name in date:
		print name
		file_name = '../dataset/JG_uniqe/' + name + '.csv'
		rList = readList(file_name)
		leaseDict = extractLease(rList)
		getLeaseLife_withLoc(leaseDict)
		



