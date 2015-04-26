#!/usr/bin/env python
import math
import random
import sys
#Generate Random Numbers according to a probability density function
# 
#
#By Ken Leung d2fdydx


# the probility density need to return value >=0 

class PDRandom:
	mFunc=None
	mNumSubDiv=10
	mTarget= 0
	mProgress=0
	#public
	BASE_UNIT=5000

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
	def RandList(self,num, showProg=True):
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

		return temp


	#return a [[x1,x2,.., count]] list
	# 
	# if   binLowerBound <= randomNum < binLowerBound + binWidth, randomNum will be counted for this bin with value = binLowerBound
	#inclusive lowerbound, exclusive upper
	def GetCountList(self,binNum, li):
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
			self.count(countlist,li,binWidth, binNum)
			return countlist


		else:
			binWidth = float(self.mUpper-self.mLower) / binNum
			countlist =[ (self.mLower+ binWidth *i, 0) for i in range(binNum)]
			self.count(countlist,li,binWidth,binNum)
			return countlist

	# output to a file with space speration format
	def OutputCountList(self,countlist, filename , option="w"):
		print ("start: output countlist")
		with open(filename,option) as f :

			if self.mDimension > 1 :
				for item in countlist:
					for i in range(len(item)):
						item[i] = str(item[i])
					line = " ".join(item)
					f.write(line+"\n")

					

			else:
				for tup in countlist:
					line = "%f %d\n"%(tup[0],tup[1])
					f.write(line)
			
			print ("Done: output to %s"%filename)

	# directly output random number to a file
	def OutputRawRandom(self,number, filename, nproc=1):
		print("start: output raw random numbers")
		self.mTarget=number
		self.mProgress=0
		remain = number
		with open(filename, "w") as f:
			while remain >0 :
				if remain < self.BASE_UNIT:
					lis= self.RandList(remain,False)
					self.mProgress += remain
					remain =0

				else:
					lis = self.RandList(self.BASE_UNIT,False)
					remain = remain - self.BASE_UNIT
					self.mProgress= self.mProgress + self.BASE_UNIT

				for item in lis:
					if (self.mDimension >1):
						for i in range(len(item)):
							item[i] = str(item[i])
						line= " ".join(item) + "\n"
					else:
						line = item + "\n"
					f.write(line)

				self.showProgress()
			print ("complete output raw random numbers")

	# gen a count list and output
	def OutputGenCountList (self, number , binNum, filename, nproc=1):
		print ("start: output and gen count list")
		self.mTarget=number
		self.mProgress=0
		remain = number
		
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

			while remain >0 :
				lis=[]
				if remain < self.BASE_UNIT:
					lis= self.RandList(remain,False)
					self.mProgress += remain
					remain =0
				else:
					lis = self.RandList(self.BASE_UNIT,False)
					remain = remain - self.BASE_UNIT
					self.mProgress= self.mProgress + self.BASE_UNIT
				self.count(countlist,lis,binWidth, binNum)
				self.showProgress()
			self.OutputCountList(countlist,filename)


		#============================	
		else:
			binWidth = float(self.mUpper- self.mLower)/binNum
			countlist =[ (self.mLower+ binWidth *i, 0) for i in range(binNum)]
			while remain >0 :
				lis=[]
				if remain < self.BASE_UNIT:
					lis= self.RandList(remain,False)
					self.mProgress += remain
					remain =0
				else:
					lis = self.RandList(self.BASE_UNIT,False)
					remain = remain - self.BASE_UNIT
					self.mProgress= self.mProgress + self.BASE_UNIT
				self.count(countlist,lis,binWidth,binNum)
				self.showProgress()	
			self.OutputCountList(countlist,filename)

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

	def count(self,countlist, lis,binWidth,binNum ):
		if self.mDimension >1:
			for item in lis:
				binIndex=[]
				for d in range(self.mDimension):
					tempBinIndex = int((item[d] - self.mLower[d])/binWidth[d])
					binIndex.append(tempBinIndex)
				globalIndex = self.getGlobalIndex(binIndex,binNum)
				countlist[globalIndex][self.mDimension] = countlist[globalIndex][self.mDimension]  + 1
		#============================	
		else:
			for item in lis:
				binIndex = int((item- self.mLower)/binWidth)
				countlist[binIndex] =(countlist[binIndex][0], countlist[binIndex][1]+1)



# end of class ========================

