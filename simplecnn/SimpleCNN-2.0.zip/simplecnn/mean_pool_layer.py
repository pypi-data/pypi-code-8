'''
Created on May 9, 2015

@author: Zhengxing Chen
'''
import numpy as np
from pool import mean_pool_unsample_c
import pdb
import img_op as img_op
from pool import mean_pool_ff_c

class MeanPoolLayer(object):
    '''
    A mean pooling layer
    '''

    def __init__(self, pl_dim, input_dim, prev_fltr_num):
        '''
        Constructor
        '''
        self.pl_dim = pl_dim
        self.input_dim = input_dim

        # pooling layer keeps the same number of filters after pooling
        self.prev_fltr_num = prev_fltr_num
        self.fltr_num = prev_fltr_num      
            
        self.init_params()
        
    def init_params(self):
        # Check if input_dim and pl_dim fit well without extra spaces
        if self.input_dim % self.pl_dim != 0:
            raise AttributeError('pooling layer parameters not correct')
        self.output_dim = self.input_dim / self.pl_dim
    
    def feedforward(self, prev_layer_output):
        '''
        Return ff_activation, the max pooling result of this layer
        ff_activation[img_num x fltr_num x output_dim x output_dim]
        prev_layer_output[img_num x prev_fltr_num x prev_output_dim x prev_output_dim]
        '''
        img_num = prev_layer_output.shape[0]
        ff_activation = np.zeros((img_num, self.fltr_num, self.output_dim, self.output_dim))
        
        prev_fltr_num = prev_layer_output.shape[1]
        prev_output_dim = prev_layer_output.shape[2]
        assert prev_output_dim == self.input_dim
        
        # Use Cython code to mean pool
        mean_pool_ff_c(prev_layer_output, ff_activation, self.pl_dim)
        
        # pooling layer doesn't have to store ff_activation or prev_layer_output
        return ff_activation

    def output_params(self):
        print "pooling layer params:"
        print ("pl_dim: %d\ninput_dim: %d\noutput_dim: %d\nprev_fltr_num: %d"
               % (self.pl_dim, self.input_dim, self.output_dim, self.prev_fltr_num))
        print 

    def back_prop(self, prev_layer):
        '''
        First, calculate sensitivity based on previous layer.
        Next, unsampled the sensitivity
        '''
        if prev_layer.__class__.__name__ == "SoftMaxLayer":
            img_num = prev_layer.sensitivity.shape[0]
            # prev_sensitivity[img_num x classes]
            # prev_W[sm_input_dim x classes]
            # sensitivity[img_num x sm_input_dim]
            sensitivity = np.dot(prev_layer.sensitivity, np.transpose(prev_layer.W))
            # sensitivity[img_num x fltr_num x output_dim x output_dim]
            sensitivity.resize(img_num, self.fltr_num, self.output_dim, self.output_dim)
        elif prev_layer.__class__.__name__ == "ConvLayer":
            pass
        
        sensitivity_unsampled = np.zeros((img_num, self.fltr_num, self.input_dim, self.input_dim))
        
        mean_pool_unsample_c(sensitivity, sensitivity_unsampled)
        
        self.sensitivity = sensitivity_unsampled
    
    def update_W_b(self, alpha):
        '''
        Pooling layer doesn't need to update anything
        '''
        pass
        
    def W_L2(self):
        return 0
        
        
        
        
        
        
        