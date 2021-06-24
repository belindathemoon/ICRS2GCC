"""Functions to perform distance transformations"""
import numpy as np
from scipy.stats import multivariate_normal
import emcee

def calc_distance(params, cov_matrix):
    """Calculate Distances

    Args:
        params (array): length 3 vector.
        cov_matrix (array): 3x3 matrix.

    Returns:
        distance and standard deviation
    """
    parallax = params[2]
    sigma_parallax = np.sqrt(cov_matrix[2, 2])
    f = sigma_parallax/parallax
    if f > 0.1 or f < 0:
        distance, sigma_distance = method_mcmc(params, cov_matrix)
    else:
        distance, sigma_distance = method_simple(params, cov_matrix)
    return distance, sigma_distance

def method_simple(params, cov_matrix):
    """Simple Method 
    
    For parallaxes that have large errors or negative
    Runs 100 Monte Carlo simulations and calculates the mean and SD of the calculated distances
    
    Args:
        params (array): length 3 vector.
        cov_matrix (array): 3x3 matrix.

    Returns:
        distance and standard deviation
    """
    num_sim = 100
    dist_arr = np.zeros(num_sim)
    # run 100 monte carlo simulations
    for i in range(num_sim):
        mc_sim = run_mc_sim(params, cov_matrix)
        ## save distance values
        parallax_sim = mc_sim[2]
        dist_sim = 1/parallax_sim
        dist_arr[i] = dist_sim
    # calculate mean and std of the calculated distances
    distance = np.mean(dist_arr)
    sigma_distance = np.std(dist_arr)
    return distance*10**3, sigma_distance*10**3

def run_mc_sim(params, cov_matrix):
    rvs = multivariate_normal.rvs(mean=params, cov=cov_matrix)
    return rvs

def method_mcmc(params, cov_matrix):
    return 0, 0

def prior(d):
    L = 2.6 # value used in the paper
    p = d**2 * np.exp(-d/L)
    return p

def likelihood(d, parallax, sigma_parallax):
    like = np.exp(-1/(2*sigma_parallax**2)*(parallax-1/d)**2)
    return like

def posterior(d, parallax, sigma_parallax):
    p = prior(d)
    like = likelihood(d, parallax, sigma_parallax)
    return p*like

def run_mcmc(d, parallax, sigma_parallax):
    nwalkers = 32
    pos = d + 1e-4 * np.random.randn(nwalkers, 1)
    #ndim, nwalkers = pos.shape
    sampler = emcee.EnsembleSampler(nwalkers, 1, posterior,
                                    args=(parallax, sigma_parallax))
    sampler.run_mcmc(pos, 5000, progress=True)#, skip_initial_state_check=True)
    flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)
    print(np.mean(flat_samples))
    mcmc = np.percentile(flat_samples[:], [16, 50, 84])
    print(mcmc)
