import numpy
import os

class fileImport():
    
    def __init__(self):
        self.extension='txt'
        self.description='datas in 2 columns (or 3 with error)'
        self.icon=None
        self.comments='#'
        self.qCol=0
        self.iCol=1
        self.errCol=2
        self.skiprows=0
        self.q=None
        self.i=None
        self.err=None
        self.data=None
        
    def read(self,filename):
        #read
        print self.qCol
        self.data=numpy.loadtxt(filename, comments=self.comments, skiprows=self.skiprows)#, usecols=(self.qCol,self.errCol))# Load data from a text file.
        self.data=numpy.transpose(numpy.array(self.data))
        self.q=self.data[self.qCol]
        self.i=self.data[self.iCol]
        self.err=self.data[self.errCol]
        return self.q,self.i,self.err
        

def import_list():
        """ List all python modules in specified plugins folders """
        l=[]
        print __file__
        print os.path.dirname(__file__)
        for filename in os.listdir(os.path.dirname(__file__)):
                name, ext = os.path.splitext(filename)
                #print name
                if ext.endswith(".py"):
                    if name!='fileimport' and name!='__init__':
                        l.append(name)
        return l