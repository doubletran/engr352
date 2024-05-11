import numpy as np
from utils.geo_transforms import GeoTransformer

class ProjectionSettings:
    """
    Manages the projection parameters and calculations for mapping the Earth onto a spherical display.

    Attributes:
        light_to_sphere (float): Distance from the projection center to the sphere surface.
        light_to_image (float): Distance from the projection center to the image plane.
        texture_size (int): Size of the texture for the Earth's surface projection.
        radius_display (float): Radius for the display projection on the sphere.
        geo_transformer (GeoTransformer): Instance of GeoTransformer for coordinate transformations.
    """

    def __init__(self, light_to_sphere=6.0, light_to_image=1.0, texture_size=100, radius_display=6371.0):
        """
        Initializes the ProjectionSettings with default or provided projection parameters.

        Args:
            light_to_sphere (float): Distance from the light source to the sphere surface.
            light_to_image (float): Distance from the light source to the image plane.
            texture_size (int): Texture size for the projection.
            radius_display (float): Radius used for the display projection calculations.
        """
        self.light_to_sphere = light_to_sphere
        self.light_to_image = light_to_image
        self.texture_size = texture_size
        self.radius_display = radius_display
        self.geo_transformer = GeoTransformer(self.radius_display)

    def update_settings(self, **kwargs):
        """
        Updates projection settings based on provided keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments corresponding to projection attributes.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: {key} is not a valid attribute of ProjectionSettings and will be ignored.")

        # Update the GeoTransformer instance if the earth radius changes
        if 'radius_display' in kwargs:
            self.geo_transformer = GeoTransformer(self.radius_display)

    def get_projected_coordinates(self, lon, lat):
        """
        Projects geographic coordinates onto the sphere based on current settings.

        Args:
            lon (float): Longitude in degrees.
            lat (float): Latitude in degrees.

        Returns:
            tuple: Projected (x, y, z) coordinates on the sphere.
        """
        x, y, z = self.geo_transformer.lon_lat_to_xyz(lon, lat)
        # Apply the projection transformation
        i, j, z = self.geo_transformer.coordinate_transformations_for_projection(
            x, y, z, self.light_to_sphere, self.light_to_image
        )
        return i, j, z

    def map_to_texture_coordinates(self, x, y):
        """
        Maps 3D coordinates on the sphere to 2D texture coordinates.

        Args:
            x (float): The x coordinate on the sphere.
            y (float): The y coordinate on the sphere.

        Returns:
            tuple: Mapped (u, v) texture coordinates.
        """
        u = self.geo_transformer.mapper(x, -self.radius_display, self.radius_display, 0, self.texture_size)
        v = self.geo_transformer.mapper(y, -self.radius_display, self.radius_display, 0, self.texture_size)
        return u, v

    def visualize_projection(self):
        """
        Generates a simple visualization of the current projection for debugging purposes.
        """
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        fig, ax = plt.subplots()
        ax.set_xlim(-self.radius_display, self.radius_display)
        ax.set_ylim(-self.radius_display, self.radius_display)
        ax.set_aspect('equal', 'box')

        # Draw sphere outline
        circle = patches.Circle((0, 0), self.radius_display, fill=False, color='blue', linestyle='dashed')
        ax.add_patch(circle)

        # Example points to project
        example_points = [(-90, 0), (0, 0), (90, 0), (0, 90), (0, -90)]
        for lon, lat in example_points:
            x, y, z = self.get_projected_coordinates(lon, lat)
            u, v = self.map_to_texture_coordinates(x, y)
            ax.plot(x, y, 'ro')  # Projected point on sphere
            ax.text(x, y, f'({lon}, {lat})', color='red')

            # Draw lines from the sphere to the texture map position
            ax.plot([x, u], [y, v], 'gray', linestyle='dotted')
            ax.plot(u, v, 'gs')  # Corresponding point on texture

        plt.xlabel('X coordinate')
        plt.ylabel('Y coordinate')
        plt.title('Projection Visualization')
        plt.grid(True)
        plt.show()

# If this module is run as the main module, demonstrate its capabilities
if __name__ == '__main__':
    # Create an instance of ProjectionSettings
    proj_settings = ProjectionSettings()

    # Update settings if needed
    proj_settings.update_settings(light_to_sphere=6.0, light_to_image=1.0, texture_size=100, radius_display=6371.0)

    # Print some example projected coordinates
    print("Projected Coordinates for (0, 0):", proj_settings.get_projected_coordinates(0, 0))
    print("Projected Coordinates for (90, 0):", proj_settings.get_projected_coordinates(90, 0))
    print("Projected Coordinates for (0, 90):", proj_settings.get_projected_coordinates(0, 90))

    # Visualize the projection
    proj_settings.visualize_projection()
