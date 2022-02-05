# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 19:12:31 2022

@author: Brian Chung
This is a revised model. Differences are as follows
1. The number of particles are assumed to grow linearly with each time step
2. New particles, at each time step, all divide along the same dimension

Other than that, the assumptions are the same as the first model. The purpose
of this revision is to cut down on the run time, making running the model
more feasible.
"""
import pandas as pd
from numpy.random import default_rng
import numpy as np

rng = default_rng()


# First of all, let's create a parent material. Parent material should have
# 3 sides and a specific density. From this information, the volume and mass
# will be calculated.
def parentMaterial(side1, side2, side3, density):
    """
    Creates a dataframe of a single row representing the parent material.
    This dataframe will be used to create the subsequent soil profile. Units
    must remain constant, and should the units be different, then the end user
    needs to manually do conversions to give them the same units.

    Parameters
    ----------
    side1 : numeric
        The length of the first side of the parent material.
    side2 : numeric
        The length of the second side of the parent material.
    side3 : numeric
        The length of the third side of the parent material.
    density : numeric
        The density of the parent material.

    Returns
    -------
    A dataframe containing the parent material.

    """
    volume = side1*side2*side3
    mass = volume*density
    SA = (2*side1*side2) + (2*side2*side3) + (2*side1*side3)
    values = [side1, side2, side3, density, volume, mass, SA]
    # pm = pd.DataFrame(data=values, columns=["side1", "side2", "side3",
    #                                         "density", "volume", "mass", "SA"])
    pm = pd.DataFrame(data={"id": [1], "side1": [side1], "side2": [side2],
                            "side3": [side3], "density": [density],
                            "volume": [volume], "mass": [mass], "SA": [SA]})
    return pm


# Now, let's create a growth function
def growth(soilProfile):
    """
    This growth function calculates the number of new soil particles that will
    be created at a time step.

    Parameters
    ----------
    soilProfile : Pandas dataframe
        A dataframe that contains data on all the individual particles at a
        particular time step prior to the creation of new particles.

    Returns
    -------
    A number representing the number of new particles that will be created.

    """
    existingParticles = soilProfile.shape[0]
    if existingParticles <= 10:
        newParticles = 1
    elif existingParticles <= 20 and existingParticles > 10:
        newParticles = 10
    elif existingParticles <= 50 and existingParticles > 20:
        newParticles = 20
    elif existingParticles <= 100 and existingParticles > 50:
        newParticles = 50
    elif existingParticles <= 200 and existingParticles > 100:
        newParticles = 100
    elif existingParticles <= 300 and existingParticles > 200:
        newParticles = 200
    elif existingParticles <= 1000 and existingParticles > 300:
        newParticles = 300
    elif existingParticles > 1000:
        newParticles = 1000
    return newParticles


def createParticles(soilProfile):
    """
    This function will be run iteratively, where each iteration is a particular
    time step in which a new soil profile will be created. Creates a new soil
    profile from an existing soil profile at a particular time step.

    Parameters
    ----------
    soilProfile : Pandas dataframe
        The existing soil profile at a particular time step.

    Returns
    -------
    A pandas dataframe that represents the new soil profile at this time step.

    """
    newNum = growth(soilProfile)
    particlesToDivide = soilProfile.sample(newNum, axis=0)
    oldSoilProfile = soilProfile.copy()
    particlesToDivideId = str(particlesToDivide.id.tolist())
    queryStr = "id != {}".format(particlesToDivideId)
    oldSoilProfile = oldSoilProfile.query(queryStr)
    dividedSide = rng.integers(1, 3, endpoint=True)
    if dividedSide == 1:
        particlesToDivide.side1 = particlesToDivide.side1/2
    elif dividedSide == 2:
        particlesToDivide.side2 = particlesToDivide.side2/2
    elif dividedSide == 3:
        particlesToDivide.side3 = particlesToDivide.side3/2
    particlesToDivide.volume = (particlesToDivide.side1
                                * particlesToDivide.side2
                                * particlesToDivide.side3)
    particlesToDivide.mass = particlesToDivide.density*particlesToDivide.volume
    particlesToDivide.SA = ((2*particlesToDivide.side1*particlesToDivide.side2)
                            + (2*particlesToDivide.side2
                               * particlesToDivide.side3)
                            + (2*particlesToDivide.side1
                               * particlesToDivide.side3))
    soilParticlesList = [oldSoilProfile, particlesToDivide, particlesToDivide]
    newProfile = pd.concat(soilParticlesList, axis=0)
    particleNum = newProfile.shape[0]
    newProfile.id = np.arange(1, particleNum + 1)
    newProfile = newProfile.reset_index(drop=True)
    return newProfile


def run(timeStep, side1, side2, side3, density):
    """
    Runs the model iteratively, producing a new soil profile at each time step.
    Calculations will be conducted on each new soil profile, with the variables
    being calculated include means of particle mass and volume, specific
    surface area, and number of particles.

    Parameters
    ----------
    timeStep : numeric
        The final time step. The model will be run iteratively in a loop until
        the final time step is reached.
    side1 : numeric
        The length of the first side of the parent material.
    side2 : numeric
        The length of the second side of the parent material.
    side3 : numeric
        The length of the third side of the parent material.
    density : numeric
        The density of the parent material.

    Returns
    -------
    A pandas dataframe containing characteristics of each soil profile created
    at each time step.

    """
    pm = parentMaterial(side1, side2, side3, density)
    oldProfile = pm
    timeStep = int(timeStep)
    zerosArray = np.zeros(timeStep)
    outputDF = pd.DataFrame({"timeStep": zerosArray,
                             "numOfParticles": zerosArray,
                             "meanParticleMass": zerosArray,
                             "meanParticleVolume": zerosArray,
                             "specificSA": zerosArray})
    for index, row in outputDF.iterrows():
        outputDF.loc[index, "timeStep"] = index + 1
        newProfile = createParticles(oldProfile)
        meanDF = newProfile.mean()
        outputDF.loc[index, "numOfParticles"] = newProfile.id.max()
        outputDF.loc[index, "specificSA"] = newProfile.SA.sum()
        outputDF.loc[index, "meanParticleMass"] = meanDF.mass
        outputDF.loc[index, "meanParticleVolume"] = meanDF.volume
        oldProfile = newProfile

    return outputDF


# 500 iterations is good for me
