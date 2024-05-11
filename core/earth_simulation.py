#not working yet
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
import OpenGL.GL as gl
import glfw
from urllib.request import urlopen
import json
from utils.opengl_helpers import OpenGLHelpers
from utils.geo_transforms import GeoTransformer
from projection_settings import ProjectionSettings
from earth_element import EarthElement

class EarthSimulation:
    """
    EarthSimulation manages the entire Earth projection simulation,
    including loading geographic data, managing Earth elements,
    and rendering them based on current projection settings.
    """
    def __init__(self):
        # Initialize the simulation with some global settings
        self.projection_settings = ProjectionSettings()
        self.elements = []
        self.geo_transformer = GeoTransformer(self.projection_settings.radius_display)

    def load_geographic_data(self, url):
        """
        Loads geographic data from a GeoJSON URL and initializes the Earth elements.

        Args:
            url (str): The URL to the GeoJSON file containing geographic data.
        """
        with urlopen(url) as response:
            data = json.load(response)
        world_gdf = gpd.GeoDataFrame.from_features(data["features"])

        # Convert MultiPolygon to Polygon if necessary
        flattened = []
        for shape in world_gdf['geometry']:
            if isinstance(shape, MultiPolygon):
                flattened.extend(list(shape.geoms))
            else:
                flattened.append(shape)

        # Initialize the continental data as an EarthElement
        vertices = []
        indices = []
        current_index = 0
        for polygon in flattened:
            if polygon.exterior is not None:
                # Transform the geographic coordinates to projection coordinates
                projected_coords = []
                for lon, lat in polygon.exterior.coords:
                    x, y, z = self.geo_transformer.lon_lat_to_xyz(lon, lat)
                    projected_coords.append((x, y, z))

                # Flatten the list of tuples and extend the vertices list
                vertices.extend(np.array(projected_coords).flatten())

                # Create indices for this polygon (assuming triangles fan for simplicity)
                indices.extend([current_index + i for i in range(len(projected_coords))])
                current_index += len(projected_coords)

        # Convert vertices and indices into numpy arrays
        vertices = np.array(vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)

        # Shader code
        vertex_shader = """
        #version 330 core
        layout (location = 0) in vec3 aPos;
        uniform mat4 projection;
        uniform mat4 view;
        void main() {
            gl_Position = projection * view * vec4(aPos, 1.0);
        }
        """
        fragment_shader = """
        #version 330 core
        out vec4 FragColor;
        void main() {
            FragColor = vec4(0.5, 0.7, 0.5, 1.0);  // Earth color
        }
        """

        shader_program = OpenGLHelpers.link_shader_program(vertex_shader, fragment_shader)

        continent_element = EarthElement(shader_program, color=[0.5, 0.7, 0.5, 1.0])
        continent_element.load_data(vertices, indices)
        self.add_element(continent_element)

    def add_element(self, element):
        """
        Adds an EarthElement to the simulation.

        Args:
            element (EarthElement): The Earth element to be added.
        """
        self.elements.append(element)

    def render(self):
        """
        Renders all Earth elements using their specified projection and view settings.
        """
        projection_matrix = np.eye(4)  # Identity matrix for simplicity, replace with real projection
        view_matrix = np.eye(4)  # Identity matrix for simplicity, replace with real view

        for element in self.elements:
            element.render(projection_matrix, view_matrix)

    def run(self):
        """
        The main loop of the simulation where the Earth is rendered.
        """
        if not glfw.init():
            raise Exception("GLFW can't be initialized")

        # Create a windowed mode window and its OpenGL context
        window = glfw.create_window(640, 480, "Earth Simulation", None, None)
        if not window:
            glfw.terminate()
            raise Exception("GLFW window can't be created")

        # Make the window's context current
        glfw.make_context_current(window)

        # Initialize OpenGL
        OpenGLHelpers.initialize_opengl()

        while not glfw.window_should_close(window):
            # Render here
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            # Update and render EarthElement
            self.render()

            # Swap front and back buffers
            glfw.swap_buffers(window)

            # Poll for and process events
            glfw.poll_events()

        glfw.terminate()

# Example usage
if __name__ == '__main__':
    simulation = EarthSimulation()
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    simulation.load_geographic_data(url)
    simulation.run()
