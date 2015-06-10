#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Simulation time
SimulationTimeFloat=150.
#SimulationTimeFloat=0.2
BrianingDebugVariable=0.1 if SimulationTimeFloat<0.5 else 25.

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
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Fast':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					},
					#'LeakingNoiseStdVariable':0.01
				}),
				('|Decoder',{
					'RecordingLabelVariable':[0],
					#'BrianingDebugVariable':BrianingDebugVariable
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
		_DynamicBool=True,
		_JacobianVariable={
			'ModeStr':"Track",
			'ConstantTimeFloat':30. #(ms)
		},
		_CommandVariable="#custom:#clock:50*ms:1.*mV*int(t==50*ms)",
		_DecoderVariable=[5.],
		_InteractionStr="Rate"
	).simulate(
		SimulationTimeFloat
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



