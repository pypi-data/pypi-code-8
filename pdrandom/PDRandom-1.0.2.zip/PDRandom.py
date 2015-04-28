#!/usr/bin/env python
import math
import random
import sys
import multiprocessing
import os
import os.path
#Generate Random Numbers according to a probability density function
# Distributed under the MIT License.
# see the LICENSE.txt
# 1.0.2
#By Ken Leung 


# the probility density need to return value >=0 

class PDRandom:
	mFunc=None
	mNumSubDiv=10
	mTarget= 0
	mProgress=0
	#public
	BASE_UNIT=10000
	

	#return one random Number
	def Next(self):
		while True:
			if self.mDimension > 1:
				randNum=[random.random() for d in range(self.mDimension)]
				(divIndex,values) = self.getX(randNum)
				if (self.acceptReject(divIndex,values)):
					return values
				

			else:

				randNum = random.random()
				(divIndex,x) = self.getX(randNum)
				if (self.acceptReject(divIndex,x)):
					return x

	#return a list of random numbers
	def RandList(self,num, nproc=1,showProg=True):
		if  nproc >1 :
			return self.multiRandList(num,nproc)


		if (showProg==True):
			print ("start: randlist")
			self.mTarget=num
			self.mProgress=0
		temp=[]
		for i in range(num):
			temp.append(self.Next()) 
			if showProg and (i%self.BASE_UNIT)==0:
				self.mProgress = i
				self.showProgress()
		if showProg:
			self.mProgress=num
			self.showProgress()
			print("")

		return temp


	#return a [[x1,x2,.., count]] list
	# 
	# if   binLowerBound <= randomNum < binLowerBound + binWidth, randomNum will be counted for this bin with value = binLowerBound
	#inclusive lowerbound, exclusive upper
	def GetCountList(self,binNum, li):
		(countlist,binWidth,binNum)= self.initCountList(binNum)		
		self.count(countlist,li,binWidth, binNum)
		return countlist	
		
	#directly generate a countlist
	# support multiprocessing
	def GenCountList(self,num,binNum,nproc=1):
		print ("start: gen count list")
		countlist = self.genCountList(num,binNum,nproc)	
		print ("finish:gen count list")	
		return countlist

	# output to a file with space speration format
	def OutputCountList(self,countlist, filename , foption='w'):
		print ("start: output countlist")
		tempList =[]
		if foption=='a':
			if os.path.isfile(filename):
				with open (filename,'r') as f:
					for line in f:
						tempList.append(line.split(" "))
				self.catCountList(tempList,countlist)



		with open(filename,'w') as f :
			for item in countlist:
				for i in range(len(item)):
					item[i] = str(item[i])
				line = " ".join(item)
				f.write(line+"\n")
			
		print ("finish: output to %s"%filename)

	# directly output random number to a file
	def OutputRawRandom(self,number, filename, nproc=1, foption = 'w'):

		print("start: output raw random numbers")
		self.mTarget=number
		self.mProgress=0
		if nproc > 1 :
			self.multiOutputRawRandom(number,filename,nproc,foption=foption)
			return


		remain = number
		with open(filename, foption) as f:
			while remain >0 :
				if remain < self.BASE_UNIT:
					lis= self.RandList(remain,showProg= False)
					self.mProgress += remain
					remain =0

				else:
					lis = self.RandList(self.BASE_UNIT,showProg= False)
					remain = remain - self.BASE_UNIT
					self.mProgress= self.mProgress + self.BASE_UNIT

				self.outputRandomFile(lis,f)

				self.showProgress()
			print("")
			print ("finish: output raw random numbers")

	# gen a count list and output
	def OutputGenCountList (self, number , binNum, filename,foption='w', nproc=1):
		print ("start: output and gen count list")
		countlist = self.genCountList(number,binNum,nproc)	
		self.OutputCountList(countlist,filename,foption=foption)

		print ("finish: output and gen count list")	


	
	# subdiv: used for finding max in a division
	# divWidth too small -> performance hit
	# divWidth too large -> rejection rate increase -> performance hit
	def __init__(self,func,lower,upper , numDiv, subdiv=100, dimension=1):
		print ("Start initializing")
		self.mDimension=dimension
		if dimension > 1:
			try:
				assert isinstance(lower,list)
				assert isinstance(upper,list)
				assert isinstance(numDiv,list)
				
			except AssertionError:
				sys.stderr.write("not pass a list argument for dimension %d"%(dimension))
				exit(1)
			self.mFunc = func 
			self.mLower =lower
			self.mUpper =upper

			divWidth = [(upper[d]-lower[d])*1.0/numDiv[d] for d in range(dimension)]
			self.mDivWidth = divWidth

			if not isinstance(subdiv,list):
				subdiv = subdiv ** (1.0/dimension)
				subdiv = math.ceil(subdiv)
				self.mNumSubDiv = [int(subdiv) for i in range(dimension)]
				#print self.mNumSubDiv
			else:
				self.mNumSubDiv= [int(num) for num in subdiv ]

			self.mNumDiv=numDiv
			self.mTotalNumDiv =1 
			for num in numDiv:
				self.mTotalNumDiv *= num

			

			#print self.mNumDiv
			
			#print self.mTotalNumDiv
			self.mTarget=self.mTotalNumDiv
			self.mProgress=0

			print ("start: finding maximum")
			self.mMaxs=[]
			for globalIndex in range(self.mTotalNumDiv):
				eachIndex = self.getEachIndex(globalIndex,self.mNumDiv)
				#print eachIndex
				subLower=[i*divWidth[index]+lower[index] for index, i in enumerate(eachIndex)]

				subUpper= [(i+1)*divWidth[index] +lower[index]  for index, i in enumerate(eachIndex)]
			#	print subLower
			#	print subUpper
				self.mMaxs.append(self.findMax(subLower, subUpper))
				if (globalIndex%100)==0:
					self.mProgress=globalIndex
					self.showProgress()

			self.mProgress=self.mTarget
			self.showProgress()
			print(" ")

			#print self.mMaxs
			self.initMapping()	


		else: # dimension =1

			self.mFunc = func 
			self.mLower =lower
			self.mUpper =upper

			self.mDivWidth = float(upper-lower)/numDiv
			divWidth=self.mDivWidth
			self.mNumSubDiv=int(subdiv)

			self.mNumDiv = numDiv
			self.mMaxs=[ self.findMax(i*divWidth+lower, (i+1)*divWidth +lower) for i in range(numDiv)]
			self.initMapping()

		print("Complete initialization")



	# some helper function ======================================
	#
	#
	# finding the local max of a function by discrete method
	def findMax(self, low, upper):

		if (self.mDimension > 1):
			maximum =-1
			divWidth= [float(upper[i] - low[i])/self.mNumSubDiv[i] for i in range(self.mDimension)]
		
			totalNumSubDiv = 1
			numValuePoints= [self.mNumSubDiv[d]+1 for d in range(self.mDimension)]
			for d in range(self.mDimension):
				totalNumSubDiv = totalNumSubDiv * (numValuePoints[d])


			for i in range (totalNumSubDiv):
				values =[]
				eachIndex = self.getEachIndex(i,numValuePoints) 
			
				for d in range(self.mDimension):		
					values.append(eachIndex[d] *divWidth[d] + low[d] )
				temp=self.mFunc(values)	
		
				if i == 0:
					maximum=temp
					continue

				if temp > maximum:
					maximum=temp	


			return maximum
			





		else:
			maximum =-1
			divWidth = float(upper-low)/self.mNumSubDiv
			#print divWidth
			for i in range (self.mNumSubDiv+1):
				temp=self.mFunc(divWidth*i+low)	
				if i == 0:
					maximum=temp
					continue

				if temp > maximum:
					maximum=temp	

	#		print maximum
			return maximum

	# init the mapping of random number	to our range
	def initMapping(self): 
		print("start: init mapping")
		if self.mDimension > 1:
			areas = []
			groupAreas=[]
			self.mMapValues=[]
			
			totalArea=[]
			tempNum =  1
			for d in range(self.mDimension):
				totalArea.append([0 for i in range(tempNum)])
				tempNum = self.mNumDiv[d] * tempNum
				groupAreas.append([0 for i in range(tempNum	)])
				self.mMapValues.append([None for i in range(tempNum)])

			self.mTarget=len(self.mMaxs)
			self.mProgress=0

			for i in range(len(self.mMaxs)):
				temp = self.mMaxs[i]
				for d in range(self.mDimension):
					temp = temp * self.mDivWidth[d]
				areas.append(temp)

				#== 
				eachIndex = self.getEachIndex(i, self.mNumDiv)
				for d in range(self.mDimension):
					# total Area
					if d ==0:
						totalArea[d][0] = totalArea[d][0] + temp
						
					else:
						subEachIndex = []
						subNumDiv =[]
						for d2 in range(d):
							subEachIndex.append(eachIndex[d2])
							subNumDiv.append(self.mNumDiv[d2])
						subGlobalIndex =self.getGlobalIndex(subEachIndex, subNumDiv)
						totalArea[d][subGlobalIndex] = totalArea[d][subGlobalIndex] + temp
					#=========group Area ==============
					subEachIndex=[]
					subNumDiv=[]
					for d2 in range(d+1):
						subEachIndex.append(eachIndex[d2])
						subNumDiv.append(self.mNumDiv[d2])
					subGlobalIndex =self.getGlobalIndex(subEachIndex, subNumDiv)
					groupAreas[d][subGlobalIndex] = groupAreas[d][subGlobalIndex] + temp

				if (i % 1000)==0:
					self.mProgress=i
					self.showProgress()

			self.mProgress=self.mTarget
			self.showProgress()
			print("")


			
			self.mProgress=0	
			self.mTarget = self.mDimension 
			for d in range (self.mDimension):
				self.mTarget *= len(totalArea[d])
			for d in range(self.mDimension):
				for totalIndex, total in enumerate(totalArea[d]):
					if d == 0:
						tempArea = 0
						for index, area in enumerate( groupAreas[d]):
							lowerBound = tempArea
							tempArea = tempArea+area
							self.mMapValues[d][index]=((index,lowerBound/total, area/total))
					else:
						subGlobalIndex = totalIndex 
						subNumDiv=[]
						for d2 in range(d):
							subNumDiv.append(self.mNumDiv[d2])
						subEachIndex = self.getEachIndex(subGlobalIndex,subNumDiv)
						subEachIndex.append(0)
						subNumDiv.append(self.mNumDiv[d])
						tempArea = 0 
						for ownIndex in range (self.mNumDiv[d]):
							subEachIndex[d]=ownIndex
							tempGlobalIndex = self.getGlobalIndex(subEachIndex,subNumDiv)
							lowerBound =tempArea
							tempArea = tempArea + groupAreas[d][tempGlobalIndex]
							self.mMapValues[d][tempGlobalIndex]=((ownIndex,lowerBound/total, groupAreas[d][tempGlobalIndex]/total ))
					self.mTarget+=1
					if (self.mTarget%1000):
						self.showProgress()
			self.mProgress=self.mTarget
			self.showProgress()
			print("")

			return 	


		else:
			#===================D - 1 =======================
			areas =[]
			totalArea=0
			for i in range(len(self.mMaxs)):
				temp = self.mMaxs[i] * self.mDivWidth
				totalArea = totalArea + temp
				areas.append(temp)
		#	print areas
			tempArea =0.0
			self.mMapValues=[]
			for index, area in enumerate(areas):
				lowerBound = tempArea
				tempArea = tempArea+area
				self.mMapValues.append ( (index,lowerBound/totalArea,area/totalArea))

			self.mMapValues= sorted(self.mMapValues,key = lambda mapping:mapping[2],reverse =True )

	#given a rand, return the corresponding value(s) 
	def getX (self,rand):

#		print rand
		if self.mDimension >1 :
			values=[]
			eachIndex =[]
			eachDiv =[]
			globalIndex=0
			for d, ran in enumerate(rand):
				
				if d == 0:
					for  (divIndex,lower, width) in self.mMapValues[d]:
						if ran >= lower and ran < (lower + width):
							tempWidth = ran -lower
							
							values.append(self.mLower[d]+(divIndex+(tempWidth/width)) * self.mDivWidth[d])
							eachIndex.append(divIndex) 
							eachDiv.append(self.mNumDiv[d])

							break
				else:
					eachIndex.append(0)
					eachDiv.append(self.mNumDiv[d])
					for ownIndex in range(self.mNumDiv[d]):
						eachIndex[d]= ownIndex
						globalIndex = self.getGlobalIndex(eachIndex,eachDiv)
						(divIndex,lower, width) = self.mMapValues[d][globalIndex]
						if ran >= lower and ran < (lower + width):
							tempWidth = ran -lower
							values.append(self.mLower[d]+ (divIndex+(tempWidth/width)) * self.mDivWidth[d])
							
							break

				

			#print values
			return  (globalIndex, values)



		else :
			for  (divIndex,lower, width) in self.mMapValues:
				if rand >= lower and rand < (lower + width):
					tempWidth = rand -lower
	#				print str(tempWidth) + " " + str(lower)
					return (divIndex,self.mLower+(divIndex+(tempWidth/width)) * self.mDivWidth )

			print ("error: corresponding x not found")

	def acceptReject(self,divIndex, x):
		if self.mDimension >1:
			for d, value  in enumerate(x):
				if  value >= self.mUpper[d]:
					return False
		else:
			if x >=self.mUpper:
				return False

		randHight = random.random() * self.mMaxs[divIndex]
		funcH = self.mFunc(x) 
		if randHight <= funcH:
			#print "accept: funcH %f v.s. randHight %f"%(funcH,randHight)
			return True
		else:

			#print "reject: funcH %f v.s. randHight %f"%(funcH,randHight)
			return False


	# used for dimension > 1
	def getEachIndex(self,globalIndex, numDiv):
		eIndex=[]
		for d in range(len(numDiv)):
			index = globalIndex% numDiv[d]
			globalIndex= globalIndex - index
			globalIndex = int(globalIndex/numDiv[d])
			eIndex.append(index)
		return eIndex

	def getGlobalIndex(self,eachIndex, numDiv):
		globalIndex = 0	
		for i in range(len(eachIndex)-1,-1, -1):
			if i == 0:
				globalIndex = globalIndex + eachIndex[i]
			else:
				globalIndex = (globalIndex + eachIndex[i]) * numDiv[i-1]

		return globalIndex

	def showProgress(self):
		percentage = float(self.mProgress)/self.mTarget * 100.0
		sys.stdout.write("\r%f%%"%percentage)
		sys.stdout.flush()

	def showProgressM(self, count, Total):
		percentage = float(count)/Total * 100.0
		sys.stdout.write("\r%f%%"%percentage)
		sys.stdout.flush()

	def initCountList(self,binNum):
		if self.mDimension > 1:
			binWidth =[ float(self.mUpper[d]-self.mLower[d])/binNum[d]  for d in range(self.mDimension)]  # binsNum respect to x1,x2,...

			allBins = 1 # all bins counted as 1 dim
			for num in binNum:
				allBins *= num
			countlist=[]

			for i in range(allBins):
				eachIndex = self.getEachIndex(i,binNum)
				temp =[self.mLower[d] + binWidth[d] * eachIndex[d] for d in range(self.mDimension)] 
				temp.append(0)
				countlist.append(temp)
			return (countlist,binWidth,binNum)
		#============================	
		else:
			binWidth = float(self.mUpper- self.mLower)/binNum
			countlist =[ [self.mLower+ binWidth *i, 0] for i in range(binNum)]
			return (countlist,binWidth,binNum)
			

	def count(self,countlist, lis,binWidth,binNum ):
		if self.mDimension >1:
			for item in lis:
				binIndex=[]
				for d in range(self.mDimension):
					tempBinIndex = int((item[d] - self.mLower[d])/binWidth[d])
					binIndex.append(tempBinIndex)
				globalIndex = self.getGlobalIndex(binIndex,binNum)
				countlist[globalIndex][self.mDimension] += 1
		#============================	
		else:
			for item in lis:
				binIndex = int((item- self.mLower)/binWidth)
				countlist[binIndex][-1] +=1


	def genCountList(self, number , binNum, nproc=1):
		if nproc> 1:
			return self.multiOutputGenCountList(number,binNum,nproc)

		self.mTarget=number
		self.mProgress=0
		remain = number
		
		(countlist,binWidth,binNum)= self.initCountList(binNum)		
		while remain >0 :
			lis=[]
			if remain < self.BASE_UNIT:
				lis= self.RandList(remain,showProg= False)
				self.mProgress += remain
				remain =0
			else:
				lis = self.RandList(self.BASE_UNIT,showProg= False)
				remain = remain - self.BASE_UNIT
				self.mProgress= self.mProgress + self.BASE_UNIT
			self.count(countlist,lis,binWidth, binNum)
			self.showProgress()

		print("")
		return countlist

	#helper
	def outputRandomFile(self,lis, f):
		for item in lis:
			if (self.mDimension >1):
				for i in range(len(item)):
					item[i] = str(item[i])
				line= " ".join(item) + "\n"
			else:
				line = str(item) + "\n"
			f.write(line)



	def catCountList(self, payload ,to):
		for i ,count in enumerate(payload):
			to[i][-1] += int(count[-1])
		

	def test_count(self,countlist):
		s =0
		for i in countlist:
			s+=i[-1]
		return s
	#======================= multi Processing =========================
	#
	#
	#
	#

	def multiOutputRawRandom(self, num,filename,nproc,foption='w'):
		
		
		total = num
		re = num
		count = multiprocessing.Value('i',0)
		filenames = [filename+"_tmp_"+str(i) for i in range(nproc)]

		perNum = int(num) /nproc
		remain = num %nproc
		processes =[]

		print ("start running in %d proc"%(nproc))

		for i in range(nproc):
			if i ==0:
				processes.append(multiprocessing.Process(target=self.randomOutputTask, args=(perNum+remain,count,total,filenames[i])))
			else:
				processes.append(multiprocessing.Process(target=self.randomOutputTask, args=(perNum,count,total,filenames[i])))


		for each in processes:
			each.start()
		for each in processes:
			each.join()

		print ("")
		print ("combining tmp files")
		with open (filename,foption) as out:
			for tmpFile in filenames:
				with open(tmpFile,'r') as tmp:
					for line in tmp:
						out.write(line)

		
		#clean up
		for tmpFile in filenames:
			os.remove(tmpFile)

		print ("finish: output raw random")

			
	
		

	def randomOutputTask(self,num,count,total,filename):
		randlist=[]

		num = int(num)
		remain=int(num)
		counter =0
		
		with open (filename,'w') as f:
			for i in range(num):
				randlist.append(self.Next())
				counter +=1
				if (counter%self.BASE_UNIT) ==0:
					
					self.outputRandomFile(randlist,f)	
					randlist=[]
					with count.get_lock():
						count.value+=counter
						self.showProgressM(count.value,total)
					counter =0
			self.outputRandomFile(randlist,f)		
			with count.get_lock():

				count.value+=counter
				self.showProgressM(count.value,total)	
			counter=0



		return num

	def multiOutputGenCountList(self,num, binNum, nproc):
		total = int(num)
		
		count = multiprocessing.Value('i',0)


		perNum = int(num) /nproc
		remain = num %nproc
		processes =[]

		manager = multiprocessing.Manager()
		outputs = manager.list()

		print ("start running in %d proc"%(nproc))

		for i in range(nproc):
			if i ==0:
				processes.append(multiprocessing.Process(target=self.countlistTask, args=(perNum+remain,binNum,count,total,outputs )))
			else:
				processes.append(multiprocessing.Process(target=self.countlistTask, args=(perNum,binNum,count,total,outputs)))


		for each in processes:
			each.start()
		for each in processes:
			each.join()

		print ("")
		print ("combining")

		finallist = outputs[0]
	
	
		
		for i in range(1,nproc):
			self.catCountList(outputs[i],finallist)
		return finallist

	def countlistTask(self,num,binNum,count,total, output):
		remain = int(num)
		num = int(num)	
		(countlist,binWidth,binNum)=self.initCountList(binNum)
		randlist=[]
		while remain >0:
			if remain  < self.BASE_UNIT:
				randlist=self.RandList(remain,showProg=False)
				with count.get_lock():
					count.value+=remain
					self.showProgressM(count.value,total)

				remain =0
			else:
				randlist=self.RandList(self.BASE_UNIT,showProg=False)
				remain -= self.BASE_UNIT
				with count.get_lock():
					count.value+=self.BASE_UNIT
					self.showProgressM(count.value,total)
					
			self.count(countlist,randlist,binWidth,binNum)

			
		output.append(countlist)


	def multiRandList(self, num,nproc):
		total = num
		
		count = multiprocessing.Value('i',0)


		perNum = int(num) /nproc
		remain = num %nproc
		processes =[]

		manager = multiprocessing.Manager()
		outputs = manager.list()

		print ("start running in %d proc"%(nproc))

		for i in range(nproc):
			if i ==0:
				processes.append(multiprocessing.Process(target=self.randomListTask, args=(perNum+remain,count,total,outputs )))
			else:
				processes.append(multiprocessing.Process(target=self.randomListTask, args=(perNum,count,total,outputs)))


		for each in processes:
			each.start()
		for each in processes:
			each.join()

		finallist = outputs[0]
		for i in range(1,nproc):
			finallist.extend(outputs[i])
		return finallist


	def randomListTask(self,num,count,total,outputs):
		remain = int(num)
		num =int(num)	
		randlist=[]
		finallist=[]
		while remain >0:
			if remain  < self.BASE_UNIT:
				randlist=self.RandList(remain,showProg=False)
				with count.get_lock():
					count.value+=remain
					self.showProgressM(count.value,total)

				remain =0
			else:
				randlist=self.RandList(self.BASE_UNIT,showProg=False)
				remain -= self.BASE_UNIT
				with count.get_lock():
					count.value+=self.BASE_UNIT
					self.showProgressM(count.value,total)
					
			finallist.extend(randlist)
		outputs.append(finallist)
		return 
	
# end of class ========================

