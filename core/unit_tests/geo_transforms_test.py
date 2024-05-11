import unittest
import math
from utils import geo_transforms

class TestGeoTransforms(unittest.TestCase):

    def test_lon_lat_to_xyz(self):
        """
        Test the conversion from geographic coordinates (longitude and latitude)
        to 3D Cartesian coordinates.
        """
        # Test conversion of zero coordinates (0, 0)
        x, y, z = geo_transforms.lon_lat_to_xyz(0, 0)
        self.assertAlmostEqual(x, 1)
        self.assertAlmostEqual(y, 0)
        self.assertAlmostEqual(z, 0)

        # Test conversion of (90, 0) - Equator at 90 degrees longitude
        x, y, z = geo_transforms.lon_lat_to_xyz(90, 0)
        self.assertAlmostEqual(x, 0)
        self.assertAlmostEqual(y, 1)
        self.assertAlmostEqual(z, 0)

        # Test conversion of (0, 90) - North Pole
        x, y, z = geo_transforms.lon_lat_to_xyz(0, 90)
        self.assertAlmostEqual(x, 0)
        self.assertAlmostEqual(y, 0)
        self.assertAlmostEqual(z, 1)

        # Test conversion of (180, 0) - Equator at 180 degrees longitude
        x, y, z = geo_transforms.lon_lat_to_xyz(180, 0)
        self.assertAlmostEqual(x, -1)
        self.assertAlmostEqual(y, 0)
        self.assertAlmostEqual(z, 0)

    def test_mapper(self):
        """
        Test the value mapping from one numerical range to another.
        """
        # Test simple mapping from [0, 10] to [0, 100]
        self.assertAlmostEqual(geo_transforms.mapper(5, 0, 10, 0, 100), 50)
        # Test mapping from [0, 10] to [100, 0]
        self.assertAlmostEqual(geo_transforms.mapper(5, 0, 10, 100, 0), 50)
        # Test mapping from [0, 10] to [0, -100]
        self.assertAlmostEqual(geo_transforms.mapper(5, 0, 10, 0, -100), -50)
        # Test mapping where input is outside the initial range
        self.assertAlmostEqual(geo_transforms.mapper(-5, -10, 0, 0, 100), 50)
        self.assertAlmostEqual(geo_transforms.mapper(15, 0, 10, 0, 100), 150)

    def test_coordinate_transformations_for_projection(self):
        """
        Test the transformations of 3D Cartesian coordinates based on projection settings.
        """
        # Example for testing: Transform a point with hypothetical projection parameters
        x, y, z = geo_transforms.lon_lat_to_xyz(0, 0)
        LIGHT_TO_SPHERE = 6
        LIGHT_TO_IMAGE = 1

        result_x, result_y, result_z = geo_transforms.coordinate_transformations_for_projection(x, y, z, LIGHT_TO_SPHERE, LIGHT_TO_IMAGE)

        # Here we use trigonometry to expect results
        expected_x = (x / (LIGHT_TO_SPHERE - x)) * LIGHT_TO_IMAGE
        expected_y = (y / (LIGHT_TO_SPHERE - x)) * LIGHT_TO_IMAGE
        expected_z = (z / (LIGHT_TO_SPHERE - x)) * LIGHT_TO_IMAGE

        self.assertAlmostEqual(result_x, expected_x)
        self.assertAlmostEqual(result_y, expected_y)
        self.assertAlmostEqual(result_z, expected_z)

    def test_utility_functions(self):
        """
        Test additional utility functions that are commonly used in various transformations.
        """
        # Degree to radian conversion for 180 degrees
        self.assertAlmostEqual(geo_transforms.deg_to_rad(180), math.pi)
        # Calculate the Euclidean distance between two points (0,0) and (1,1)
        self.assertAlmostEqual(geo_transforms.calculate_distance(0, 0, 1, 1), math.sqrt(2))
        # Linear interpolation between 0 and 10 for a midpoint
        self.assertAlmostEqual(geo_transforms.linear_interpolate(0, 10, 0.5), 5)

if __name__ == '__main__':
    unittest.main()
