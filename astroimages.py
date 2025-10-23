# Import necessary libraries
import os
import glob
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from astropy.io import fits
import numpy as np

# Set the folder path containing the FITS files
folder_path = './fits_folder'  # Replace with your actual folder path

# Get all FITS files in the folder
fits_files = glob.glob(os.path.join(folder_path, '*.fits'))

# Check if any FITS files were found
if not fits_files:
    print(f"No FITS files found in {folder_path}")
else:
    # Loop through each FITS file
    for fits_file in fits_files:
        try:
            # Open the FITS file
            with fits.open(fits_file) as hdul:
                # Print HDU info for debugging
                print(f"\nProcessing {fits_file}")
                print(hdul.info())
                
                # Find the first HDU with 2D or 3D data
                data = None
                for i, hdu in enumerate(hdul):
                    if hasattr(hdu, 'data') and hdu.data is not None:
                        if hdu.data.ndim in [2, 3]:
                            data = hdu.data
                            print(f"Using data from HDU {i} with shape {data.shape}")
                            break
                if data is None:
                    print(f"No valid 2D/3D image data found in {fits_file}")
                    continue
                
                # Convert data to float to handle NaN and inf checks
                data = np.array(data, dtype=np.float64)
                
                # Handle potential NaNs or infs in data
                if np.any(np.isnan(data)) or np.any(np.isinf(data)):
                    data = np.nan_to_num(data)
                
                # Ensure data is 2D (if 3D, take first channel for simplicity)
                if data.ndim == 3:
                    print(f"3D data detected, using first channel: {data.shape}")
                    data = data[0]  # Take first channel if 3D
                
                # Verify data is 2D
                if data.ndim != 2:
                    print(f"Invalid data shape {data.shape} in {fits_file}, skipping")
                    continue
                
                # Determine vmin and vmax based on data percentiles for better visualization
                # Randomize slightly for variety
                percentile_low = random.uniform(0, 10)  # Random low percentile
                percentile_high = random.uniform(90, 100)  # Random high percentile
                vmin = np.percentile(data, percentile_low)
                vmax = np.percentile(data, percentile_high)
                
                # Generate 10,000 positions, ensuring start at 0 and end at 1
                num_colors = 10000
                # Create random positions between 0 and 1, excluding endpoints
                positions = [random.random() for _ in range(num_colors - 2)]
                positions.sort()  # Sort to ensure increasing order
                positions = [0.0] + positions + [1.0]  # Force start at 0, end at 1
                
                # Generate 10,000 random RGB colors
                colors = []
                for _ in range(num_colors):
                    r = random.randint(0, 255) / 255.0
                    g = random.randint(0, 255) / 255.0
                    b = random.randint(0, 255) / 255.0
                    colors.append((r, g, b))
                
                # Create cdict for LinearSegmentedColormap
                cdict = {'red': [], 'green': [], 'blue': []}
                for pos, color in zip(positions, colors):
                    cdict['red'].append((pos, color[0], color[0]))
                    cdict['green'].append((pos, color[1], color[1]))
                    cdict['blue'].append((pos, color[2], color[2]))
                
                # Create the custom colormap
                custom_cmap = mcolors.LinearSegmentedColormap('custom_cmap', cdict)
                
                # Create the plot
                fig, ax = plt.subplots(figsize=(10, 10))
                im = ax.imshow(data, cmap=custom_cmap, vmin=vmin, vmax=vmax, origin='lower')
                ax.set_title(os.path.basename(fits_file))
                fig.colorbar(im, ax=ax)
                
                # Save the plot
                save_path = fits_file.replace('.fits', '_plot.png')
                plt.savefig(save_path)
                plt.close(fig)  # Close to avoid displaying in Jupyter if not needed
                
                print(f"Saved plot for {fits_file} to {save_path}")
                
        except Exception as e:
            print(f"Error processing {fits_file}: {str(e)}")
