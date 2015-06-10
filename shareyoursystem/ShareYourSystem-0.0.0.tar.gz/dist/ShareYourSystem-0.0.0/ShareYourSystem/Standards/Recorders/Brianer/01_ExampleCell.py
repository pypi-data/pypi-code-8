#/###################/#
# Import modules
#


#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Definition an instance
MyBrianer=SYS.BrianerClass(
	).mapSet(
		{
			'BrianingNeurongroupDict':{
				'N':10,
				'model':
				'''
					dv/dt = (-(v+60*mV)+11*mV + 5.*mV*sqrt(20.*ms)*xi)/(20*ms) : volt
				''',
				'threshold':'v>-50*mV',
				'reset':'v=-70*mV'
			},
			'-Traces':{
				'|v':{
					'NumscipyingStdFloat':0.001,
					'-Samples':{
						'|Default':{
							'RecordingLabelVariable':[0,1],
							'ViewingXScaleFloat':1000.,
							'ViewingYScaleFloat':1000.						
						}
					}
				}
			},
			'-Events':{
				'|Default':{
				}
			}
		}	
	).brian(
	)
	
#/###################/#
# Do one simulation
#

MyBrianer.simulate(
		500.
	)

#/###################/#
# View
#

"""
MyBrianer[
		'/-Traces/|*v/-Samples/|Default'
	].view(
	).pyplot(
	).show(
	)
"""

"""
MyBrianer['/-Events/|Default'].view(
	).pyplot(
	).show(
	)
"""

MyBrianer.view(
	).pyplot(
	).show(
	)

#/###################/#
# Print
#

#Definition the AttestedStr
print('MyBrianer is ')
SYS._print(MyBrianer) 


