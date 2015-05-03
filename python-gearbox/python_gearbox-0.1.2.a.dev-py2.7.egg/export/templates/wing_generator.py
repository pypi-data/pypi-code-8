'''
Created on 19/06/2014

@author: vinicius@esss.com.br

based on: 
- http://en.wikipedia.org/wiki/NACA_airfoil
- http://groups.google.com/group/SketchUp3d/browse_thread/thread/68865aa2fc881e30/26a9ccea8c3c9af1?#26a9ccea8c3c9af1
'''
import math
import locale
import cStringIO

    
#===================================================================================================
# WingGenerator
#===================================================================================================
class WingGenerator(object):
    '''
    NACA wing profile generator.
    
    This code generates the coordinates of a wing using the NACA formulae. Such coordinates are written
    in a CSV file format used by ANSYS to import data curves.
    Additionally, it also writes the required code to 
    '''


    def __init__(self, numberOfPoints=25):
        '''
        Constructor
        
        :param numberOfProfiles: number of profiles
        :param numberOfPoints: nu
        '''

        self._numberOfPoints = numberOfPoints
        
        self._defaultNumberOfProfiles = 3
        self._defaultNacaProfile = (4, 4, 12, 1.0)
        self._defaultWingLength = 3.0
        
        self._output = cStringIO.StringIO()
        
        self._profiles = {}
        
    def configureDefaultProfiles(self):
        '''
        Configures the profiles using default values.
        '''
        distBetweenProfiles = self._defaultWingLength / self._defaultNumberOfProfiles
        
        for i in xrange(self._defaultNumberOfProfiles + 1):
            name = "Profile%d" % i
            pos = i * distBetweenProfiles
            self._profiles[name] = (self._defaultNacaProfile, pos)
            
    
    def addProfile(self, name, m, p, t, s=1.0, pos=1):
        '''
        Add a profile. This profile will compose the wing at the given position. In addition, it
        can be scaled (up or down).
        
        :param name: profile name
        :param m: maximum chamber, relative to chord
        :param p: position (tenths) of maximum chamber
        :param t: thickness, relative to chord
        :param s: scale factor
        :param pos: profile position (from a reference plane)
        '''
        self._profiles[name] = ((m, p, t, s), pos)
    
    
    def _generateProfile(self, m=4, p=4, t=12, s=1.0):
        '''
        Generates the NACA profile, using the given parameters.
        
        :param m: maximum chamber, relative to chord
        :param p: position (tenths) of maximum chamber
        :param t: thickness, relative to chord
        :param s: scale factor
        '''
        _m = m / 100.0
        _p = p / 10.0
        _t = t / 100.0
        
        x = []
        yt = []
        yc = []
        xu = []
        yu = []
        xl = []
        yl = []
        
        last_x = 0.0
        last_yc = 0.0
        for n in xrange(self._numberOfPoints):
            
            _x = 1 - math.cos(math.radians(n) * (90.0 / (self._numberOfPoints - 1)))
            x.append(_x)
            
            _yt = (_t / 0.2) * (0.2969 * math.sqrt(_x) - 0.126 * _x - 0.3516 * _x ** 2 + 0.2843 * _x ** 3 - 0.1015 * _x ** 4) 
            yt.append(_yt)
            
            if _x < _p:
                _yc = (_m / _p ** 2) * (2 * _p * _x - _x ** 2)
            else:
                _yc = (_m / (1 - _p) ** 2) * ((1 - 2 * _p) + 2 * _p * _x - _x ** 2)
            yc.append(_yc)
            
            if n > 0:
                delta_x = _x - last_x
                last_x = _x
                 
                delta_yc = _yc - last_yc
                last_yc = _yc 
                
                theta = math.atan(delta_yc / delta_x)
    
                _xu = _x - _yt * (math.sin(theta))
                _yu = _yc + _yt * (math.cos(theta))
                _xl = _x + _yt * (math.sin(theta))
                _yl = _yc - _yt * (math.cos(theta))
            else:
                _xu = 0
                _yu = 0
                _xl = 0
                _yl = 0
                
            xu.append(_xu * s)
            yu.append(_yu * s)
            xl.append(_xl * s)
            yl.append(_yl * s)
        
        # Close the trailing edge
        close_x = (xu[-1] + xl[-1]) / 2.0 
        close_y = (yu[-1] + yl[-1]) / 2.0 
        xu[-1] = close_x
        xl[-1] = close_x
        yu[-1] = close_y
        yl[-1] = close_y

        return xu, yu, xl, yl
        
        
    def writeCoorfinatesFile(self, filename, xu, yu, xl, yl, z=0, group=1):
        '''
        Auxiliar method. Used to export the profile to a file. This file could be later read by
        DesignModeller
        
        :param filename: the file name
        :param xu: the X coordinates for the upper curve of the wing
        :param yu: the Y coordinates for the upper curve of the wing
        :param xl: the X coordinates for the lower curve of the wing
        :param yl: the Y coordinates for the lower curve of the wing
        :param z: the Z coordinate
        :param group: the group ID
        '''
        out = open(filename, "w")
        
        out.write("# List of Point Coordinates\n\n")
        out.write("# Format is integer Group, integer ID, then X Y Z all\n")
        out.write("# delimited by spaces, with nothing after the Z value.\n\n")
        
        line_fmt = "%d\t%d\t%10.5f%10.5f%10.5f\n"
        
        # Sets the locale for all categories to the users default setting 
        locale.setlocale(locale.LC_ALL, '')
        
        out.write("# Group\n")
        
        # Loop the points, starting from the beginning: upper curve
        for i, val in enumerate(zip(xu, yu)):
            x, y = val  
            line = locale.format_string(line_fmt, (group, i + 1, x, y, z))
            out.write(line)
        
        # Loop in the opposite direction: lower curve
        for i, val in enumerate(reversed(zip(xl, yl))):
            x, y = val
            line = locale.format_string(line_fmt, (group + 1, self._numberOfPoints + i + 1, x, y, z))
            out.write(line)
        
        out.close()


    def _writeNewPlane(self, planeName, offset=0.0):
        self._output.write("""
function do%s ()
{
    // Get the reference Plane (in this case, the XY plane)
    var planeXY = agb.GetXYPlane();
    var Yes = agc.Yes;
    var No  = agc.No;
    
    var newPlane = agb.PlaneFromPlane(planeXY);
    if (newPlane)
    {
      newPlane.Name = "%s";
      newPlane.ReverseNormal = No;
      newPlane.ReverseAxes = No;
      newPlane.ExportCS = No;
      newPlane.AddTransform(agc.XformZOffset, %f);
    }
    
    agb.regen();
    
    return newPlane;
}
""" % (planeName, planeName, offset))


    def _writeNacaProfileOnPlane(self, planeName, nacaProfile=None):
        '''
        Writes the profile creation function.
        
        :param planeName: the plane name
        :param nacaProfile: the Naca profile
        '''
        
        if nacaProfile == None:
            xu, yu, xl, yl = self._generateProfile(*self._defaultNacaProfile)
        else:
            xu, yu, xl, yl = self._generateProfile(*nacaProfile)
        
        self._output.write("""
function doSketches%s (plane)
{
    p = new Object();
    
    //Plane
    agb.SetActivePlane (plane);
    p.Plane  = agb.GetActivePlane();
    p.Origin = p.Plane.GetOrigin();
    p.XAxis  = p.Plane.GetXAxis();
    p.YAxis  = p.Plane.GetYAxis();

    //Sketch
    p.Sk1 = p.Plane.NewSketch();
    p.Sk1.Name = "Sketch%s";

    //Edges
    with (p.Sk1)
    {   
""" % (planeName, planeName))
        
        # concatenates the coordinates (but first inverse the coordinates from lower curve)
        # additionally, here I suppress the last point from the upper curve, which is equal to the
        # first point from the lower curve
        xl.reverse()
        yl.reverse()
        x = xu[:-1] + xl
        y = yu[:-1] + yl
        coords = zip(x, y)
        
        for idx in xrange(len(coords) - 1):
            _x, _y = coords[idx]
            x_, y_ = coords[idx + 1]
            self._output.write("\t\tp.Ln7 = Line(%10.5f, %10.5f, %10.5f, %10.5f);\n" % (_x, _y, x_, y_))

        self._output.write("""
    }
    
    agb.Regen();
    
    return p;
}
""")

    
    def _writeCreatePlaneFromSketch(self, planeName):
        '''
        Writes the commands for the plane creation (must be called after the functions definition)
        
        :param planeName: the plane name
        '''
        self._output.write("pl%s = do%s ();\n" % (planeName, planeName))
        sketchName = "sk%s" % planeName
        self._output.write("%s = doSketches%s (pl%s);\n\n" % (sketchName, planeName, planeName))
        
        return sketchName
    
    
    def _writeSkinOperation(self, skinName, sketches):
        '''
        Writes the commands for the Skin operation
        
        :param skinName: the skin name
        :param sketches: a list with the sketches which will form the wing 
        '''
        self._output.write("var Skin1 = agb.Skin(agc.Add, agc.No, 0.0, 0.0);\n")
        self._output.write('Skin1.Name = "%s";\n' % skinName)
        
        for sketchName in sketches: 
            self._output.write("Skin1.AddBaseObject(%s.Sk1);\n" % sketchName)
        self._output.write("agb.Regen()")
        
   
    def writeScript(self):
        '''
        Writes the JScript that builds the wing to the output.
        '''
        
        profileNames = self._profiles.keys()
        profileNames.sort()
        sketches = []
        
        for profileName in profileNames:
            profileData = self._profiles[profileName]
            planeName = "Plane" + profileName
            nacaProfile, position = profileData
            
            self._writeNewPlane(planeName, offset=position)
            self._writeNacaProfileOnPlane(planeName, nacaProfile)
            sketchName = self._writeCreatePlaneFromSketch(planeName)
            sketches.append(sketchName)
            
        self._writeSkinOperation("Skin", sketches)
            
        contents = self._output.getvalue()
        self._output.close()
        
        return contents

#===================================================================================================
# Main
#===================================================================================================
if __name__ == '__main__':
    
    ng = WingGenerator()
    
    # ng.configureDefaultProfiles()
    ng.addProfile("P01", 0, 4, 12, 1.0, 0)
    ng.addProfile("P02", 2, 4, 12, 0.7, 2)
    ng.addProfile("P03", 4, 4, 12, 0.5, 4)
    ng.addProfile("P04", 4, 6, 06, 0.4, 6)
    
    jscript = ng.writeScript()
    
    SetScriptVersion(Version="15.0")
    
    # Gets the System
    geomSystem = GetSystem(Name="Geom")
    geometryComponent = geomSystem.GetContainer(ComponentName="Geometry")
    geometryComponent.Edit(Interactive=False)
    geometryComponent.SendCommand(Command=jscript)
    
    Update()
    
