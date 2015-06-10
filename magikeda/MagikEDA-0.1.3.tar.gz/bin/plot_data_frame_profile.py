# -*- coding: utf-8 -*-
"""


"""

import argparse
import sys
import pandas as pd

from magikeda import univar

class MyParser(argparse.ArgumentParser):
    """
        Configura argumentos da linha de comando.
    """
  
    def __init__(self):      
        """
          Configure command line args
        """
        super(MyParser, self).__init__()
        self.add_argument('input_file', help=u'CSV file.')        
        self.add_argument('--sep', default=',', help=u'Separator used in CSV. Default is coma ",".') 
        self.add_argument('--encoding', default='latin1', help=u'File encoding used by the CSV file. Accepts any valid encoding to pass to pandas.read_csv method. Default is "latin1". ') 
  
    def error(self, msg):
        """
            Mostra mensagens de erro quando argumentos passados são errados.
        """
        sys.stderr.write('Erro: %s\n' % msg)
        self.print_help()
        sys.exit(2)
        
        
def _plot_dataframe(data_frame):
    """ """
    pass
        
        
if __name__=='__main__':
    
    # Parse arguments from command line
    parser = MyParser()  
    args = parser.parse_args() 
    
    # Load csv file
    data = pd.read_csv(args.input_file, sep=args.sep, encoding=args.encoding)    
    
    univar.plot_dataframe_profile(data)
    
    print data
    print args.input_file, args.sep, args.encoding
    