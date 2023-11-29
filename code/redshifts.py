import numpy as np
from astropy.table import Table
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.Cosmo.lens_cosmo import LensCosmo
from lenstronomy.LensModel.Solver.lens_equation_solver import LensEquationSolver



def list_source_redshifts(selected_deflectors):
    """
    Lists source redshifts for the selected deflectors.

    Parameters:
    - selected_deflectors (list): List of selected deflectors.

    Returns:
    - List of source redshifts.
    """
    # Placeholder logic
    # In the actual implementation, you'd use astropy or another source to get the redshifts for the deflectors.
    return [1.5 for _ in selected_deflectors]  # Assuming a dummy redshift value for now.




def select_source_redshifts(source_data, redshift_range):
    """
    Selects sources within a specified redshift range.

    Parameters:
    - source_data (astropy.Table): Table containing source data.
    - redshift_range (tuple): (min, max) range for redshift.

    Returns:
    - astropy.Table of selected sources.
    """
    selected_sources = source_data[(source_data['z'] >= redshift_range[0]) & 
                                   (source_data['z'] <= redshift_range[1])]
    return selected_sources

def mean_redshift(sources):
    """
    Computes the mean redshift of a given set of sources.

    Parameters:
    - sources (astropy.Table): Table of sources.

    Returns:
    - float, mean redshift.
    """
    return np.mean(sources['z'])

def median_redshift(sources):
    """
    Computes the median redshift of a given set of sources.

    Parameters:
    - sources (astropy.Table): Table of sources.

    Returns:
    - float, median redshift.
    """
    return np.median(sources['z'])

# Further functionalities related to redshift can be added as required.


def redshift_distribution(sources, bins=30):
    """
    Computes a histogram of source redshifts.

    Parameters:
    - sources (astropy.Table): Table of sources.
    - bins (int): Number of bins for the histogram.

    Returns:
    - hist (array), bin_edges (array)
    """
    return np.histogram(sources['z'], bins=bins)

def compute_magnification(deflector, source_redshift, lens_model_name='SPEP'):
    """
    Computes magnification for a source at given redshift, considering a specific deflector.

    Parameters:
    - deflector (astropy.Row): Lens properties.
    - source_redshift (float): Redshift of the source.
    - lens_model_name (str): Name of the lens model.

    Returns:
    - float, Magnification.
    """
    lens_model = LensModel(lens_model_list=[lens_model_name])
    # Example kwargs for SPEP lens model. In practice, you'd extract these from your `deflector`.
    kwargs_lens = [{'theta_E': 1.0, 'gamma': 2.0, 'center_x': 0, 'center_y': 0, 'e1': 0.1, 'e2': -0.1}]
    magnification = lens_model.magnification(theta=0, beta=0, kwargs_lens=kwargs_lens)
    return magnification

def compute_time_delay(deflector, source_redshift, lens_model_name='SPEP'):
    """
    Computes time delay for a source at given redshift, considering a specific deflector.

    Parameters:
    - deflector (astropy.Row): Lens properties.
    - source_redshift (float): Redshift of the source.
    - lens_model_name (str): Name of the lens model.

    Returns:
    - float, Time delay.
    """
    # This is a placeholder; actual implementation would require more details
    # about the lens system, such as image positions.
    pass

def cosmological_scaling(source_redshift, cosmo):
    """
    Computes cosmological scaling factors for a given source redshift.

    Parameters:
    - source_redshift (float): Redshift of the source.
    - cosmo (astropy.cosmology): The cosmology used.

    Returns:
    - dict with angular diameter distances.
    """
    lens_cosmo = LensCosmo(z_lens=0.5, z_source=source_redshift, cosmo=cosmo)  # Assuming a placeholder lens redshift
    return {
        'D_S': lens_cosmo.D_s,
        'D_L': lens_cosmo.D_d,
        'D_LS': lens_cosmo.D_ds
    }

def compute_time_delay(deflector, source_redshift, lens_model_name='SPEP', source_position=(0, 0)):
    """
    Computes time delay for a source at given redshift, considering a specific deflector.

    Parameters:
    - deflector (astropy.Row): Lens properties.
    - source_redshift (float): Redshift of the source.
    - lens_model_name (str): Name of the lens model.
    - source_position (tuple): Position of the source.

    Returns:
    - list of time delays for each image.
    """
    lens_model = LensModel(lens_model_list=[lens_model_name])
    # Example kwargs for SPEP lens model. In practice, you'd extract these from your `deflector`.
    kwargs_lens = [{'theta_E': 1.0, 'gamma': 2.0, 'center_x': 0, 'center_y': 0, 'e1': 0.1, 'e2': -0.1}]
    
    # Solving the lens equation to find image positions
    solver = LensEquationSolver(lens_model)
    image_positions = solver.image_position_from_source(source_position, kwargs_lens)
    
    # Compute fermat potential 
    fermat_potential = lens_model.fermat_potential(image_positions, kwargs_lens, source_position)
    
    # Time delay is proportional to the difference in fermat potential between images
    # You would typically get time delays by taking differences between these fermat potentials
    # and multiplying by a constant depending on cosmology and lens configuration.
    
    return fermat_potential  # Placeholder: you'd want to return the actual time delays after computing differences and applying the proportional constant.

def differential_time_delay(deflector, source_redshift, lens_model_name='SPEP', source_position=(0, 0)):
    """
    Computes differential time delay (difference in time delay) between lensed images.

    Parameters:
    - deflector (astropy.Row): Lens properties.
    - source_redshift (float): Redshift of the source.
    - lens_model_name (str): Name of the lens model.
    - source_position (tuple): Position of the source.

    Returns:
    - list of differential time delays between images.
    """
    time_delays = compute_time_delay(deflector, source_redshift, lens_model_name, source_position)
    differential_delays = np.diff(sorted(time_delays))
    
    return differential_delays