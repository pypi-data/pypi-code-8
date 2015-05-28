"""A class to read temperature from a thermistor.

The voltage read-out must be provided by a separate device-dependent package
(see __init__ descriptor for details).

The class provides method to retrieve the voltage, resistance or temperature,
to convert the resistance to temperature (B-equation), and to record
the temperature as a function of time, optionally in a background thread.

(c) Guillaume Lepert, Imperial College London, 2015. Public domain.
"""

import threading
import numpy as np
import time

class Thermistor(object):
  def __init__(self, ai, bias=0.1, B=3977.0, T0=298.15, R0=10.0, kelvin=False):
    """The default parameters are for NTC thermistor R = 10kohm at 25C, B=3977K.
    
    *args:
      ai: voltage analog input. Must be callable, so that ai() returns the voltage in V across the thermistor.
    **kwargs:
      - bias: thermistor bias current, in mA (default 0.1 mA). 
      - B (K), TO (K), R0 (kohms): B-equation coefficients
      - kevin: returns the temperature in K if True. Default is to use C (False).
    """
    super(Thermistor, self).__init__()
    self.ai = ai
    self.B = B
    self.T0 = T0
    self.R0 = R0
    self.kelvin = kelvin  # True if temperature to be returned in K
    self.bias = bias  # bias current in mA
    
  def voltage(self):
    """Return the voltage across thermistor, in V."""
    return self.ai()
    
  def resistance(self):
    """Return the thermistor resistance, in kohms."""
    return self.voltage() / self.bias
    
  def temperature(self):
    """Return the temperature, in C or K."""
    return self.R_to_T(self.resistance())
    
  def R_to_T(self, R):
    """Convert the resistance R (in kohms, float or numpy array) to temperature."""
    return 1/(1/self.T0 + (1/self.B) * np.log(R/self.R0)) - (0 if self.kelvin else 273.15)
  
  def record_voltage(self, dt):
    """Record the voltage every dt (in seconds), in main thread.
    
    set running = False to stop.
    """
    self.data = []
    self.running = True
    while self.running:
      self.data.append((time.time(), self.ai()))
      time.sleep(dt)
  
  def _record(self, dt):
    """Record the temperature every dt (in seconds), in main thread.
    
    Use run() instead to use a background thread.
    
    Ctrl + C to stop.
    """
    self.data = []
    self.running = True
    try:
      while self.running:
        self.data.append((time.time(), self.temperature()))
        time.sleep(dt)
    except KeyboardInterrupt:
      self.running = False
    self.data = np.array(self.data)	# convert list of (t, T) tuples to numpy array
      
  def record(self, dt=1, thread=True):
    """Record the temperature in fixed time intervals.
    
    **kwargs:
      - dt: the time step, in seconds (default: 1s)
      - thread: if True (default), runs in a background thread.
                  -> Set running = False or call stop() to stop the acquisition.
                If False, runs in the main thread.
                  -> Ctrl+C to stop the acquisition.
    """
    if thread:
      self.thread = threading.Thread(target=self._record, args=(dt,))
      self.thread.start()
    else:
      self._record(dt)