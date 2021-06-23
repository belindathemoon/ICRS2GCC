import numpy as np

# temp params used to test the code (copied them from a specific star from the
# paper)

pm_ra_star = -2.676
sigma_pm_ra_star = 0.043
pm_dec_star = -4.991
sigma_pm_dec_star = 0.034
parallax_star = 0.454
sigma_parallax_star = 0.029

cov_matrix_star = np.diag([sigma_pm_ra_star**2, sigma_pm_dec_star**2,
                           sigma_parallax_star**2])

params_star = [pm_ra_star, pm_dec_star, parallax_star]

def calc_distance(params, cov_matrix):
    parallax = params[2]
    sigma_parallax = np.sqrt(cov_matrix[2, 2])
    f = sigma_parallax/parallax
    if f > 0.1 or f < 0:
        distance = method_mcmc(params, cov_matrix)
    else:
        distance = method_simple(params, cov_matrix)
    return distance

def method_simple(params, cov_matrix):
    print('Using simple method')
    return 0

def method_mcmc(params, cov_matrix):
    print('Using complicated method')
    return 0

# calc_distance(params_star, cov_matrix_star)
