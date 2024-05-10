import matplotlib.pyplot as plt
import math
import shapely.geometry as shp
from shapely.geometry import Polygon
import numpy as np
import geopandas as gpd

LIGHT_TO_SPHERE = 6
LIGHT_TO_IMAGE = 1
TEXTURE_SIZE = 100

world_gdf = gpd.read_file(
    gpd.datasets.get_path('naturalearth_lowres')
)

# Convert MultiPolygon to Polygon
world_coord = world_gdf['geometry'].to_numpy()
flattened = []
for shape in world_coord:
    if shape.type == 'MultiPolygon':
        flattened.extend(list(shape.geoms))
    else:
        flattened.append(shape)

def mapper(x, oldMin, oldMax, newMin, newMax):
    ratio = (x - oldMin) / (oldMax - oldMin)
    return newMin + (ratio * (newMax - newMin))

def lon_lat_to_xyz(lon, lat):
    # Convert degrees to radians
    lon_rad = math.radians(lon)
    lat_rad = math.radians(lat)

    # Convert to Cartesian coordinates
    x = math.cos(lat_rad) * math.cos(lon_rad)
    y = math.cos(lat_rad) * math.sin(lon_rad)
    z = math.sin(lat_rad)

    return x, y, z

polygon_series = []
for polygon in flattened:
    if polygon.exterior is not None:
        coords = polygon.exterior.coords
        projected_array = []
        for lon, lat in coords:
            x, y, z = lon_lat_to_xyz(lon, lat)
            if x < 0.2:
                continue
            dist_of_pt_center_line = np.sqrt(y ** 2 + z ** 2)
            dist_of_proj_pt_center = dist_of_pt_center_line / (LIGHT_TO_SPHERE - x) * LIGHT_TO_IMAGE
            angle_of_proj_pt_z_axis = np.arctan2(y, z)
            j = np.sin(angle_of_proj_pt_z_axis) * dist_of_proj_pt_center
            i = np.cos(angle_of_proj_pt_z_axis) * dist_of_proj_pt_center * np.sign(z)

            if not np.isnan(i) and not np.isnan(j):
                max_val = 0.203  # Adjust this based on your data range
                i_mapped = mapper(i, -max_val, max_val, 0, TEXTURE_SIZE)
                j_mapped = mapper(j, -max_val, max_val, 0, TEXTURE_SIZE)
                projected_array.append((i_mapped, j_mapped))
        if len(projected_array) >= 4:
            polygon_series.append(Polygon(projected_array))

# Create a GeoSeries from the list of Polygons
mapplot = gpd.GeoSeries(polygon_series)

# Plot the GeoSeries
fig, ax = plt.subplots(1, 1, figsize=(12, 12))  # Adjusted for potentially larger view

mapplot.plot(ax=ax)

# Adjust plot limits to make sure we can see the full projection
x_min, y_min, x_max, y_max = mapplot.total_bounds
x_range = x_max - x_min
y_range = y_max - y_min
max_range = max(x_range, y_range)

# Expand the range by a small margin to ensure nothing is clipped
margin = max_range * 0.1
ax.set_xlim(-x_min + margin, x_max + margin)
ax.set_ylim(y_min - margin, y_max + margin)

# Set aspect ratio
ax.set_aspect('equal')

# Set labels and title
ax.set_xlabel('Projected x')
ax.set_ylabel('Projected y')
ax.set_title('Full Projected World Map onto Sphere')

plt.show()
