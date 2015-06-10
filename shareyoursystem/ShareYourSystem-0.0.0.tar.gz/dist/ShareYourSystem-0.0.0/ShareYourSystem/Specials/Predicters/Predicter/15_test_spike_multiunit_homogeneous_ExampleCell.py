#/###################/#
# Import modules
#


#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#set
BrianingDebugVariable=25.

#Define
MyPredicter=SYS.PredicterClass(
	).mapSet(
		{
			'BrianingStepTimeFloat':0.05,
			'-Populations':[
				('|Sensor',{
					'LeakingMonitorIndexIntsList':[0],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Encod':{
							'BrianingDebugVariable':BrianingDebugVariable
						}
					}
				}),
				('|Agent',{
					'LeakingMonitorIndexIntsList':[0,1],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Fast':{
							'BrianingDebugVariable':BrianingDebugVariable
						}
					},
					#'LeakingNoiseStdVariable':0.01
					#'LeakingThresholdMethodStr':'filterSpikespace'
				}),
				('|Decoder',{
					'LeakingMonitorIndexIntsList':[0],
					#'BrianingDebugVariable':BrianingDebugVariable
					'-Interactions':{
						'|Slow':{
							'BrianingDebugVariable':BrianingDebugVariable,
							#'LeakingWeigthVariable':0.
						}
					}
				})
			]
		}
	).predict(
		_AgentUnitsInt=100,
		_CommandVariable="#custom:#clock:20*ms:1.*mV+1.*mV*int(t==20*ms)",#2.,
		_DecoderVariable="#array",
		_DecoderStdFloat=0.,
		_DecoderMeanFloat=2.,
		#_AgentResetVariable=-60.5
		_InteractionStr="Spike"
	).simulate(
		50.
	)

#/###################/#
# View
#

MyPredicter.mapSet(
		{
			'PyplotingFigureVariable':{
				'figsize':(10,8)
			},
			'PyplotingGridVariable':(30,30),
			'-Panels':[
			]
		}
	).view(
	).pyplot(
	).show(
	)


#/###################/#
# Print
#

#Definition the AttestedStr
print('MyPredicter is ')
SYS._print(MyPredicter) 

