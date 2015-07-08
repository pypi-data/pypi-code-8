#!/usr/bin/python3
#shebang is good

import sys
import numpy as np
from scipy.optimize import fmin
import matplotlib.pyplot as plt
import matplotlib as mpl
from plotly.plotly import *
from plotly.graph_objs import *
from types import *
from mpl_toolkits.mplot3d import Axes3D
import random

"""machine learning ex2 assignment"""

class logisticClassification:
    
    def __init__(self, inputs, targets):
        print("init logisticClassification...")

    def mapFeature(self, x1, x2):
        degree = 6
        out = np.array(np.ones((x1.shape[0], 1))) 
        for i in range(1, degree+1):
            for j in range(i+1):
                r = (x1**(i-j)) * (x2**j)
                r = r[:, None]
                out = np.concatenate((out, r), axis=1)
        return out

    def sigmoid(self, z):
        return 1/(1+np.exp(-z))
        
    def costFunction(self, theta, inputs, targets):
        trainingNO = inputs.shape[0]
        inputs = np.concatenate((np.ones((trainingNO, 1)), inputs), axis=1)
        sigmoid = self.sigmoid(np.dot(inputs, theta))
        return ( (np.dot(np.transpose(-targets), np.log(sigmoid))-np.dot(np.transpose(1-targets), np.log(1-sigmoid)))/trainingNO )

    def mapFeatureCostFn(self, theta, inputs, targets, lmda):
        trainingNO = inputs.shape[0]
        sigmoid = self.sigmoid(np.dot(inputs, theta))
        theta1 = theta[1:,]
        return ( (np.dot(np.transpose(-targets), np.log(sigmoid))-np.dot(np.transpose(1-targets), np.log(1-sigmoid)))/trainingNO + (lmda/(2*trainingNO)) * np.dot(np.transpose(theta1),theta1) )
    
    def plotDecisionBoundry(self, theta):
        u = np.linspace(-1, 1.2, 50)
        v = np.linspace(-1, 1.2, 50)
        u = u[:, None]
        v = v[:, None]
        z = np.zeros((u.shape[0], v.shape[0])) 
        for i in range(len(u)):
            for j in range(len(v)):
                self.mapFeature(np.array(u[i]), np.array(v[j]))
                z[i, j] = self.sigmoid(np.dot(self.mapFeature(np.array(u[i]), np.array(v[j])),(np.array(theta))) )
        u, v = np.meshgrid(u, v)
        z = np.transpose(z)
        plt.contour(u, v, z, levels=[0.499999])
