#!/usr/bin/python3
#shebang is good

import math
import sys
import numpy as np
import scipy.io 
from types import *
from mpl_toolkits.mplot3d import Axes3D
import random

from scipy.optimize import fmin
from scipy.optimize import fmin_cg
from scipy.optimize import fmin_bfgs

import matplotlib.pyplot as plt
import matplotlib as mpl

from plotly.plotly import *
from plotly.graph_objs import *

"""machine learning ex3 assignment"""

class multiClassification:
    def __init__(self, inputs, targets, lmda, numLabel):

        #initialize theta as 0
        self.lmda = lmda
        self.numLabel = numLabel
    
    def sigmoid(self, z):
        return 1/(1+np.exp(-z))
        
    def costFunction(self, theta, inputs, targets):
        trainingNO = inputs.shape[0]
        sigmoid = self.sigmoid(np.dot(inputs, theta))
        theta1 = theta[1:,]
        costJ = ( (np.dot(np.transpose(-targets), np.log(sigmoid))-np.dot(np.transpose(1-targets), np.log(1-sigmoid)))/(trainingNO) + ((self.lmda)/(2*(trainingNO))) * np.dot(np.transpose(theta1),theta1) )
        #print(costJ)
        return costJ
    
    def gradCost(self, theta, inputs, targets):
        trainingNO = inputs.shape[0]
        sigmoid = self.sigmoid(np.dot(inputs, theta))
        sigmoid = sigmoid[:, None]
        #print(sigmoid.shape)
        delta = sigmoid - targets
        theta = theta[:, None]
        #print(theta.shape)
        theta[0,0] = 0
        ta = theta
        thetaJ = ((np.dot(np.transpose(inputs), delta))/(trainingNO))+(ta*(self.lmda)/(trainingNO))
        #the return value of fprime of fmin_cg must be a 1-D array
        return thetaJ.flatten()

    def oneVsAll(self, theta, inputs, targets):
        m = inputs.shape[0]
        n = inputs.shape[1]
        allTheta = np.zeros((self.numLabel, n))
        for i in range(0, self.numLabel):
            y = np.in1d(targets, i)
            y = y[:, None]
            #make y from boolean to int
            y = y+np.zeros((m,1))
            print("i = ", i)
            #when using fmin_cg, the initial value must be 1-D array
            xopt = fmin_cg(self.costFunction, theta, fprime=self.gradCost, args=(inputs, y), gtol=1e-05, maxiter=10)
            #y index 0 1 2 3 4 5 6 7 8 9
            allTheta[i, :] = xopt
        return allTheta

    def predictOneVsAll(self, allTheta, x, y):
        compute = self.sigmoid( np.dot(x, np.transpose(allTheta)) )
        #pick the highest probability
        tmp = np.argmax(compute, axis=1)
        tmp = tmp[:, None]
     
        #compare the predicted and the training example
        result = (tmp == y) 
        return result

    def showDataOneByOne(self, allTheta, x, y):         
        compute = self.sigmoid( np.dot(x, np.transpose(allTheta)) )
        predicted = np.argmax(compute, axis=1)
        predicted = predicted[:, None]
        result = (predicted == y)
        #make y and predicted into a list index by index
        t = list(zip(y, predicted))
        x = x[:,1:] # delete first column(x0) of x
        for k in range(100):
            print("   actual value = ", t[k][0][0]) 
            print("predicted value = ", t[k][1][0])
            
            #fig, ax = plt.subplots(10, 10)
            img_size = math.sqrt(x.shape[1])
            xi = x[k, :].reshape(img_size, img_size).T
            plt.imshow(xi, aspect="auto", cmap="gray")
            plt.show()
        return 1
