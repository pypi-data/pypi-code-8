'''
Created on May 7, 2015

@author: Zhengxing Chen
'''
import argparse
from mnist_loader import MNIST
import numpy as np
import re
from conv_layer import ConvLayer
from pool_layer import PoolLayer
from mean_pool_layer import MeanPoolLayer
from softmax_layer import SoftMaxLayer
import os
import pdb

# set numpy print option
np.set_printoptions(linewidth = 1000, edgeitems = 5)

class SimpleCNN(object):
    
    def __init__(self, train_data_path, train_label_path, test_data_path, test_label_path, 
                 input_dim, output_dim, layers, mini_batch_size, epoch):
        # use a helper class, MNIST, to parse mnist data
        mndata = MNIST(train_data_path, train_label_path, test_data_path, test_label_path)
        train_images, train_labels = mndata.load_training()
        test_images, test_labels = mndata.load_testing()

        train_images_ndarray = np.reshape(train_images, (-1, input_dim, input_dim)) 
        train_labels_ndarray = np.array(train_labels)
        test_images_ndarray = np.reshape(test_images, (-1, input_dim, input_dim)) 
        test_labels_ndarray = np.array(test_labels)
        
        # images and labels are stored as ndarrays and kept in the SimpleCNN instance
        self.train_images = train_images_ndarray        # [train_images x dim x dim]
        self.train_labels = train_labels_ndarray
        
        # for test
        # self.train_labels[self.train_labels==0] = 10
        # self.train_labels = self.train_labels - 1
        
        self.test_images = test_images_ndarray          # [test_iamges x dim x dim]
        self.test_labels = test_labels_ndarray
        
        self.mini_batch_size = mini_batch_size
        self.epoch = epoch
        
        print layers
        cnn_layers = []
        for layer in layers.split("-"):
            if layer.startswith("C"):
                cv_match = re.match("C\(( ?)(\d+)( ?),( ?)(\d+)( ?),( ?)(\d+)( ?)\)", layer)
                cv_stride = int(cv_match.group(2)) 
                cv_fltr_dim = int(cv_match.group(5))
                cv_fltr_num = int(cv_match.group(8))
                
                # if cnn_layers is empty, input to the ConvLayer is digit images themselves, 
                # which is equivalently an output of a previous layer with one filter and 28 input_dim. 
                # Otherwises, use the fltr_num and output_dim from previous layer
                cv_prev_fltr_num = 1
                cv_input_dim = input_dim
                if len(cnn_layers) != 0:
                    prev_cnn_layer = cnn_layers[len(cnn_layers) - 1]
                    cv_prev_fltr_num = prev_cnn_layer.fltr_num
                    cv_input_dim = prev_cnn_layer.output_dim
                
                cv_layer = ConvLayer(stride=cv_stride, fltr_num = cv_fltr_num, fltr_dim = cv_fltr_dim, 
                                            input_dim = cv_input_dim, prev_fltr_num = cv_prev_fltr_num)    
                cnn_layers.append(cv_layer)
                cv_layer.output_params()
                
            elif layer.startswith("P"):
                pl_match = re.match("P\(( ?)(\d+)( ?)\)", layer)
                pl_dim = int(pl_match.group(2))
                
                # if cnn_layers is empty, input to the PoolLayer is digit images themselves, 
                # which is equivalently an output of a previous layer with one filter and 28 input_dim. 
                # Otherwises, use the fltr_num and output_dim from previous layer
                pl_prev_fltr_num = 1
                pl_input_dim = input_dim
                if len(cnn_layers) != 0:
                    prev_cnn_layer = cnn_layers[len(cnn_layers) - 1]
                    pl_prev_fltr_num = prev_cnn_layer.fltr_num
                    pl_input_dim = prev_cnn_layer.output_dim
                
                # for test
                # pl_layer = PoolLayer(pl_dim = pl_dim, 
                #                     input_dim = pl_input_dim, 
                #                     prev_fltr_num = pl_prev_fltr_num)
                
                pl_layer = MeanPoolLayer(pl_dim = pl_dim, 
                                     input_dim = pl_input_dim, 
                                     prev_fltr_num = pl_prev_fltr_num)
                
                
                cnn_layers.append(pl_layer)
                pl_layer.output_params()
            
            elif layer.startswith("S"):
                # SoftMaxLayer is always the last layer. 
                # So its output_dim equals to output_dim (# of classes)
                sm_output_dim = output_dim
               
                # if cnn_layers is empty, input to the SoftMaxLayer is digit images themselves, 
                # which is equivalently an output of a previous layer with one filter and 28 input_dim. 
                # Otherwises, use the fltr_num and output_dim from previous layer
                sm_prev_fltr_num = 1
                sm_input_dim = input_dim   
                if len(cnn_layers) != 0:
                    prev_cnn_layer = cnn_layers[len(cnn_layers) - 1]
                    sm_prev_fltr_num = prev_cnn_layer.fltr_num
                    sm_input_dim = prev_cnn_layer.output_dim
                    
                sm_layer = SoftMaxLayer(output_dim = sm_output_dim, 
                                        input_dim = sm_input_dim, 
                                        prev_fltr_num = sm_prev_fltr_num)
                
                cnn_layers.append(sm_layer)
                sm_layer.output_params()
                
        self.cnn_layers = cnn_layers
    
    momentum = 0.5        # used for updating gradient
    alpha = 0.05           # used for updating gradient
    decay_lambda = 0.003         # weight decay
    
    def train(self):
        
        train_data_size = self.train_labels.shape[0]
        
        for e in range(self.epoch):
            # Randomly permutate indices of data for minibatch
            rd_train_index = np.random.permutation(train_data_size)       
           
            # Traverse each mini-batch
            for mb in range(0, train_data_size, self.mini_batch_size):
                mb_train_index = rd_train_index[mb:mb+self.mini_batch_size]
                mb_train_data = self.train_images[mb_train_index, :, :]
                mb_train_label = self.train_labels[mb_train_index]
            
                # prev_activation records activation from the previous layer
                # the first layer will take input_images as prev_activation
                # and the prev_fltr_num will be 1 since input images have only 
                # one channel.
                
                # prev_activation[img_num x prev_fltr_num x prev_fltr_dim x prev_fltr_dim]
                prev_activation = mb_train_data.reshape(self.mini_batch_size, 1, input_dim, input_dim)        
                
                for layer in self.cnn_layers:
                    ff_activation = layer.feedforward(prev_activation)
                    prev_activation = ff_activation
                
                # Now prev_activation contains the output unit probabilities from softmax layer
                # prev_activation[img_num x output_dim]
                
                # Suppose probs is the softmax probabilties of an image(\vec(x),y).   (y is label)
                # Cost function: \sum_{mini_batch_size} -log(probs_y) + \lambda / 2 * W^2
                # probs_y is a component of probs with index==y
                
                # Obtain gradients for W and b
                for layer in reversed(self.cnn_layers):
                    # Softmax layer will not use prev_layer because it is the last layer. 
                    # Softmax layer will use image label information however.
                    if layer.__class__.__name__ == "SoftMaxLayer":
                        layer.back_prop(mb_train_label)
                    else:
                        layer.back_prop(next_layer)
                    next_layer = layer
                    print (("Epoch %d, minibatch %d__back_prop:%s") 
                            % (e, (mb / self.mini_batch_size), layer.__class__.__name__))
                
                # Update W and b
                for layer in self.cnn_layers:
                    layer.update_W_b(self.alpha)
            
                # Calculate cost function
                cost_func = 0
                
                # Last layer is softmax layer
                softmax_layer = self.cnn_layers[len(self.cnn_layers) - 1]       
                cost_func = (1. / self.mini_batch_size) * softmax_layer.neg_log_prob_y_sum(mb_train_label)
                
                # For debugging purpose. Keep track how much neg log part contributes to the cost func
                cost_func_neg_log = cost_func
                
                # Also add weights^2 to the cost function
                for layer in self.cnn_layers:
                    cost_func += self.decay_lambda * layer.W_L2()
                        
                # For debugging purpose. Keep track how much weights L2 part contributes to the cost func
                cost_func_W_L2 = cost_func - cost_func_neg_log
                
                # Also calculate accuracy in the current minibatch
                acc = softmax_layer.accuracy(mb_train_label)
                
                print (("Epoch %d, minibatch %d__cost function:%.10f, neg log:%.10f, W_L2:%f. Accuracy: %f") 
                       % (e, (mb / self.mini_batch_size), cost_func, cost_func_neg_log, cost_func_W_L2, acc))
    
    def print_img0(self):
        print "SimpleCNN first image:"
        render = ''
        for row in self.train_images[0]:
            render += "\n"
            for ele in row:
                render += "{:.3f}".format(ele) + " "        # print with precision=3
        print render
        return render

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a simple convolutional neural network.',
                                     epilog="A example of valid command: " + 
                                     "python simple_cnn.py 784 10 C(1,9,20)-P(2)-S 300 \\ 3 " + 
                                     "'C:\workspace\MyMachineLearning\data\\train-images.idx3-ubyte' " + 
                                     "\\ 'C:\workspace\MyMachineLearning\data\\train-labels.idx1-ubyte' " + 
                                     "\\ 'C:\workspace\MyMachineLearning\data\\t10k-images.idx3-ubyte' " + 
                                     "\\ 'C:\workspace\MyMachineLearning\data\\t10k-labels.idx1-ubyte'")
    parser.add_argument('input_n', metavar='input_n', type=int, nargs='?', default=784,
                        help="Number of input units. It should be a square number (in*in)." + 
                        " SimpleCNN only handles square images of fixed size.")
    parser.add_argument('output_n', metavar='output_n', type=int, nargs='?', default=10,
                        help="Number of output units (classes). SimpleCNN only handles fixed number of output units.")
    parser.add_argument('layers', metavar='layers_str', type=str, nargs='?', default='C(1,9,20)-P(2)-S',
                        help="A string concatenating the layers in the CNN. " + 
                        "C(s,d,n): convolution layer with stride=s, dimension=d (the width or height of filter) and number of filters=n. " + 
                        "P(d): max pooling layer with dimension d. " + 
                        "S: softmax layer. Please use hypens to separate layers. " + 
                        "See the example command below.")
    parser.add_argument('mini_batch_size', metavar='mini_batch_size', type=int, nargs='?', default=300,
                        help="The size of mini_batch.")
    parser.add_argument('epoch', metavar='epoch', type=int, nargs='?', default=300, help="The number of epoches")
    parser.add_argument('train_data_path', metavar='train_data_path', type=str, nargs='?', 
                        default=os.path.abspath('../../data/train-images.idx3-ubyte'),
                        help="path to the train data file")
    parser.add_argument('train_label_path', metavar='train_label_path', type=str, nargs='?', 
                        default=os.path.abspath('../../data/train-labels.idx1-ubyte'),
                        help="path to the train label file")
    parser.add_argument('test_data_path', metavar='test_data_path', type=str, nargs='?', 
                        default=os.path.abspath('../../data/t10k-images.idx3-ubyte'),
                        help="path to the test data file")
    parser.add_argument('test_label_path', metavar='test_label_path', type=str, nargs='?', 
                        default=os.path.abspath('../../data/t10k-labels.idx1-ubyte'),
                        help="path to the test label file")
    args = parser.parse_args()

    train_data_path = args.train_data_path        
    train_label_path = args.train_label_path
    test_data_path = args.test_data_path
    test_label_path = args.test_label_path

    # TODO verify input_dim (whether is a square number) and output_dim
    input_dim = int(np.sqrt(args.input_n))
    output_dim = args.output_n
    layers = args.layers
    mini_batch_size = args.mini_batch_size
    epoch = args.epoch
    
    # Initialize SimpleCNN using parsed args
    simple_cnn = SimpleCNN(train_data_path, train_label_path, test_data_path, test_label_path, 
                           input_dim, output_dim, layers, mini_batch_size, epoch)  
    simple_cnn.train()
    
