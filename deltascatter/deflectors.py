import numpy as np
from astropy.table import Table
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.Cosmo.lens_cosmo import LensCosmo
from lenstronomy.LensModel.Solver.lens_equation_solver import LensEquationSolver


def select_deflectors(lens_data, delta_sigma_range, delta_z_range):
    """
    Selects lenses within specified Δσ and Δz ranges.

    Parameters:
    - lens_data (astropy.Table): Table containing lens data.
    - delta_sigma_range (tuple): (min, max) range for Δσ.
    - delta_z_range (tuple): (min, max) range for Δz.

    Returns:
    - astropy.Table of selected deflectors.
    """
    selected_deflectors = lens_data[(lens_data['sigma'] >= delta_sigma_range[0]) & 
                                    (lens_data['sigma'] <= delta_sigma_range[1]) &
                                    (lens_data['z'] >= delta_z_range[0]) & 
                                    (lens_data['z'] <= delta_z_range[1])]
    return selected_deflectors

def compute_einstein_radius_sis(deflector, cosmo):
    """
    Computes the Einstein radius for a given deflector using the SIS model.

    Parameters:
    - deflector (astropy.Row): Single row from lens_data representing one deflector.
    - cosmo (astropy.cosmology): The cosmology used.

    Returns:
    - float, Einstein radius for the deflector.
    """
    sigma_v = deflector['sigma']  # velocity dispersion in km/s
    lens_redshift = deflector['z']

    # Compute angular diameter distances
    lens_cosmo = LensCosmo(z_lens=lens_redshift, z_source=2.0, cosmo=cosmo)  # Assuming a placeholder source redshift
    D_LS = lens_cosmo.D_dt
    D_S = lens_cosmo.D_s
    
    # Compute Einstein radius for SIS model
    theta_E = (4 * np.pi * (sigma_v * 1e3 / 299792458)**2 * D_LS) / D_S  # sigma_v multiplied by 1e3 to convert to m/s
    return theta_E

def compute_einstein_radius_complex(deflector, source_pos, lens_model_name='SPEP'):
    """
    Computes the Einstein radius for more complex lens models using lens equation solving.

    Parameters:
    - deflector (astropy.Row): Lens properties.
    - source_pos (tuple): Source position used for solving lens equation.
    - lens_model_name (str): Name of the complex lens model.

    Returns:
    - float, Einstein radius.
    """
    # Initialize lens model
    lens_model = LensModel(lens_model_list=[lens_model_name])
    
    # Lens parameters (these would depend on the specific lens model you're using)
    kwargs_lens = [{...}]
    
    # Solve the lens equation
    solver = LensEquationSolver(lens_model)
    image_positions = solver.image_position_from_source(source_pos, kwargs_lens)
    
    # Compute Einstein radius (as an example, we take the average distance of image positions from lens center)
    theta_E = np.mean(np.abs(image_positions))
    return theta_E

# More functions related to scatter and other properties can be added similarly

def compute_scatter(values):
    """
    Computes scatter (standard deviation) of given values.

    Parameters:
    - values (array-like): List or array of values.

    Returns:
    - float, scatter (standard deviation).
    """
    return np.std(values)

def compute_rms(values):
    """
    Computes root mean square of given values.

    Parameters:
    - values (array-like): List or array of values.

    Returns:
    - float, root mean square value.
    """
    return np.sqrt(np.mean(np.square(values)))

def compute_iqr(values):
    """
    Computes the interquartile range (IQR) of given values.

    Parameters:
    - values (array-like): List or array of values.

    Returns:
    - float, interquartile range (IQR).
    """
    return np.percentile(values, 75) - np.percentile(values, 25)

def einstein_radius_scatter(deflectors, cosmo):
    """
    Computes scatter in Einstein radius for given deflectors.

    Parameters:
    - deflectors (astropy.Table): Table of deflectors.
    - cosmo (astropy.cosmology): The cosmology used.

    Returns:
    - dict containing standard deviation, RMS, and IQR of Einstein radii.
    """
    radii = [compute_einstein_radius_sis(deflector, cosmo) for deflector in deflectors]
    
    return {
        'std_dev': compute_scatter(radii),
        'rms': compute_rms(radii),
        'iqr': compute_iqr(radii)
    }