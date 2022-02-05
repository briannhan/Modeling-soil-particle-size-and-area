# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 10:41:24 2021

@author: Brian Chung
This is a simple, time-resolved (I made that word up), mathematical model of
how soil particles change in size and specific surface area through time. The
original purpose of this model is to study the relationship between the size
of individual soil particles and the specific surface area of the entire soil
profile.

The model models the time-resolved process of weathering over time, in which
the original parent materials break down into smaller and smaller particles.
To help explain the model, the phrase "all particles" will include the parent
material as well.
The following assumptions are made:

(1) All particles, including the original parent material, are rectangular
prisms or cubes
(2) All particles are made out of the same material with a specific chemical
structure and so have the same density that remains constant through time
across all particles. In other words, only physical weathering is occurring.
(3) The parent material starts out as a cube or a rectangular prism and is,
therefore, a giant particle
"""

import pandas as pd
import numpy as np
from numpy.random import default_rng
from time import time

rng = default_rng()


class particle:
    def __init__(self, side1, side2, side3, density):
        self.d1 = side1
        self.d2 = side2
        self.d3 = side3
        self.density = density
        self.surfaceArea = (2*side1*side2) + (2*side2*side3) + (2*side3*side1)
        self.volume = side1*side2*side3
        self.mass = density*self.volume

    def divide(self):
        """
        Divides a particle into 2 new particles. A side will randomly be chosen
        to divide the particle, and the particle will be divided by a bisector
        down the middle of that side.

        Returns
        -------
        2 new particles.

        """
        number = rng.integers(1, 3, endpoint=True)
        if number == 1:
            newSide1 = self.d1/2
            newParticle1 = particle(newSide1, self.d2, self.d3, self.density)
            newParticle2 = particle(newSide1, self.d2, self.d3, self.density)
        elif number == 2:
            newSide2 = self.d2/2
            newParticle1 = particle(self.d1, newSide2, self.d3, self.density)
            newParticle2 = particle(self.d1, newSide2, self.d3, self.density)
        elif number == 3:
            newSide3 = self.d3/2
            newParticle1 = particle(self.d1, self.d2, newSide3, self.density)
            newParticle2 = particle(self.d1, self.d2, newSide3, self.density)
        return newParticle1, newParticle2


def divideParticles(oldParticles):
    """
    Divides all the particles at a particular time step into new particles.

    Parameters
    ----------
    oldParticles : tuple
        The list of particles at a particular time step. All of the particles
        in this list will be divided.

    Returns
    -------
    A new tuple of divided particles at this time step, representing the new
    soil profile, and the amount of time it takes the model to create this new
    soil profile to measure model performance.

    """
    start = time()
    newParticles = ()  # empty tuple
    for item in oldParticles:
        dividedParticles = item.divide()  # Since it returns multiple items
        # but the items are not each assigned a name, these items are put into
        # a single tuple. Hence, this method now returns a single tuple
        newParticles = newParticles + dividedParticles
    end = time()
    profileCreationTime = end - start
    return newParticles, profileCreationTime


def characteristics(particles):
    """
    At a particular time step, after all the old particles are divided, this
    calculates the physical characteristics of the new soil profile with new
    particles. These physical characteristics are the specific surface area
    and the average volume of each new soil particle. Because all soil
    particles are bisected in each time step, every particle should have
    identical volume as each other, and the volume of each particle should be
    the average volume.

    Parameters
    ----------
    particles : tuple
        The new soil profile with new particles created at the end of this
        time step. Characteristics of this will be calculated.

    Returns
    -------
    Characteristics of the new soil profile: specific surface area (total
    surface area of all soil particles), mean particle volume, number of
    particles. Also outputs the amount of time it takes to perform these
    calculations as a means of measuring model performance.

    """
    start = time()
    numOfParticles = len(particles)
    SAarray = np.array([])
    volumeArray = np.array([])
    for particle in particles:
        SAarray = np.append(SAarray, particle.surfaceArea)
        volumeArray = np.append(volumeArray, particle.volume)
    specificSA = np.sum(SAarray)
    meanVolume = np.mean(volumeArray)
    end = time()
    calculationTime = end - start
    return specificSA, meanVolume, numOfParticles, calculationTime


def run(parentMaterial, end):
    """
    Runs a simulation of the model over a specific time interval, the ending
    time step of which is specified by the "end" parameter. Produces a pandas
    dataframe containing the characteristics of the new soil profile created
    at the end of each time step.

    Parameters
    ----------
    parentMaterial : particle object
        The parent material that will be divided with each time step.
    end : int
        The ending time step

    Returns
    -------
    A pandas dataframe containing physical characteristics of the new soil
    profile created at the end of each time step.

    """
    # Creating the empty output dataframe to be filled in later
    timeSteps = np.arange(1, end + 1)
    emptySpecificSA = np.zeros(end)
    emptyVolume = np.zeros(end)
    emptyPartNum = np.zeros(end)
    creationTimeArray = np.zeros(end)
    calculationTimeArray = np.zeros(end)
    dfFormat = {"timeStep": timeSteps, "numberOfParticles": emptyPartNum,
                "specificSurfaceArea": emptySpecificSA,
                "particleVolume": emptyVolume,
                "modelCreationTime": creationTimeArray,
                "modelCalculationTime": calculationTimeArray}
    outputDF = pd.DataFrame(data=dfFormat)

    # Populating the dataframe with characteristics of the new soil profile
    # after each time step
    oldProfile = (parentMaterial,)
    for index, row in outputDF.iterrows():
        newProfile, creationTime = divideParticles(oldProfile)
        specificSA, particleVolume, num, calcTime = characteristics(newProfile)

        # Puts in characteristics of the soil profile created at a time step
        outputDF.loc[index, "specificSurfaceArea"] = specificSA
        outputDF.loc[index, "particleVolume"] = particleVolume
        outputDF.loc[index, "numberOfParticles"] = num
        oldProfile = newProfile

        # Puts in times used to create and calculate the characteristics of
        # the soil profile to measure model performance
        outputDF.loc[index, "modelCreationTime"] = creationTime
        '''The amount of time it takes the model to create this particular
        soil profile.'''
        cumuCreationTime = outputDF["modelCreationTime"].sum()
        '''Calculates the total amount of time it takes the model to create all
        the soil profiles up till now. Sums up the creation time from the
        initial time step all the way to this current time step that's being
        looped through'''
        outputDF.loc[index, "cumuCreationTime"] = cumuCreationTime

        outputDF.loc[index, "modelCalculationTime"] = calcTime
        '''The amount of time it takes the model to perform calculations on
        this particular soil profile.'''
        cumuCalcTime = outputDF["modelCalculationTime"].sum()
        '''Calculates the total amount of time it takes the model to perform
        calculations for all soil profiles from the initial time step to the
        one that's being looped through.'''
        outputDF.loc[index, "cumuCalcTime"] = cumuCalcTime

        outputDF.loc[index, "modelTime"] = creationTime + calcTime
        '''Calculates the total amount of time it takes the model to work
        through this new profile, from creating it to performing calculations
        on it.'''
        cumuModelTime = outputDF["modelTime"].sum(skipna=True)
        '''Calculates the amount of time it takes the model to create all the
        soil profiles up to the one that's being looped through and perform
        calculations on them.'''
        outputDF.loc[index, "cumuModelTime"] = cumuModelTime

    return outputDF
