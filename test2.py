import xarray as xr

# Define file paths
model_level_file = "era5_2006-02-05_0000.grib"  # Replace with your model-level GRIB file
single_level_file = "era5_single_levels_2006-02-05_0000.grib"  # Replace with your single-level GRIB file

# Open model-level data
model_ds = xr.open_dataset(
    model_level_file,
    engine="cfgrib",
    backend_kwargs={"indexpath": ""},  # Disable caching
)

# Open single-level data
single_ds = xr.open_dataset(
    single_level_file,
    engine="cfgrib",
    backend_kwargs={"indexpath": ""},  # Disable caching
)

# Extract soil temperature layers individually
stl1 = xr.open_dataset(
    single_level_file,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {"shortName": "stl1"}, "indexpath": ""}
)
stl2 = xr.open_dataset(
    single_level_file,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {"shortName": "stl2"}, "indexpath": ""}
)
stl3 = xr.open_dataset(
    single_level_file,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {"shortName": "stl3"}, "indexpath": ""}
)
stl4 = xr.open_dataset(
    single_level_file,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {"shortName": "stl4"}, "indexpath": ""}
)

# Combine soil temperature layers into one variable
soil_temp_combined = xr.concat(
    [
        stl1["stl1"].assign_coords(depth=0.07),  # Depth in meters
        stl2["stl2"].assign_coords(depth=0.28),
        stl3["stl3"].assign_coords(depth=1.0),
        stl4["stl4"].assign_coords(depth=2.89)
    ],
    dim="depth"
)
soil_temp_combined.name = "soil_temperature"

# Extract volumetric soil water layers
swvl1 = xr.open_dataset(
    single_level_file,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {"shortName": "swvl1"}, "indexpath": ""}
)
swvl2 = xr.open_dataset(
    single_level_file,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {"shortName": "swvl2"}, "indexpath": ""}
)
swvl3 = xr.open_dataset(
    single_level_file,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {"shortName": "swvl3"}, "indexpath": ""}
)
swvl4 = xr.open_dataset(
    single_level_file,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {"shortName": "swvl4"}, "indexpath": ""}
)

# Combine volumetric soil water layers into one variable
soil_water_combined = xr.concat(
    [
        swvl1["swvl1"].assign_coords(layer=0.07),
        swvl2["swvl2"].assign_coords(layer=0.28),
        swvl3["swvl3"].assign_coords(layer=1.0),
        swvl4["swvl4"].assign_coords(layer=2.89)
    ],
    dim="layer"
)
soil_water_combined.name = "volumetric_soil_water"

# Combine all single-level variables
single_combined = xr.Dataset({
    "geopotential": single_ds["z"],  # Replace 'z' with actual variable name
    "land_sea_mask": single_ds["lsm"],  # Replace 'lsm' with actual variable name
    "skin_temperature": single_ds["skt"],  # Replace 'skt' with actual variable name
    "soil_temperature": soil_temp_combined,
    "volumetric_soil_water": soil_water_combined,
    "sea_ice_cover": single_ds["siconc"],  # Replace 'siconc' with actual variable name
    "snow_depth": single_ds["sd"],  # Replace 'sd' with actual variable name
    "log_surface_pressure": single_ds["lnsp"],  # Replace 'lnsp' with actual variable name
})

# Combine with model-level data
combined_ds = xr.merge([model_ds, single_combined])

# Save to NetCDF
combined_ds.to_netcdf("combined_era5_data.nc")
print("Combined dataset saved as 'combined_era5_data.nc'")

