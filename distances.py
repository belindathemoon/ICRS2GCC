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
        distance, sigma_distance = method_mcmc(params, cov_matrix)
    else:
        distance, sigma_distance = method_simple(params, cov_matrix)
    return distance, sigma_distance

def method_simple(params, cov_matrix):
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
    return distance, sigma_distance

def method_mcmc(params, cov_matrix):
    return 0, 0

def run_mc_sim(params, cov_matrix):
    return [0, 0, 1]

calc_distance(params_star, cov_matrix_star)
