# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 07:57:31 2021

@author: Brian Chung
Analyzes model performance by analyzing the amount of time it takes the model
to create soil profiles and calculate physical characteristics of each profile
"""

from model import particle
from model import run
import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as py
from matplotlib.patches import Patch
from scipy.optimize import curve_fit
from scipy.stats import linregress
import numpy as np

# %%
cwd = Path(os.getcwd())
filesAndFolders = os.listdir(cwd)
outputDir = cwd/'Analyzing model performance'
outputFileName = "Runtime data.csv"
outputPath = outputDir/outputFileName

# Running the model for 18 time steps
if os.path.exists(outputPath) is False:
    PM = particle(1e4, 100, 100, 2.1)
    output = run(PM, 18)
    output.to_csv(outputPath, index=False)
else:
    output = pd.read_csv(outputPath)
# %%
'''Hypothesis to be tested:
    The amount of time it takes the model to create and calculate all particles
    at a given time step grows exponentially with each time step'''

# Creating an exponential growth function to fit against the different model
# times and the number of particles
def exponential(x, y0, r):
    """
    An exponential function that will be fitted against the data using
    curve_fit()

    Parameters
    ----------
    x : numeric
        The independent variable.
    y0 : float
        The initial y value when x = 0.
    r : float
        Growth rate at each iteration as a decimal.

    Returns
    -------
    The estimated value of the dependent variable.

    """
    return y0*((1 + r)**x)


# %%
# Testing the hypothesis on the amount of time it takes the model to create
# particles

# Fitting exponential function to the data
creaParam, creaParamCov = curve_fit(exponential, output.timeStep,
                                    output.modelCreationTime)

# Creating estimates of modelCreationTime based on the exponential regression
modelCreationTimeReg = exponential(output.timeStep, creaParam[0], creaParam[1])

# Graphing 2 figures. Figure of regressed and actual modelCreationTime against
# the number of time steps. Figure of regressed and actual modelCreationTime
# against each other
creaLinResults = linregress(modelCreationTimeReg, output.modelCreationTime)
creaLinY = creaLinResults.slope*modelCreationTimeReg + creaLinResults.intercept
creationFig = py.figure("Creation time analysis", (20, 12))
py.subplot(1, 2, 1)
py.title("Exponential growth figure")
py.xlabel("Time step")
py.ylabel("Model creation time")
expoActual = py.plot("timeStep", "modelCreationTime", "o-r", data=output)
expoRegress = py.plot(output.timeStep, modelCreationTimeReg, ".-b")
expoLineList = expoActual + expoRegress
expoLabels = ["Actual data", "Exponential regression"]
py.legend(handles=expoLineList, labels=expoLabels)
py.subplot(1, 2, 2)
py.title("Comparing actual model creation time and exponential regression")
py.xlabel("Estimated model creation time")
py.ylabel("Actual model creation time")
actual = py.plot(modelCreationTimeReg, output.modelCreationTime, "o-k")
regression = py.plot(modelCreationTimeReg, creaLinY, "-r")
emptyPatch = Patch(facecolor=(1, 1, 1))
linLines = actual + regression
linLines.append(emptyPatch)
r2val = creaLinResults.rvalue**2
# r2val = float(r2val)
r2str = "R-squared = {:.4f}".format(r2val)
linLabels = ["Points", "Linear regression", r2str]
py.legend(handles=linLines, labels=linLabels)
'''Ye the exponential growth hypothesis explains the relationship between
time step and model creation time very well. Although keep in mind that this is
based on only 18 data points'''
# %%
# Testing the same hypothesis on the time it takes for model to perform
# calculations at each time step

# calParam, calParamCov = curve_fit(exponential, output.timeStep,
#                                   output.modelCalculationTime)
'''RuntimeError: Optimal parameters not found
Well shit. This means 1 of 2 things, either this relationship is not actually
exponential, or scipy just can't evaluate it, whether or not the relation is
actually exponential. I'll just evaluate this visually, then'''
calFig = py.figure("Calculation time analysis", (10, 12))
py.title("Calculation time analysis")
py.xlabel("Time step")
py.ylabel("Model creation time")
expoActual2 = py.plot("timeStep", "modelCalculationTime", "o-r", data=output)
'''Visually, it does look like exponential growth to me. So, in conclusion,
the way that I constructed the model so far, by doubling the number of
particles at each time step, I'm effectively causing model calculation and
creation times to also grow exponentially.'''
