'''
Created on May 9, 2015

@author: Zhengxing Chen
'''
import numpy as np
import img_op as img_op
import scipy.special as sci
import pdb
import scipy.io 

class ConvLayer(object):
    '''
    ConvLayer with sigmoid as activation function
    '''

    def __init__(self, stride, fltr_num, fltr_dim, input_dim, prev_fltr_num):
        '''
        Constructor
        '''
        self.stride = stride
        self.fltr_num = fltr_num
        self.fltr_dim = fltr_dim
        self.input_dim = input_dim
        self.prev_fltr_num = prev_fltr_num
        
        # Check if fltr_dim, input_dim and stride fit well without extra space
        if ((self.input_dim - self.fltr_dim) / self.stride) % self.stride != 0:
            raise AttributeError('conv layer parameters not correct')
        self.output_dim = (self.input_dim - self.fltr_dim) / self.stride + 1

        self.init_params()
        
    def init_params(self):
        # TODO why multiply 0.1
        # A filter connects local areas of all filters from previous layers
        self.W = 0.1 * np.random.randn(self.fltr_num, self.prev_fltr_num, self.fltr_dim, self.fltr_dim)
        self.b = np.zeros(self.fltr_num)
        
    def output_params(self):
        print "conv layer params:"
        print ("stride: %d\nfltr_num: %d\nfltr_dim: %d\ninput_dim: %d\nprev_fltr_num:%d\noutput_dim: %d" 
               % (self.stride, self.fltr_num, self.fltr_dim, self.input_dim, self.prev_fltr_num, self.output_dim))
        print "W[fltr_num x prev_fltr_num x fltr_dim x fltr_dim]:"
        print self.W
        print "b[fltr_num]:"
        print self.b 
        print
        
    def feedforward(self, prev_layer_output):
        '''
        Return ff_activation, the feedforward activation of this layer
        ff_activation[img_num x fltr_num x output_dim x output_dim]
        prev_layer_output[img_num x prev_fltr_num x prev_output_dim x prev_output_dim]
        '''
        img_num = prev_layer_output.shape[0]
        ff_activation = np.zeros((img_num, self.fltr_num, self.output_dim, self.output_dim))
        
        prev_fltr_num = prev_layer_output.shape[1]
        prev_output_dim = prev_layer_output.shape[2]
        assert prev_output_dim == self.input_dim
        
        for img_index in range(img_num):
            # img[prev_fltr_num x prev_output_dim, prev_output_dim]
            img = prev_layer_output[img_index, :, :, :]
            
            for fltr_index in range(self.fltr_num):
                # fltr_W[prev_fltr_num x fltr_dim x fltr_dim]
                fltr_W = self.W[fltr_index, :, :, :]
                
                # By default, img_op.correlate returns correlation result with stride=1 and without padding.
                img_convoluted_output = img_op.correlate(img, fltr_W)
                # We extract areas according to the defined stride
                # img_convoluted_output will become a 2D array
                img_convoluted_output = img_convoluted_output[0, ::self.stride, ::self.stride]
                
                # Pass through sigmoid function
                img_convoluted_sigmoid_output = sci.expit(img_convoluted_output)
                ff_activation[img_index, fltr_index, :, :] = img_convoluted_sigmoid_output
        
        self.ff_activation = ff_activation        # Store ff_activation for backpropagation later
        self.input_data = prev_layer_output       # Store prev_layer_output for backpropatation later
        
        return ff_activation
    
    # TODO Python global variable
    decay_lambda = 0.003         # weight decay
    
    def back_prop(self, prev_layer):
        if prev_layer.__class__.__name__ == "PoolLayer" or prev_layer.__class__.__name__ == "MeanPoolLayer":
            # Element-wise multiplication because for each unit in conv_layer:
            # sensitivity_{conv layer} = sensitivity_{pooling layer}*sigmoid'  
            #                          = sensitivity_{pooling_layer}*conv_layer.ff_activation*(1-ff_activation) 
            #
            # prev_layer.sensitivity[img_num x fltr_num x output_dim x output_dim]
            # sensitivity[img_num x fltr_num x output_dim x output_dim]
            self.sensitivity = prev_layer.sensitivity * self.ff_activation * (1 - self.ff_activation)  

            # Calculate W_grad[fltr_num x prev_fltr_num x fltr_dim x fltr_dim]
            # We first intialize W_grad to be of size: [fltr_num x prev_fltr_num x fltr_dim x fltr_dim]
            # so that we can keep track of every image's W_grad
            img_num = self.sensitivity.shape[0]
            W_grad = np.zeros((img_num, self.fltr_num, self.prev_fltr_num, self.fltr_dim, self.fltr_dim))
            # Similarly, we initialize b_grad in a way that we can keep track of every image's b_grad 
            b_grad = np.zeros((img_num, self.fltr_num))
            
            # For each img, we need to obtain W_grad[img, :, :, :, :]
            for img_index in range(img_num):
                for fltr_index in range(self.fltr_num):
                    img_sensitivity = self.sensitivity[img_index, fltr_index]

                    # In order to use img_op.correlate, we need to match the shape
                    # of img_sensitivity and the shape of img_input
                    img_sensitivity = np.expand_dims(img_sensitivity, axis = 0)
                    img_input = self.input_data[img_index, :, :, :]
                    
                    # img_W_grad[prev_fltr_num x fltr_dim x fltr_dim]
                    img_W_grad = img_op.correlate(img_input, img_sensitivity)
                    
                    # This part of code verifies that imp_op.correlate returns correct result to img_W_grad
                    # img_W_grad_prev_fltr = np.zeros(img_W_grad.shape)
                    # for prev_fltr_index in range(self.prev_fltr_num):
                    #    img_fltr_input = self.input_data[img_index, prev_fltr_index, :, :]
                    #    img_W_grad_prev_fltr[prev_fltr_index, :, :] = img_op.correlate(img_fltr_input, np.squeeze(img_sensitivity))
                    
                    W_grad[img_index, fltr_index, :, :, :] = img_W_grad
                    b_grad[img_index, fltr_index] = np.sum(img_sensitivity)
            
            # Calculate W_grad[fltr_num x prev_fltr_num x fltr_dim x fltr_dim] by aggregating along img axis
            W_grad = W_grad.sum(axis = 0)
            assert W_grad.shape == self.W.shape
            
            # Calculate b_grad[fltr_num] by aggregating along img axis
            b_grad = b_grad.sum(axis = 0)
            assert b_grad.shape == self.b.shape
            
            self.W_grad = (1. / img_num) * W_grad + self.decay_lambda * self.W    
            self.b_grad = (1. / img_num) * b_grad
            
        elif prev_layer.__class__.__name__ == "ConvLayer":
            pass
        elif prev_layer.__class__.__name__ == "SoftMaxLayer":
            pass
        
    def update_W_b(self, alpha):
        assert self.W_grad.shape == self.W.shape
        assert self.b_grad.shape == self.b.shape
        self.W = self.W - alpha * self.W_grad
        self.b = self.b - alpha * self.b_grad
        
    def W_L2(self):
        '''
        Return weights^2 for calculating the cost function
        '''
        return np.sum(self.W ** 2)
        
        
        
        
        
        
        