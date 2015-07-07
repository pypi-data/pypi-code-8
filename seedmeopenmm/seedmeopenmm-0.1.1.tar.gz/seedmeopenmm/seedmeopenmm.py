"""
seedmerepoter.py: Outputs data about a simulation to seedme

This is a adaptation of the OpenMM molecular simulation tool statedatareporter.py
"""

__author__ = "Sebastian Amara"
__version__ = "1.0"

import simtk.openmm as mm
import simtk.unit as unit
import math
import time
import seedme # import the seedme module

class SeedMeStateDataReporter(object):
    """SeedMeStateDataReporter outputs information about a simulation, such as energy and temperature, to a new SeedMe collection.

    To use it, create a SeedMeStateDataReporter, then add it to the Simulation's list of reporters.  The set of
    data to write is configurable using boolean flags passed to the constructor.  By default the data is
    written in comma-separated-value (CSV) format, but you can specify a different separator to use.
    """

    def __init__(self, collection, reportInterval, step=False, time=False, potentialEnergy=False, kineticEnergy=False, totalEnergy=False, temperature=False, volume=False, density=False,
                 progress=False, remainingTime=False, speed=False, separator=',', systemMass=None, totalSteps=None):
        """Create a SeedMeReporter.

        Parameters:
         - collection (string) The name of the collection to write to.
         - reportInterval (int) The interval (in time steps) at which to write frames
         - step (boolean=False) Whether to write the current step index to the file
         - time (boolean=False) Whether to write the current time to the file
         - potentialEnergy (boolean=False) Whether to write the potential energy to the file
         - kineticEnergy (boolean=False) Whether to write the kinetic energy to the file
         - totalEnergy (boolean=False) Whether to write the total energy to the file
         - temperature (boolean=False) Whether to write the instantaneous temperature to the file
         - volume (boolean=False) Whether to write the periodic box volume to the file
         - density (boolean=False) Whether to write the system density to the file
         - progress (boolean=False) Whether to write current progress (percent completion) to the file.
           If this is True, you must also specify totalSteps.
         - remainingTime (boolean=False) Whether to write an estimate of the remaining clock time until
           completion to the file.  If this is True, you must also specify totalSteps.
         - speed (bool=False) Whether to write an estimate of the simulation speed in ns/day to the file
         - separator (string=',') The separator to use between columns in the file
         - systemMass (mass=None) The total mass to use for the system when reporting density.  If this is
           None (the default), the system mass is computed by summing the masses of all particles.  This
           parameter is useful when the particle masses do not reflect their actual physical mass, such as
           when some particles have had their masses set to 0 to immobilize them.
         - totalSteps (int=None) The total number of steps that will be included in the simulation.  This
           is required if either progress or remainingTime is set to True, and defines how many steps will
           indicate 100% completion.
        """
        self._reportInterval = reportInterval
        
        self._obj = seedme.SeedMe()
        result = self._obj.create_collection(title=collection)
        
        self._my_cid = self._obj.get_id(result)
        if not self._my_cid:
            print("Abort: Collection id not found in: " + result)
            exit(1)
        url = self._obj.get_url(result)
        print("Collection url is: " + url)  
               
        if (progress or remainingTime) and totalSteps is None:
            raise ValueError('Reporting progress or remaining time requires total steps to be specified')
        
        self._step = step
        self._time = time
        self._potentialEnergy = potentialEnergy
        self._kineticEnergy = kineticEnergy
        self._totalEnergy = totalEnergy
        self._temperature = temperature
        self._volume = volume
        self._density = density
        self._progress = progress
        self._remainingTime = remainingTime
        self._speed = speed
        self._separator = separator
        self._totalMass = systemMass
        self._totalSteps = totalSteps
        self._hasInitialized = False
        self._needsPositions = False
        self._needsVelocities = False
        self._needsForces = False
        self._needEnergy = potentialEnergy or kineticEnergy or totalEnergy or temperature

    def describeNextReport(self, simulation):
        """Get information about the next report this ect will generate.

        Parameters:
         - simulation (Simulation) The Simulation to generate a report for
        Returns: A five element tuple.  The first element is the number of steps until the
        next report.  The remaining elements specify whether that report will require
        positions, velocities, forces, and energies respectively.
        """
        steps = self._reportInterval - simulation.currentStep%self._reportInterval
        return (steps, self._needsPositions, self._needsVelocities, self._needsForces, self._needEnergy)

    def report(self, simulation, state):
        """Generate a report.

        Parameters:
         - simulation (Simulation) The Simulation to generate a report for
         - state (State) The current state of the simulation
        """
        if not self._hasInitialized:
            self._initializeConstants(simulation)
            headers = self._constructHeaders()
            self._obj.add_ticker(self._my_cid, '#"%s"' % ('"'+self._separator+'"').join(headers))
          
            self._initialClockTime = time.time()
            self._initialSimulationTime = state.getTime()
            self._initialSteps = simulation.currentStep
            self._hasInitialized = True

        # Check for errors.
        self._checkForErrors(simulation, state)

        # Query for the values
        values = self._constructReportValues(simulation, state)

        # Write the values.
        self._obj.add_ticker(self._my_cid, self._separator.join(str(v) for v in values))

    def _constructReportValues(self, simulation, state):
        """Query the simulation for the current state of our observables of interest.

        Parameters:
         - simulation (Simulation) The Simulation to generate a report for
         - state (State) The current state of the simulation

        Returns: A list of values summarizing the current state of
        the simulation, to be printed or saved. Each element in the list
        corresponds to one of the columns in the resulting CSV file.
        """
        values = []
        box = state.getPeriodicBoxVectors()
        volume = box[0][0]*box[1][1]*box[2][2]
        clockTime = time.time()
        if self._progress:
            values.append('%.1f%%' % (100.0*simulation.currentStep/self._totalSteps))
        if self._step:
            values.append(simulation.currentStep)
        if self._time:
            values.append(state.getTime().value_in_unit(unit.picosecond))
        if self._potentialEnergy:
            values.append(state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole))
        if self._kineticEnergy:
            values.append(state.getKineticEnergy().value_in_unit(unit.kilojoules_per_mole))
        if self._totalEnergy:
            values.append((state.getKineticEnergy()+state.getPotentialEnergy()).value_in_unit(unit.kilojoules_per_mole))
        if self._temperature:
            values.append((2*state.getKineticEnergy()/(self._dof*unit.MOLAR_GAS_CONSTANT_R)).value_in_unit(unit.kelvin))
        if self._volume:
            values.append(volume.value_in_unit(unit.nanometer**3))
        if self._density:
            values.append((self._totalMass/volume).value_in_unit(unit.gram/unit.item/unit.milliliter))
        if self._speed:
            elapsedDays = (clockTime-self._initialClockTime)/86400.0
            elapsedNs = (state.getTime()-self._initialSimulationTime).value_in_unit(unit.nanosecond)
            if elapsedDays > 0.0:
                values.append('%.3g' % (elapsedNs/elapsedDays))
            else:
                values.append('--')
        if self._remainingTime:
            elapsedSeconds = clockTime-self._initialClockTime
            elapsedSteps = simulation.currentStep-self._initialSteps
            if elapsedSteps == 0:
                value = '--'
            else:
                estimatedTotalSeconds = (self._totalSteps-self._initialSteps)*elapsedSeconds/elapsedSteps
                remainingSeconds = int(estimatedTotalSeconds-elapsedSeconds)
                remainingDays = remainingSeconds//86400
                remainingSeconds -= remainingDays*86400
                remainingHours = remainingSeconds//3600
                remainingSeconds -= remainingHours*3600
                remainingMinutes = remainingSeconds//60
                remainingSeconds -= remainingMinutes*60
                if remainingDays > 0:
                    value = "%d:%d:%02d:%02d" % (remainingDays, remainingHours, remainingMinutes, remainingSeconds)
                elif remainingHours > 0:
                    value = "%d:%02d:%02d" % (remainingHours, remainingMinutes, remainingSeconds)
                elif remainingMinutes > 0:
                    value = "%d:%02d" % (remainingMinutes, remainingSeconds)
                else:
                    value = "0:%02d" % remainingSeconds
            values.append(value)
        return values

    def _initializeConstants(self, simulation):
        """Initialize a set of constants required for the reports

        Parameters
        - simulation (Simulation) The simulation to generate a report for
        """
        system = simulation.system
        if self._temperature:
            # Compute the number of degrees of freedom.
            dof = 0
            for i in range(system.getNumParticles()):
                if system.getParticleMass(i) > 0*unit.dalton:
                    dof += 3
            dof -= system.getNumConstraints()
            if any(type(system.getForce(i)) == mm.CMMotionRemover for i in range(system.getNumForces())):
                dof -= 3
            self._dof = dof
        if self._density:
            if self._totalMass is None:
                # Compute the total system mass.
                self._totalMass = 0*unit.dalton
                for i in range(system.getNumParticles()):
                    self._totalMass += system.getParticleMass(i)
            elif not unit.is_quantity(self._totalMass):
                self._totalMass = self._totalMass*unit.dalton

    def _constructHeaders(self):
        """Construct the headers for the CSV output

        Returns: a list of strings giving the title of each observable being reported on.
        """
        headers = []
        if self._progress:
            headers.append('Progress (%)')
        if self._step:
            headers.append('Step')
        if self._time:
            headers.append('Time (ps)')
        if self._potentialEnergy:
            headers.append('Potential Energy (kJ/mole)')
        if self._kineticEnergy:
            headers.append('Kinetic Energy (kJ/mole)')
        if self._totalEnergy:
            headers.append('Total Energy (kJ/mole)')
        if self._temperature:
            headers.append('Temperature (K)')
        if self._volume:
            headers.append('Box Volume (nm^3)')
        if self._density:
            headers.append('Density (g/mL)')
        if self._speed:
            headers.append('Speed (ns/day)')
        if self._remainingTime:
            headers.append('Time Remaining')
        return headers

    def _checkForErrors(self, simulation, state):
        """Check for errors in the current state of the simulation

        Parameters
         - simulation (Simulation) The Simulation to generate a report for
         - state (State) The current state of the simulation
        """
        if self._needEnergy:
            energy = (state.getKineticEnergy()+state.getPotentialEnergy()).value_in_unit(unit.kilojoules_per_mole)
            if math.isnan(energy):
                raise ValueError('Energy is NaN')
            if math.isinf(energy):
                raise ValueError('Energy is infinite')
                
    def _del_(self):
        print('deleting')
