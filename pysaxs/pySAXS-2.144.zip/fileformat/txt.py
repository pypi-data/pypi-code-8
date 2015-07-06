from pySAXS.fileformat import fileimport

class txt(fileimport.fileImport):
    extension='txt'
    description='datas in 2 columns (or 3 with error)'
    icon=None
    comments='#'
    qCol=0
    iCol=1
    errCol=3
    skiprows=0
    
