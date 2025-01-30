import xarray as xr

# Load model-level data
model_ds = xr.open_dataset("era5_2006-02-05_0000.grib", engine="cfgrib")

# Load single-level data
single_ds = xr.open_dataset("era5_single_levels_2006-02-05_0000.grib", engine="cfgrib")

# Merge datasets
combined_ds = xr.merge([model_ds, single_ds])

# Save the merged dataset as a NetCDF file
combined_ds.to_netcdf("combined_data.nc")

print("Combined data saved as 'combined_data.nc'")

