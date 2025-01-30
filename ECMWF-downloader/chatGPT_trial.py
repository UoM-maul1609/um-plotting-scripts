import cdsapi
from datetime import datetime, timedelta

# Initialize the CDS API client
c = cdsapi.Client()

# Define the parameters
# Define the single-level variables
variables = [
    "geopotential",
    "land_sea_mask",
    "skin_temperature",
    "soil_temperature_level_1",
    "soil_temperature_level_2",
    "soil_temperature_level_3",
    "soil_temperature_level_4",
    "volumetric_soil_water_layer_1",
    "volumetric_soil_water_layer_2",
    "volumetric_soil_water_layer_3",
    "volumetric_soil_water_layer_4",
    "sea_ice_cover",
    "snow_depth",
    "surface_pressure"
]
params2=[9,14,65,40,50,51,66,30,31,32,33,22,41,11]
params2=[129,172,235,139,170,183,236,39,40,41,42,500069,141,25]
params=[130,133,248,246,247,131,132]
model_levels = list(range(1, 61))  # Levels 1 to 60

# Define date range and time steps
start_date = datetime(2006, 2, 5)
end_date = datetime(2006, 2, 6)
# Loop through times and create separate files
times=["00:00", "06:00", "12:00", "18:00"] # Four times per day


# Generate a list of all dates
current_date = start_date
dates = []
while current_date <= end_date:
    dates.append(current_date.strftime("%Y-%m-%d"))
    current_date += timedelta(days=1)




# Loop through dates and times
for date in dates:
    for time in times:
        output_filename = f"era5_{date}_{time.replace(':', '')}.grib"  # File name
        print(f"Requesting data for {date} {time}...")
        c.retrieve(
        	"reanalysis-era5-complete",  # Dataset
        	{
				"format": "grib",  # Output in GRIB format
				"param": params,
				"levtype": 'ml',
				"levelist": model_levels,
				"date": date,  # Date range
				"time": time,  
# 				"area": [90, -180, -90, 180],  # Global extent: North, West, South, East
				"area": [90, 0, -90, 360],  # Global extent: North, West, South, East
				"grid": [0.75,0.75],
				"expver": "1"  # Experiment version
			},
			output_filename  # Output file name
		)
        print(f"Data saved to {output_filename}")


        output_filename = f"era5_single_levels_{date}_{time.replace(':', '')}.grib"
        print(f"Requesting data for {date} {time}...")
        # Submit the request
        c.retrieve(
#         	"reanalysis-era5-complete",  # Dataset
            "reanalysis-era5-single-levels",
            {
               "product_type":"reanalysis",
               "format": "grib",  # Output format
                "variable": variables,
                #"param": params2,
                "date": date,  # Single date
                "time": time,  # Single time step
#                 "area": [90, -180, -90, 180],  # Global extent
                "area": [90, 0, -90, 360],  # Global extent
				"grid": [0.75,0.75],
            },
            output_filename  # Save to this file
        )
        print(f"Data saved to {output_filename}")


