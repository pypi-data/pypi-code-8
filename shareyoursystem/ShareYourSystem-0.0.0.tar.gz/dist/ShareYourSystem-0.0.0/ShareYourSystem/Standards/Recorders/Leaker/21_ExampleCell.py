#/###################/#
# Import modules
#


#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Define
MyLeaker=SYS.LeakerClass(
	).mapSet(
		{
			'-Populations':{
				'|P':{
					'LeakingUnitsInt':1,
					'LeakingSymbolPrefixStr':'V',
					'-Inputs':{
						'|Rest':{
							'LeakingWeightVariable':'#scalar:-60*mV'
						},
						'|External':{
							'LeakingWeightVariable':'#scalar:100*mV'
						}
					},
					'LeakingNoiseStdVariable':0.1,
					'LeakingThresholdVariable':'#scalar:V>-50*mV',
					'LeakingResetVariable':-70.,
					'LeakingRefractoryVariable':2.,
					#'BrianingDebugVariable':100
				}
			}
		}
	).leak(
	)

#/###################/#
# Do one simulation
#

MyLeaker.simulate(
		50.
	)

#/###################/#
# View
#

MyLeaker.mapSet(
		{
			'PyplotingGridVariable':(20,20)
		}
	).view(
	).pyplot(
	).show(
	)
	
#/###################/#
# Print
#

#print
print('MyLeaker is ')
SYS._print(MyLeaker) 

