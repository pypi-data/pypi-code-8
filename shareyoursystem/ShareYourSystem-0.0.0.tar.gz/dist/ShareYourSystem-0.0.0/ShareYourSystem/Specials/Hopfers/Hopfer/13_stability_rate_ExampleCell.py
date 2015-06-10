
#ImportModules
import ShareYourSystem as SYS

#Define
MyHopfer=SYS.HopferClass(
	).hopf(
		_LateralWeigthVariable=[[-150.]],
		_DelayTimeVariable=0.001,
		_DoStabilityBool=True
	)

#print
print('MyHopfer is ')
SYS._print(MyHopfer) 


"""
#Define
MyHopfer=SYS.HopferClass(
	).hopf(
		_LateralWeigthVariable=[
			[0.5,-500.],
			[500.,-10.]
		],
		_DelayTimeVariable=0.001,
		_DoStabilityBool=True
	)

#print
print('MyHopfer is ')
SYS._print(MyHopfer) 
"""