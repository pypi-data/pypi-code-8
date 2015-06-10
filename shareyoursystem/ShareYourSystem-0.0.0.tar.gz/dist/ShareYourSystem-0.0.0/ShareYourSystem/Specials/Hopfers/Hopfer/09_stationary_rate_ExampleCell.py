
#ImportModules
import ShareYourSystem as SYS

#Define
MyHopfer=SYS.HopferClass(
	).hopf(
		_LateralWeigthVariable=[[-1.]],
		_StationaryBool=True
	)

#print
print('MyHopfer is ')
SYS._print(MyHopfer) 


