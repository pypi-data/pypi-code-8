from pySAXS.fileformat import fileimport

class swing(fileimport.fileImport):
    def __init__(self):
        self.extension='dat'
        self.description='swing dat file from nx'
        self.qCol=0
        self.iCol=1
        self.errCol=2
        self.skiprows=32
    
