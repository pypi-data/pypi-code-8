'''
Created on May 7, 2015

@author: Zhengxing Chen
'''
import argparse
from mnist_loader import MNIST
import numpy as np


class SimpleCNN(object):
    def __init__(self, args):
        train_data_path = args.train_data_path        
        train_label_path = args.train_label_path
        test_data_path = args.test_data_path
        test_label_path = args.test_label_path
        input_dim = int(np.sqrt(args.input_n))
        
        mndata = MNIST(train_data_path, train_label_path, test_data_path, test_label_path)
        train_images, train_labels = mndata.load_training()
        test_images, test_labels = mndata.load_testing()
        
        train_images_ndarray = np.reshape(train_images, (-1, input_dim, input_dim)) / 255
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a simple convolutional neural network.', 
                                     epilog="A example of valid command:\rpython simple_cnn.py 784 10 C-P-S " + 
                                     "\\ 'C:\workspace\MyMachineLearning\data\\train-images.idx3-ubyte' " + 
                                     "\\ 'C:\workspace\MyMachineLearning\data\\train-labels.idx1-ubyte' " + 
                                     "\\ 'C:\workspace\MyMachineLearning\data\\t10k-images.idx3-ubyte' " +
                                     "\\ 'C:\workspace\MyMachineLearning\data\\t10k-labels.idx1-ubyte'")
    parser.add_argument('input_n', metavar='input_n', type=int, nargs='?', default=784,
                        help="number of input units. It should be a square number (in*in). SimpleCNN only handles square images of fixed size.")
    parser.add_argument('output_n', metavar='output_n', type=int, nargs='?', default=10,
                        help="number of output units (classes). SimpleCNN only handles fixed number of output units.")
    parser.add_argument('layers', metavar='layers', type=str, nargs='?', default='C-P-S',
                        help="a string concatenating the layers in the CNN. C: convolution layer. P: pooling layer. S: softmax layer. Please use hypens to separate layers.")
    parser.add_argument('train_data_path', metavar='train_data_path', type=str, nargs='?', default='C:\\workspace\\MyMachineLearning\\data\\train-images.idx3-ubyte', 
                        help="path to the train data file")
    parser.add_argument('train_label_path', metavar='train_label_path', type=str, nargs='?', default='C:\\workspace\\MyMachineLearning\\data\\train-labels.idx1-ubyte',
                        help="path to the train label file")
    parser.add_argument('test_data_path', metavar='test_data_path', type=str, nargs='?', default='C:\\workspace\\MyMachineLearning\\data\\t10k-images.idx3-ubyte',
                        help="path to the test data file")
    parser.add_argument('test_label_path', metavar='test_label_path', type=str, nargs='?', default='C:\\workspace\\MyMachineLearning\\data\\t10k-labels.idx1-ubyte',
                        help="path to the test label file")
    args = parser.parse_args()

    print args
    SimpleCNN(args)        # Initialize SimpleCNN using parsed args
    
    
