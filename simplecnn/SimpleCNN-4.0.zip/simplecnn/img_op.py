'''
Created on May 9, 2015

@author: Zhengxing Chen
'''
import scipy.signal as sci

def correlate(image, fltr):
    '''
    Correlate image and fltr and return results without zero paddings
    '''
    return sci.correlate(image, fltr, 'valid')
    
    