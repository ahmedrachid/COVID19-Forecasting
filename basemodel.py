
import pandas as pd
import os
import numpy as np
from scipy import optimize
from scipy import integrate
from scipy.integrate import odeint


class BaseModel():

    def __init__(self,*params_init):
        self.params_init = params_init
        self.params_ = None
        self.params_cov_ = None
        self.X_fit = None
        

    def sir_model(self, y, x, *params):
        
        raise NotImplementedError()

    def fit_odeint(self, x, *params):
        return integrate.odeint(self.sir_model, self.params_init, x, args = params)[:,1]

    def fit(self, X, y):
        popt, pcov = optimize.curve_fit(self.fit_odeint, X, y)
        fitted = self.fit_odeint(X, *popt)
        self.X_fit = fitted
        self.params = popt
        return self

    def predict(self, x):
        return integrate.odeint(self.sir_model, self.params_init, x, args= self.params)

