
import sklearn as sk
import pandas as pd
import numpy as np
import requests
import os
from sklearn import svm
from sklearn import naive_bayes
from sklearn import tree
from sklearn import neighbors
from sklearn import ensemble
from sklearn import model_selection
import math
import collections
import random
import statistics 
import matplotlib.pyplot as plt
import pprint
import sys
from joblib import dump, load

class Predictor : 

    def __init__(self,model = "default"):
        self.clf = load("per/"+str(model)+".joblib") 

    def predict_from_matrix(self,mat):
        m = [np.multiply(mat.ravel(),255)]
        return self.clf.predict(m)[0]
