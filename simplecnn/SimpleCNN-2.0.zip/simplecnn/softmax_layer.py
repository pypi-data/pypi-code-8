'''
Created on May 9, 2015

@author: Zhengxing Chen
'''
import numpy as np
import pdb
import math
import scipy.io

class SoftMaxLayer(object):
    '''
    classdocs
    '''
    
    # softmax has fltr_num = 1 
    fltr_num = 1

    def __init__(self, output_dim, input_dim, prev_fltr_num):
        '''
        Constructor
        '''
        self.output_dim = output_dim
        self.input_dim = input_dim
        self.prev_fltr_num = prev_fltr_num
        
        self.init_params()
        
    def init_params(self):
        # Make all prev outputs into an 1D input to the softmax layer
        self.sm_input_dim = self.input_dim * self.input_dim * self.prev_fltr_num
        
        # TODO why use r
        r  = np.sqrt(6) / np.sqrt(self.output_dim + self.sm_input_dim + 1);
        self.W = np.random.randn(self.sm_input_dim, self.output_dim) * 2 * r - r
        self.b = np.zeros(self.output_dim)
        
    def output_params(self):
        print "softmax layer params:"
        print ("output_dim: %d\ninput_dim: %d\nprev_fltr_num: %d" 
               % (self.output_dim, self.input_dim, self.prev_fltr_num))
        print "W[sm_input_dim  x output_dim]:"
        print self.W
        print "b[output_dim]:"
        print self.b
        print
    
    def feedforward(self, prev_layer_output):
        '''
        Return ff_activation, the softmax probabilities of classes for images
        ff_activation[img_num x output_dim]
        prev_layer_output[img_num x prev_fltr_num x prev_output_dim x prev_output_dim]
        '''
        img_num = prev_layer_output.shape[0]
        ff_activation = np.zeros((img_num, self.output_dim))
        
        # Reshape prev_layer_output to fit softmax layer
        # sm_input_dim = prev_fltr_num x prev_output_dim x prev_output_dim
        prev_layer_output_reshape = np.reshape(prev_layer_output, (img_num, self.sm_input_dim))
        
        for img_index in range(img_num):
            # img is an 1D array
            img = prev_layer_output_reshape[img_index, :]
            # Reshaped prev_layer_output should match softmax layer's weights
            assert img.shape[0] == self.W.shape[0]
            
            # Need to squeeze self.b to apply element-wise addition
            probs = np.dot(img, self.W) + self.b
            probs = np.exp(probs)
            probs = probs / np.sum(probs)
            
            assert 1 - sum(probs) < 0.001                        # probs should sum to 1
            ff_activation[img_index, :] = probs 
        
        self.prev_layer_output = prev_layer_output_reshape       # used for back propagation   
        self.ff_activation = ff_activation                       
         
        return ff_activation
    
    decay_lambda = 0.003         # weight decay
    
    def back_prop(self, labels):
        '''
        We don't use next_layer in softmax layer because it is the last layer 
        
        self.prev_layer_output[img_num x sm_input_dim]
        self.W[sm_input_dim, output_dim]
        self.ff_activation[img_num x output_dim]
        self.sensitivity[img_num x output_dim]
        '''
        # Should have same number of images
        assert labels.shape[0] == self.ff_activation.shape[0]
        img_num = self.ff_activation.shape[0]
        
        # one_hot_matrix[img_num x output_dim]
        one_hot_matrix = np.zeros((self.ff_activation.shape))
        one_hot_matrix[range(img_num), labels] = 1
        
        sensitivity = self.ff_activation - one_hot_matrix
        
        W_grad_all_imgs = np.dot(np.transpose(self.prev_layer_output), sensitivity) 
        W_grad = (1. / img_num) * W_grad_all_imgs + self.decay_lambda * self.W  
        b_grad = (1. / img_num) * np.sum(sensitivity, axis = 0)
        
        self.sensitivity = sensitivity
        self.W_grad = W_grad
        self.b_grad = b_grad
    
    def update_W_b(self, alpha):
        assert self.W_grad.shape == self.W.shape
        self.W = self.W - alpha * self.W_grad
        self.b = self.b - alpha * self.b_grad
        
    def neg_log_prob_y_sum(self, labels):
        '''
        Return sum of -log(prob_y) for calculating the cost function
        labels[img_num]
        '''
        # Both should contain information from the same number of images
        assert labels.shape[0] == self.ff_activation.shape[0]
        
        neg_log_prob_y_sum = 0
        for img_idx in range(labels.shape[0]):
            cls = labels[img_idx]
            prob_y = self.ff_activation[img_idx, cls]
            # Natural logrithm
            neg_log_prob_y_sum -= math.log(prob_y)
        
        return neg_log_prob_y_sum
        
    def W_L2(self):
        '''
        Return weights^2 for calculating the cost function
        '''
        return np.sum(self.W ** 2)
    
    def accuracy(self, labels):
        '''
        Calculate accuracy given labels information
        labels[img_num]
        '''
        assert labels.shape[0] == self.ff_activation.shape[0]
        
        correct_cnt = 0
        for img_idx in range(labels.shape[0]):
            cls = np.argmax(self.ff_activation[img_idx, :])
            if labels[img_idx] == cls:
                correct_cnt += 1
        
        return correct_cnt * 1. / labels.shape[0]
                
        
    
    
    
        