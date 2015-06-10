#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Simulation time
SimulationTimeFloat=50.
#SimulationTimeFloat=0.2
BrianingDebugVariable=0.1 if SimulationTimeFloat<0.5 else 2.

#Define
MyPredicter=SYS.PredicterClass(
	).mapSet(
		{
			'BrianingStepTimeFloat':0.05,
			'-Populations':[
				('|Sensor',{
					'RecordingLabelVariable':[0],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Encod':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					}
				}),
				('|Agent',{
					'RecordingLabelVariable':[0],
					'LeakingNoiseStdVariable':0.05,
					'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Fast':{
							'BrianingDebugVariable':BrianingDebugVariable
						}
					},
					#'LeakingNoiseStdVariable':0.01
				}),
				('|Decoder',{
					'RecordingLabelVariable':[0],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Slow':{
							#'BrianingDebugVariable':BrianingDebugVariable,
							#'LeakingWeigthVariable':0.
						}
					}
				})
			]
		}
	).predict(
		_AgentUnitsInt=1,
		_JacobianVariable={
			'ModeStr':"Track",
			'ConstantTimeFloat':2. #(ms)
		},
		_CommandVariable="#custom:#clock:50*ms:1.*mV+1.*mV*int(t==50*ms)",#2.,
		_DecoderVariable=[1.],
		_InteractionStr="Spike",
		_FastPlasticBool=True,
		#_AgentResetVariable=-60.5
	).simulate(
		SimulationTimeFloat
	)

#/###################/#
# View
#

MyPredicter.mapSet(
		{
			'PyplotingFigureVariable':{
				'figsize':(10,10)
			},
			'PyplotingGridVariable':(35,30),
			'-Panels':[
			]
		}
	).view(
	).pyplot(
	).show()


#/###################/#
# Print
#

#Definition the AttestedStr
print('MyPredicter is ')
SYS._print(MyPredicter) 


