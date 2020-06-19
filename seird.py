import pandas as pd
import os
import numpy as np
from scipy import optimize
from scipy import integrate
from scipy.integrate import odeint

from basemodel import BaseModel

class SEIRDModel(BaseModel):
    """
    SEIR MODEL

    """
    def __init__(self, beta_init=0.1, gamma_init=0.3, delta_init = 1/3, alpha_init = 0.15, rho_init = 0.1, N = 70* 10**6, i0 = 1):
        self.beta_0 = beta_init
        self.gamma_0 = gamma_init
        self.delta_0 = delta_init
        self.alpha_0 = alpha_init
        self.rho_0 = rho_init
        self.beta_ = None
        self.gamma_ = None
        self.delta_ = None
        self.alpha_ = None
        self.rho_ = None
        self.N = N
        self.i0 = 1
        self.s0 = self.N - self.i0
        self.r0 = 0
        self.e0 = 1
        self.d0 = 0        
        
    def seird_model(self, y, x, beta, gamma, delta, alpha, rho):
        sus = -beta * y[0] * y[2] / self.N
        expo = beta * y[0] * y[2] / self.N - delta * y[1]   
        inf = delta * y[1] - (1-alpha) * gamma * y[2] - alpha * rho * y[2]
        rec = (1-alpha) * gamma * y[2]
        death = alpha * rho * y[2]
        return sus, expo, inf, rec, death

    def fit_odeint(self, x, beta, gamma, delta, alpha, rho):
        return integrate.odeint(self.seird_model, (self.s0, self.e0, self.i0, self.r0, self.d0), x, args=(beta, gamma, delta, alpha, rho))[:,1]

    def fit(self, X, y):
        popt, pcov = optimize.curve_fit(self.fit_odeint, X, y)
        fitted = self.fit_odeint(X, *popt)
        self.X_fit = fitted
        self.beta = popt[0]
        self.gamma = popt[1]
        self.delta = popt[2]
        self.alpha = popt[3]
        self.rho = popt[4]
        return self

    def predict(self, x):
        return integrate.odeint(self.seird_model, (self.s0, self.e0, self.i0, self.r0, self.d0), x, args=(self.beta, self.gamma, self.delta, self.alpha, self.rho)).T