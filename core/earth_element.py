import numpy as np
import OpenGL.GL as gl
from utils.opengl_helpers import OpenGLHelpers
from utils.geo_transforms import GeoTransformer
import glfw

class EarthElement:
    """
    EarthElement represents a specific layer or type of data on the Earth's surface, such as continents,
    clouds, or hurricane paths. This class manages the data, its appearance, and its behavior in the simulation.
    
    Attributes:
        vertices (np.array): Array of vertex data.
        indices (np.array): Array of indices for indexed drawing.
        texture (GLuint): OpenGL texture ID if the element uses a texture.
        color (list): Default color of the element used if no texture is applied.
        shader_program (GLuint): OpenGL shader program used to render this element.
        update_interval (float): Time in seconds between data updates for dynamic data.
        last_update_time (float): Last time the data was updated.
        vertex_buffer (GLuint): Vertex Buffer Object (VBO) for vertex data.
        index_buffer (GLuint): Element Buffer Object (EBO) for index data.
    """
    
    def __init__(self, shader_program, color=None, texture_path=None, update_interval=None):
        """
        Initializes an EarthElement with optional texture, color, and dynamics.

        Args:
            shader_program (GLuint): Shader program used to render this element.
            color (list): Default color used if no texture is present.
            texture_path (str): Path to the texture image if used.
            update_interval (float): Time in seconds between updates for dynamic data.
        """
        self.vertices = None
        self.indices = None
        self.texture = None
        self.color = color if color else [1.0, 1.0, 1.0, 1.0]
        self.shader_program = shader_program
        self.update_interval = update_interval
        self.last_update_time = 0
        self.vertex_buffer = None
        self.index_buffer = None

        if texture_path:
            self.texture = OpenGLHelpers.load_texture(texture_path)

    def load_data(self, vertices, indices=None):
        """
        Loads the vertex and index data into OpenGL buffers.

        Args:
            vertices (list or np.array): Vertex data for this element.
            indices (list or np.array): Index data for indexed drawing, optional.
        """
        self.vertices = np.array(vertices, dtype=np.float32)
        if indices is not None:
            self.indices = np.array(indices, dtype=np.uint32)
        
        self.initialize_buffers()

    def initialize_buffers(self):
        """
        Initializes the vertex and index buffers in OpenGL.
        """
        self.vertex_buffer = OpenGLHelpers.create_buffer(self.vertices)
        if self.indices is not None:
            self.index_buffer = OpenGLHelpers.create_buffer(self.indices, buffer_type=gl.GL_ELEMENT_ARRAY_BUFFER)
        else:
            self.index_buffer = None

    def update(self, current_time):
        """
        Updates the element's data if necessary, based on its update interval.

        Args:
            current_time (float): The current time in seconds.
        """
        if self.update_interval is None:
            return
        
        if self.last_update_time is None or (current_time - self.last_update_time >= self.update_interval):
            # Here you would update your data
            self.last_update_time = current_time

    def render(self, projection_matrix, view_matrix):
        """
        Renders the element using OpenGL.

        Args:
            projection_matrix (np.array): The projection matrix from the camera.
            view_matrix (np.array): The view matrix from the camera.
        """
        gl.glUseProgram(self.shader_program)
        
        # Set up vertex array
        OpenGLHelpers.setup_vertex_array(self.vertex_buffer, 0, 3)

        if self.texture:
            OpenGLHelpers.set_uniform(self.shader_program, "textureSampler", 0, '1i')
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
        
        # Set shader uniforms
        OpenGLHelpers.set_uniform(self.shader_program, "color", self.color, '4f')
        OpenGLHelpers.set_uniform(self.shader_program, "projection", projection_matrix, 'mat4')
        OpenGLHelpers.set_uniform(self.shader_program, "view", view_matrix, 'mat4')
        
        # Draw the element
        if self.indices is not None:
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
            gl.glDrawElements(gl.GL_TRIANGLES, len(self.indices), gl.GL_UNSIGNED_INT, None)
        else:
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(self.vertices) // 3)
        
        # Clean up
        gl.glDisableVertexAttribArray(0)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
        gl.glUseProgram(0)

# Example of usage
if __name__ == '__main__':
    # Setup a window and OpenGL context
    if not glfw.init():
        raise Exception("GLFW can't be initialized")
    
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 480, "Hello World", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")

    # Make the window's context current
    glfw.make_context_current(window)

    # Initialize OpenGL
    OpenGLHelpers.initialize_opengl()

    # Create a shader program
    vertex_shader = """
    #version 330 core
    layout (location = 0) in vec3 aPos;
    uniform mat4 projection;
    uniform mat4 view;
    out vec3 vertexColor;
    void main() {
        gl_Position = projection * view * vec4(aPos, 1.0);
        vertexColor = vec3(0.5, 0.0, 0.0);
    }
    """
    fragment_shader = """
    #version 330 core
    in vec3 vertexColor;
    out vec4 FragColor;
    uniform vec4 color;
    void main() {
        FragColor = vec4(vertexColor * color.rgb, color.a);
    }
    """
    shader_program = OpenGLHelpers.link_shader_program(vertex_shader, fragment_shader)

    # Prepare some data for an EarthElement (simple triangle for demonstration)
    vertices = [
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        0.0, 0.5, 0.0
    ]
    
    # Initialize EarthElement
    earth_element = EarthElement(shader_program, color=[0.1, 0.2, 0.8, 1.0])
    earth_element.load_data(vertices)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render here
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Update and render EarthElement
        earth_element.render(np.eye(4), np.eye(4))

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()
