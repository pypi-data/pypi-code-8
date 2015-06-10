#/###################/#
# Import modules
#

#import
import ShareYourSystem as SYS

#define
MyLifer=SYS.LiferClass(
	).setAttr(
        'LifingTotalStationaryCurrentFloat',
        -50.
    ).lif(
	)


#print
print('MyLifer is')
SYS._print(MyLifer)


