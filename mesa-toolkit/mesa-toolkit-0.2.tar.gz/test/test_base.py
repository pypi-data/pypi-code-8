import unittest

from mesa import base

# python -m unittest test_base

class MesaTest(unittest.TestCase):

 def setUp(self):
  self.concrete = base.Casa('example.concrete')

 # test all classes get loaded
 def test_all_classes_loaded(self):
  self.assertEqual( self.concrete.casa.keys(), {'Bike','Bus','Car'} )

 # test dynamic update
 def test_new_class_loaded(self):
  import os
  # create some new file in concrete
  trike = './example/concrete/trike.py'
  with open(trike,'w') as f:
   f.write('''
from example import interface

class Trike(interface.Vehicle):
 def __init__(self):
  print('trike init')

 def horn(self):
  print ('tingaling!')

 def get_engine_size(self):
  return 0.01
''')
  self.concrete.rebuild()
  self.assertTrue( 'Trike' in self.concrete.casa.keys() )
  os.remove(trike)
  self.concrete.rebuild()

 # test function calls
 def test_generate_functions(self):
  self.assertEqual( {x[1] for x in self.concrete.generate('get_engine_size')}, {1,2,10} )

if __name__ == '__main__':
 unittest.main()