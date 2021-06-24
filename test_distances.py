import numpy as np
from scipy.stats import multivariate_normal
import emcee
import distances


## TESTS for the distances.py file


# temp params used to test the code (copied them from a specific star from the
# paper)
"""
# Star with low f

pm_ra_star = -2.676
sigma_pm_ra_star = 0.043
pm_dec_star = -4.991
sigma_pm_dec_star = 0.034
parallax_star = 0.454
sigma_parallax_star = 0.029
"""
# Star with negative f

pm_ra_star = -1.649
sigma_pm_ra_star = 0.023
pm_dec_star = -4.996
sigma_pm_dec_star = 0.029
parallax_star = -0.017
sigma_parallax_star = 0.014

cov_matrix_star = np.diag([sigma_pm_ra_star**2, sigma_pm_dec_star**2,
                           sigma_parallax_star**2])

params_star = [pm_ra_star, pm_dec_star, parallax_star]

#calc_distance(params_star, cov_matrix_star)
run_mcmc(1/parallax_star, parallax_star, sigma_parallax_star)
