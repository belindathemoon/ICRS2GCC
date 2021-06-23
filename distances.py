import numpy as np

# temp params used to test the code (copied them from a specific star from the
# paper)

pm_ra = -2.676
sigma_pm_ra = 0.043
pm_dec = -4.991
sigma_pm_dec = 0.034
parallax = 0.454
sigma_parallax = 0.029

cov_matrix = np.diag([sigma_pm_ra**2, sigma_pm_dec**2, sigma_parallax**2])
