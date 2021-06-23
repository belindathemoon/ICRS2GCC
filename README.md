# codeastro2021-group22
Project with Fredi Quispe H and Antonia Fernandez: To carry out the transformation of coordinates from ICRS (International Celestial Reference System) to Galactocentric coordinates (CGC) using Bayesian method for stars with full astrometric information in Gaia.

# Objective:

To carry out the transformation of coordinates from ICRS (International Celestial Reference System) to Galactocentric coordinates (CGC) using Bayesian method for stars with full astrometric information in Gaia.

[α,δ,μ^∗.α,μδ,ϖ,rv].ICRS→[X,Y,Z,Vx,Vy,Vz].CGC

# Theoretical framework:

To carry out the transformation from ICRS to CGC, it is necessary to have the following parameters:  Position,  proper motion in right ascension and decline, distance and radial velocity.  However, in order to take into account the correlation coefficients between the parameters (given by Gaia) and the propagation of  errors  during  the  transformation,  for  stars  with  relative  error  in  parallax (f≡σϖ/ϖ<0.1) and (f >0.1), it is necessary to perform a Bayesian treatment. This procedure is described in Marchetti et al.  2018 for both cases.

# Steps:

1.  Query object from Gaia EDR3 database (for this step we can use astroquery)

2.  Sampling ICRS coordinates using multivariate gaussian distribution
    • Get  the  covariance  matrix  using  the  correlations  coefficients  from Gaia.
    • Get the distance (f <0.1):
        –Run 1000 Monte Carlo simulations
        –Calculate the distance as d=1/ϖ for each simulation.
        –Get the distance as the mean of all the distances found in the simulations.
    • Get the distance (f <0.1 orf <0):
        –Use MCMC to estimate the posterior distribution of the distance (using priors and likelihood described in the paper).
        –Extract distance from the posterior distribution.

3.  Transform the elements of the sampling using the Galactocentric ”function” in astropy