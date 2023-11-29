from deltascatter import deflectors, redshifts, scatter
from astropy.table import Table
import astropy.cosmology as cosmo

# Example: Create a sample lens data table (assuming you have columns 'sigma' for velocity dispersion and 'z' for redshift)
lens_data = Table({
    'sigma': [200, 250, 210, 230, 240, 260],  # sample velocity dispersions in km/s
    'z': [0.3, 0.4, 0.35, 0.32, 0.33, 0.41]  # sample redshifts
})

# Defining the Δσ and Δz ranges
delta_sigma_range = (210, 250)  # example sigma range in km/s
delta_z_range = (0.3, 0.4)  # example redshift range

# Task 1: Select narrow range of deflectors
selected_deflectors = deflectors.select_deflectors(lens_data, delta_sigma_range, delta_z_range)
print("Selected Deflectors:", selected_deflectors)

# Task 2: List source redshifts (assuming you are just extracting the redshift column)
source_redshifts = redshifts.list_source_redshifts(selected_deflectors)
print("Source Redshifts:", source_redshifts)

# Task 3: Compute scatter in Einstein radius among the selected deflectors for fixed source redshift
# Using a default cosmology for demonstration
default_cosmology = cosmo.Planck18
scatter_info = scatter.einstein_radius_scatter(selected_deflectors, default_cosmology)
print("Scatter in Einstein Radius (Std Dev):", scatter_info['std_dev'])
print("Scatter in Einstein Radius (RMS):", scatter_info['rms'])
print("Scatter in Einstein Radius (IQR):", scatter_info['iqr'])
