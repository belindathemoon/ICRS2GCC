import numpy as np
import astropy.units as u
import astropy.coordinates as coord
from astroquery.gaia import Gaia

class ICRS2GCC():

    def __init__(self, source_id):
        self.source_id = source_id
    
    def query_gaia_object(self):
        """
        Function that returns all gaia information for the object with id source_id
        
        Returns:
            Gaia information (astropy table): astrometric and photometric information for the object with id source_id
        """
        query = """SELECT * FROM gaiaedr3.gaia_source 
        WHERE source_id = {Gaia_ID}"""
        query = query.format(Gaia_ID=self.source_id)
        job = Gaia.launch_job_async(query)
        return job.get_results()
    
    def cov_matrix(self):
        """
        Function that returns the covariance matrix using uncertainties and correlations coefficient from Gaia
        
        Returns:
            matrix covariance (numpy array): matrix covariance
        """
        r = self.query_gaia_object()
        # empty matrix to build the covariance matrix
        c = np.empty((6, 6), dtype=float)
        c[0, 0] = r['ra_error']*r['ra_error']
        c[0, 1] = c[1, 0] = r['ra_error']*r['dec_error']*r['ra_dec_corr']
        c[0, 2] = c[2, 0] = r['ra_error']*r['parallax_error']*r['ra_parallax_corr']
        c[0, 3] = c[3, 0] = r['ra_error']*r['pmra_error']*r['ra_pmra_corr']
        c[0, 4] = c[4, 0] = r['ra_error']*r['pmdec_error']*r['ra_pmdec_corr']
        c[0, 5] = c[5, 0] = 0
        c[1, 1] = r['dec_error']*r['dec_error']
        c[1, 2] = c[2, 1] = r['dec_error']*r['parallax_error']*r['dec_parallax_corr']
        c[1, 3] = c[3, 1] = r['dec_error']*r['pmra_error']*r['dec_pmra_corr']
        c[1, 4] = c[4, 1] = r['dec_error']*r['pmdec_error']*r['dec_pmdec_corr']
        c[1, 5] = c[5, 1] = 0
        c[2, 2] = r['parallax_error']*r['parallax_error']
        c[2, 3] = c[3, 2] = r['parallax_error']*r['pmra_error']*r['parallax_pmra_corr']
        c[2, 4] = c[4, 2] = r['parallax_error']*r['pmdec_error']*r['parallax_pmdec_corr']
        c[2, 5] = c[5, 2] = 0
        c[3, 3] = r['pmra_error']*r['pmra_error']
        c[3, 4] = c[4, 3] = r['pmra_error']*r['pmdec_error']*r['pmra_pmdec_corr']
        c[3, 5] = c[5, 3] = 0
        c[4, 4] = r['pmdec_error']*r['pmdec_error']
        c[4, 5] = c[5, 4] = 0
        c[5, 5] = r['dr2_radial_velocity_error']*r['dr2_radial_velocity_error']
        return c
#        def icrs_sampling(self):

    def distance(self):
        """
        Function that returns the heliocentric distance
        
        Returns:
            distance (float): heliocentric distance in pc (parsec) units
        """
        r = self.query_gaia_object()
        return 1000/r['parallax'][0]

    def bayes_distance(self):
        """
        Function that returns the heliocentric distance using bayes 
        
        Returns:
            distance (float): heliocentric distance in pc (parsec) units using bayes
        """
        print('the distance should be calculated using bayes and the function now is in construction')

    def icrs_to_gcc(self):
        """
        Function that returns the star position and velocity in galactocentric coordinates 
        
        Returns:
             galactocentric coordinates (float numpy array): 
        """
        r = self.query_gaia_object()
        f = r['parallax_error']/r['parallax']
        if f > 0 and f <= 0.1:
            distance = self.distance()
        else:
            distance = self.bayes_distance()
        c = coord.SkyCoord(ra = r['ra'], 
                           dec = r['dec'],
                           distance = distance*u.pc,
                           pm_ra_cosdec = r['pmra'],
                           pm_dec = r['pmdec'],
                           radial_velocity = r['dr2_radial_velocity'],
                           frame = 'icrs')
        gc = c.transform_to(coord.Galactocentric)
        gcc = np.array([gc.x.value[0], gc.y.value[0], gc.z.value[0], gc.v_x.value[0], gc.v_y.value[0], gc.v_z.value[0]])
        return gcc