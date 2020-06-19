import pandas as pd
import os
import numpy as np
from scipy import optimize
from scipy import integrate
from scipy.integrate import odeint

from basemodel import BaseModel


class SIRModel(BaseModel):
    """
    SIR MODEL

    """
    def __init__(self, beta_init=0.1, gamma_init=0.3, N = 70* 10**6, i0 = 1):
        self.beta_0 = beta_init
        self.gamma_0 = gamma_init
        self.beta_ = None
        self.gamma_ = None
        self.N = N
        self.i0 = 1
        self.s0 = self.N - self.i0
        self.r0 = 0

     
    def sir_model(self, y, x, beta, gamma):
        sus = -beta * y[0] * y[1] / self.N
        rec = gamma * y[1]
        inf = -(sus + rec)
        return sus, inf, rec

    def fit_odeint(self, x, beta, gamma):
        return integrate.odeint(self.sir_model, (self.s0, self.i0, self.r0), x, args=(beta, gamma))[:,1]

    def fit(self, X, y):
        popt, pcov = optimize.curve_fit(self.fit_odeint, X, y)
        fitted = self.fit_odeint(X, *popt)
        self.X_fit = fitted
        self.beta = popt[0]
        self.gamma = popt[1]
        return self

    def predict(self, x):
        return integrate.odeint(self.sir_model, (self.s0, self.i0, self.r0), x, args=(self.beta, self.gamma)).T



    