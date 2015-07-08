"""
machine learning ex1 assignment
inputs and targets must be a 2-D array or greater
the row of inputs must be features
the column of inputs must be training Data
the column of targets must be result of training Data
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from plotly.plotly import *
from plotly.graph_objs import *
from types import *
from mpl_toolkits.mplot3d import Axes3D
import random


class linearRegression:
    def __init__(self, inputs, targets, iterations):
        #initialize theta as 0
        self.theta = np.zeros((inputs.shape[1] + 1, targets.shape[1])) 
        self.iterations = iterations

    def batchGradientDescent(self, inputs, targets, theta, rate):
        trainingNO = inputs.shape[0]
        inputs = np.concatenate((np.ones((trainingNO,1)), inputs), axis=1)
        for n in range(self.iterations):
            hypths = np.dot(inputs, theta)
            theta -= rate*np.dot(np.transpose(inputs), hypths-targets)/(trainingNO)
        return theta
    def computeCost(self, inputs, targets, theta): 
        trainingNO = inputs.shape[0]
        inputs = np.concatenate((np.ones((trainingNO,1)), inputs), axis=1)
        tmp = (np.dot(inputs, theta)-targets)
        return (np.sum(np.multiply(tmp, tmp))/(2*(trainingNO)))
           
    def draw3DCost(self, inputs, targets, theta0, theta1):
        trainingNO = inputs.shape[0]
        inputs = np.concatenate((np.ones((trainingNO,1)), inputs), axis=1)
        theta = np.concatenate((np.matrix(theta0), np.matrix(theta1)), axis=0)
        tmp = (np.dot(inputs, theta)-targets)
        return (np.sum(np.multiply(tmp, tmp))/(2*(trainingNO)))
 
    def featureNormalize(self, inputs):
        mean = np.mean(inputs, axis=0)
        tmp = (inputs - mean)
        std = np.std(tmp, axis=0)
        normalX = tmp/std
        return normalX, mean, std

    def normalEqn(self, inputs, targets):
        trainingNO = inputs.shape[0]
        inputs = np.concatenate((np.ones((trainingNO,1)), inputs), axis=1)
        theta = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(inputs), inputs)), np.transpose(inputs)), targets)
        return theta
