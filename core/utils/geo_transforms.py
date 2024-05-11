import math
import numpy as np

class GeoTransformer:
    """
    GeoTransformer is a utility class that provides geographical transformations and 
    mapping functions necessary for projecting the Earth onto a spherical surface.

    Attributes:
        earth_radius (float): Radius of the Earth in kilometers. Default is approximately 6371 km.
    """

    def __init__(self, earth_radius=6371.0):
        """
        Initializes the GeoTransformer with the specified Earth radius.

        Args:
            earth_radius (float): Radius of the Earth in kilometers.
        """
        self.earth_radius = earth_radius

    def lon_lat_to_xyz(self, lon, lat):
        """
        Convert geographic coordinates (longitude, latitude) into 3D Cartesian coordinates.

        Args:
            lon (float): Longitude in degrees.
            lat (float): Latitude in degrees.

        Returns:
            tuple: A tuple of three floats representing the x, y, and z coordinates in 3D space.
        """
        # Convert degrees to radians
        lon_rad = math.radians(lon)
        lat_rad = math.radians(lat)

        # Calculate 3D Cartesian coordinates
        x = self.earth_radius * math.cos(lat_rad) * math.cos(lon_rad)
        y = self.earth_radius * math.cos(lat_rad) * math.sin(lon_rad)
        z = self.earth_radius * math.sin(lat_rad)

        return x, y, z

    def mapper(self, x, old_min, old_max, new_min, new_max):
        """
        Map a value from one range to another, useful in adjusting projection coordinates.

        Args:
            x (float): The value to be mapped.
            old_min (float): The minimum value of the original range.
            old_max (float): The maximum value of the original range.
            new_min (float): The minimum value of the new range.
            new_max (float): The maximum value of the new range.

        Returns:
            float: The mapped value.
        """
        # Calculate the ratio of the position of the value in the original range
        ratio = (x - old_min) / (old_max - old_min)

        # Map the value to the new range
        return new_min + (ratio * (new_max - new_min))

    def coordinate_transformations_for_projection(self, x, y, z, light_to_sphere, light_to_image):
        """
        Transform 3D Cartesian coordinates based on projection settings.

        Args:
            x (float): The x coordinate of the point.
            y (float): The y coordinate of the point.
            z (float): The z coordinate of the point.
            light_to_sphere (float): Distance from the light source to the sphere.
            light_to_image (float): Distance from the light source to the image plane.

        Returns:
            tuple: Transformed (x, y, z) coordinates after projection.
        """
        # Compute how the point is projected onto the balloon's surface
        dist_of_pt_center_line = np.sqrt(y ** 2 + z ** 2)
        dist_of_proj_pt_center = dist_of_pt_center_line / (light_to_sphere - x) * light_to_image
        angle_of_proj_pt_z_axis = np.arctan2(y, z)

        # Calculate the new projected coordinates
        j = np.sin(angle_of_proj_pt_z_axis) * dist_of_proj_pt_center
        i = np.cos(angle_of_proj_pt_z_axis) * dist_of_proj_pt_center * np.sign(z)

        return i, j, z

# Helper functions outside the class, for convenience and backward compatibility
def lon_lat_to_xyz(lon, lat, earth_radius=6371.0):
    """
    Convert geographic coordinates (longitude, latitude) into 3D Cartesian coordinates.
    This is a convenience wrapper around the GeoTransformer class.

    Args:
        lon (float): Longitude in degrees.
        lat (float): Latitude in degrees.
        earth_radius (float): Radius of the Earth in kilometers.

    Returns:
        tuple: A tuple of three floats representing the x, y, and z coordinates in 3D space.
    """
    transformer = GeoTransformer(earth_radius)
    return transformer.lon_lat_to_xyz(lon, lat)

def mapper(x, old_min, old_max, new_min, new_max):
    """
    Map a value from one range to another, useful in adjusting projection coordinates.
    This is a convenience wrapper around the GeoTransformer class.

    Args:
        x (float): The value to be mapped.
        old_min (float): The minimum value of the original range.
        old_max (float): The maximum value of the original range.
        new_min (float): The minimum value of the new range.
        new_max (float): The maximum value of the new range.

    Returns:
        float: The mapped value.
    """
    transformer = GeoTransformer()
    return transformer.mapper(x, old_min, old_max, new_min, new_max)

if __name__ == '__main__':
    print("geo transforms has been run")