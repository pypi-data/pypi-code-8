import numpy
import os

class fileImport():
    extension='txt'
    description='datas in 2 columns (or 3 with error)'
    icon=None
    comments='#'
    qCol=0
    iCol=1
    errCol=3
    skiprows=0
    
    
    def read(self,filename):
        #read
        data=numpy.loadtxt(filename, comments=self.comments, skiprows=self.skiprows, usecols=(self.qCol,self.errCol))# Load data from a text file.
        data=numpy.transpose(numpy.array(data))
        q=data[qCol]
        i=data[iCol]
        err=data[errCol]
        return q,i,err
        

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