#/###################/#
# Import modules
#


#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Define
MyHopfer=SYS.HopferClass(
	).mapSet(
		{
			'BrianingStepTimeFloat':0.1,
			'-Populations':{
				'|Agent':{
					'LeakingGlobalBool':True,
					'LeakingMaxBool':True,
					'-Traces':{
						'|*U':{
							'RecordingInitStdVariable':0.5
						}
					},
					#'BrianingDebugVariable':100
				}
			}
		}
	).hopf(
		_UnitsInt=100,
		_StdWeightFloat=1.5,
		_SymmetryFloat=-0.7
	).leak(
	).simulate(
		200.
	)


#/###################/#
# View
#

#mapSet
MyHopfer.mapSet(
		{
			'PyplotingFigureVariable':{
				'figsize':(10,8)
			},
			'PyplotingGridVariable':(30,30),
			'-Panels':[
				(
					'|Eigen',
					{
						'PyplotingTextVariable':[-0.6,0.],
						'PyplotingShapeVariable':[10,10],
						'-Charts':{
							'|Perturbation':{
									'PyplotingShiftVariable':[4,0],
								}
							}
					}
				),
				(
					'|Run',
					{
						'PyplotingTextVariable':[-0.4,0.],
						'PyplotingShiftVariable':[0,4],
						'PyplotingShapeVariable':[8,12],
						'-Charts':{
							'|Agent_*U':{
								'PyplotingLegendDict':{
									'fontsize':10,
									'ncol':1
								}
							}
						}
					}
				),
				(
					'|Stat',
					{
						'PyplotingTextVariable':[-0.4,0.],
						'PyplotingShiftVariable':[4,0],
						'PyplotingShapeVariable':[5,9],
					}
				)
			]
		}
	).view(
	).pyplot(
	).show(
	)

#/###################/#
# Print
#

#print
print('MyHopfer is ')
SYS._print(MyHopfer) 
