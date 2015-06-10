#ImportModules
import ShareYourSystem as SYS

#Define
MyHopfer=SYS.HopferClass(
    ).mapSet(
        {
            'HopfingDelayTimeVariable':0.001,
            'HopfingDoStabilityBool':True,
            'PyplotingMarkerVariable':'#direct:o',
            'PyplotingColorVariable':SYS.GetClass(
            	lambda __SelfVariable:
            	"black" if __SelfVariable.HopfedIsStableBool else "red"
            )
        }
    )

#hopf and plot
VariablesList=map(
        lambda __IndexInt:
        MyHopfer.setAttr(
            'HopfingLateralWeigthVariable',
            SYS.numpy.array(
                [0.5]+list(
                	SYS.numpy.array(
                		[
                			SYS.numpy.sqrt(
                				1200000.*SYS.scipy.stats.uniform.rvs()
                			)
                		]*2
                    )*SYS.numpy.array(
                    	[-1.,1.]
                    )
                )+[
                		-3000.*SYS.scipy.stats.uniform.rvs()
                	]
                ).reshape(
                    (2,2)
                )
            ).hopf(
            ).pyplot(
                '>>-self.HopfingLateralWeigthVariable[0,1]*self.HopfingLateralWeigthVariable[1,0]',
                '>>-self.HopfingLateralWeigthVariable[1,1]',
            ).setSwitch('pyplot'),
        xrange(1000)
    )
SYS.show()