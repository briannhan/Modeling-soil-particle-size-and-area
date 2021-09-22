# Modeling soil particle size and area
This is a very simple model of how rocks weather down to form soil. This model simulates the process of soil formation via the weathering of rocks. Assumptions that it follows are

1. The state factors of soil formation are (1) Climate, (2) Organisms, (3) Relief, aka topography, (4) Parent Material, and (5) Time. This model ignores the first 3 state factors and assumes that soil formation is shaped only by the parent material and the amount of time that passes. More specifically, it assumes that the density of soil material -- not including pore spaces, so not bulk density -- is identical to the density of the parent material, so only physical weathering occurred and that any chemical weathering that occurred is minor enough to not change the chemical composition of the soil material.
2. All particles are assumed to be rectangular prisms or cubes, and new soil particles are formed by bisecting existing soil particles down the middle of a particular length of the particle. The length that will be bisected is chosen using a random number generator. This ensures a stochasticity in specific surface area that, I believe, is realistic.

## Software versions

Conda 4.9.2

Python 3.8.5

Numpy 1.19.2

Pandas 1.1.3

## Instructions

To run the model, please ensure that you have the necessary libraries and version of Python installed. To be safe, ensure that the Python packages you've installed are the same as above.

1. Create a new Python script
2. Import the **model.py** module into your Python script
3. Create a **particle** object to serve as the parent material (More on this class below)
4. Call the **main()** function from the model.py module. Each call of this function runs the model once (More on this function below)

### Particle class

This class represents a particle in the real world, whether this particle is a mineral soil particle (clay, silt, or sand) or a rock or boulder. The particle is assumed to be either a rectangular prism or a cube, both of which have 6 sides and 3 lengths. The class has the following instantiation



*someParticle = particle(d1, d2, d3, density)*



where the attributes are



*d1 = one of the lengths of the particle. A number, either float or integer.*

*d2 = one of the lengths of the particle. A number, either float or integer.*

*d3 = one of the lengths of the particle. A number, either float or integer.*

*density = the density of the particle. A number, a float.*



The class also contains the method *divide()*. This method divides the particle that is calling the method into two new particles. An example call can be shown below



*newParticle1, newParticle2 = someParticle.divide()*



Each call of this method randomly chooses a particular length of the particle. A bisector plane will be drawn perpendicular to this length, dividing the particle into two new particles. A side is chosen using a random number generator. For example, if the side *d1* is chosen by the number generator to divide *someParticle*, the the new particles will have dimensions of



*newParticle1 = particle(d1/2, d2, d3, density)*

*newParticle2 = particle(d1/2, d2, d3, density)*



The new particles will otherwise have the same *d2* and *d3* lengths as the original *someParticle*. They will also share the same density as the original particle. A particle object also has attributes *surfaceArea*, *volume*, and *mass*, all of which are self-explanatory. These attributes are automatically calculated after specifying all the lengths and the density of a particle.

**Regarding units**: The units are of the user's own choosing, and the user has the responsibility of keeping track of the units. That means that this model was not coded to used a specific set of units. For example, if the user chose to specify the lengths in *cm* and the density in *grams per cubic centimeter*, then the model will still run normally. If the user chose to specify the lengths in *inch* and the density in *pounds per cubic inch*, then this model will also run normally. However, please keep the units for length and density the same. For example, if length is specified in *cm*, then density must also include *cm* rather than *dm*, *m*, *km*, or any non-SI units or SI units other than *cm*. Likewise, if density includes *cubic feet*, then length must also use *feet* rather than *inch*, *yard*, other imperial units or SI units.



### main()

Calling this function once will the model once. Each run of this model simulates the process of soil formation over a specified time period starting from a specific parent material, both of which are arguments to specify in the function. This function returns a Pandas dataframe (for those not in the know, this is essentially a table that contains data, and is created using the Pandas package) that contains data regarding a few physical characteristics of a particular soil profile at each time step. An example call is written below



*run1data = main(parentMaterial, end)*



where the arguments are



*parentMaterial = the parent material from which the soil profile will be created. This is an object of the particle class.*

*end = the number of time steps for which to run the model. In layman's terms, this is the amount of time over which the model will be run. This is a single integer.*



Units of a time step are arbitrary and chosen by the user, and can be anything from individual years, to decades, centuries, or millennia. After specifying the total number of time steps using the *end* argument, the model will run over the specified number of time steps starting with the initial time step of 1 during which the parent material will be divided into 2 particles. Each subsequent time step then divides particles until the final time step is reached. The output dataframe, *run1data*, contains data for the soil profile that is created after each time step. Each of this dataframe represents the soil profile created at the end of a particular time step. The columns are



*timeStep: the time step associated with the soil profile that is being created. Integer with the lowest value being 1. Has units of the user's choosing.*

*numberOfParticles: the total number of particles (rocks or soil particles) that is in the new soil profile created at the end of this time step. Integer with the lowest value being 2 at a time step of 1. Unitless.*

*specificSurfaceArea: the total surface area of all the particles in the new profile created at the end of this time step. Float, with the lowest value being at a time step of 1. Has units of the user's choosing.*

*particleVolume: the average volume of a single particle in the new profile created at the end of this time step. Float, with the highest value being at a time step of 1. Has units of the user's choosing.*



The 1st time step is when the parent material is divided into 2 new particles. This soil profile is represented as the first row in the dataframe.

**Regarding units:** Again, the units are the user's responsibility, but please ensure that characteristics with units all share the same units. For example, if *specificSurfaceArea* uses *meters*, then *particleVolume* must also use *meters* rather than *cm*, *dm*, *mm*, or any other SI units or imperial units for length.

Each run of this function outputs a dataframe containing data of the soil profile created after a particular time step. It is up to the user to use this data how they wish. I originally created this model to study the relationship between specific surface area and particle volume. This relationship has important consequences in real life. For example, adsorption of pollutants such as herbicides, insecticides, or other pesticides tend to be stronger in finer soils with smaller particles as smaller particles tend to have greater surface area. In addition, soils with relatively large particle sizes (sandy soils) have relatively low cation exchange capacity (the ability to hold onto cations) and water retention due to their large surface area. This results in them being poor media for plant growth and agriculture.
