from distutils.core import setup

setup(
    name = 'thermistor',
    version = '1.0',
    description = 'Convert thermistor voltage to temperature and associated utilites',
    long_description ="""A class to read temperature from a thermistor.\n
The voltage read-out must be provided by a separate device-dependent package
(see __init__ descriptor for details).\n
The class provides method to retrieve the voltage, resistance or temperature,
to convert the resistance to temperature (B-equation), and to record
the temperature as a function of time (sub-classing threading.Thread to make it
to record in the background).""",
    author = 'Guillaume Lepert',
    author_email = 'guillaume.lepert07@imperial.ac.uk',
    py_modules = ['thermistor']
)
