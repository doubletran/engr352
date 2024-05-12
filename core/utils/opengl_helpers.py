import OpenGL.GL as gl
from OpenGL.GL import shaders
import glfw
from PIL import Image
import numpy as np

# Set DEBUG_MODE to True to enable debugging prints
DEBUG_MODE = True

def debug_print(message):
    if DEBUG_MODE:
        print(message)

class OpenGLHelpers:
    """
    OpenGLHelpers is a utility class that provides a suite of functions to facilitate the
    use of OpenGL for rendering.
    """

    @staticmethod
    def initialize_opengl():
        """
        Initialize the OpenGL context and set up necessary configurations.
        """
        debug_print("Initializing OpenGL context...")
        # Enable depth testing for proper depth calculations
        gl.glEnable(gl.GL_DEPTH_TEST)
        debug_print("Depth testing enabled.")

        # Enable blending for transparency
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        debug_print("Blending enabled.")

        # Enable face culling to improve performance
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glCullFace(gl.GL_BACK)
        debug_print("Face culling enabled.")

    @staticmethod
    def compile_shader(source, shader_type):
        """
        Compile a shader from source.
        Args:
            source (str): The GLSL source code for the shader.
            shader_type (GLenum): The type of shader (e.g., GL_VERTEX_SHADER, GL_FRAGMENT_SHADER).
        Returns:
            GLuint: The compiled shader object.
        """
        shader = gl.glCreateShader(shader_type)
        if not shader:
            raise ValueError(f"Failed to create shader of type {shader_type}")
        gl.glShaderSource(shader, source)
        gl.glCompileShader(shader)
        
        # Check compilation status
        if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(shader).decode()
            gl.glDeleteShader(shader)
            raise RuntimeError(f"Shader compilation failed: {error}")
        
        debug_print(f"Shader compiled successfully: {shader}")
        return shader

    @staticmethod
    def link_shader_program(vertex_source, fragment_source):
        """
        Create a shader program by compiling and linking vertex and fragment shaders.
        Args:
            vertex_source (str): GLSL source code for the vertex shader.
            fragment_source (str): GLSL source code for the fragment shader.
        Returns:
            GLuint: The linked shader program.
        """
        debug_print("Linking shader program...")
        vertex_shader = OpenGLHelpers.compile_shader(vertex_source, gl.GL_VERTEX_SHADER)
        fragment_shader = OpenGLHelpers.compile_shader(fragment_source, gl.GL_FRAGMENT_SHADER)
        program = gl.glCreateProgram()
        gl.glAttachShader(program, vertex_shader)
        gl.glAttachShader(program, fragment_shader)
        gl.glLinkProgram(program)
        
        # Check linking status
        if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
            error = gl.glGetProgramInfoLog(program).decode()
            gl.glDeleteProgram(program)
            raise RuntimeError(f"Shader linking failed: {error}")
        
        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)

        debug_print(f"Shader program linked successfully: {program}")
        return program

    @staticmethod
    def load_texture(image_path):
        """
        Load a texture from an image file.

        Args:
            image_path (str): The file path to the image to load as a texture.

        Returns:
            GLuint: The texture object ID.
        """
        debug_print(f"Loading texture from {image_path}...")
        # Load image with Pillow
        img = Image.open(image_path)
        img_data = np.array(list(img.getdata()), np.uint8)

        texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width, img.height, 0,
                        gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_data)

        # Set texture parameters
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        debug_print(f"Texture loaded and created with ID: {texture_id}")
        return texture_id

    @staticmethod
    def create_buffer(data, buffer_type=gl.GL_ARRAY_BUFFER):
        """
        Create a Buffer Object (VBO or EBO) and load data into it.

        Args:
            data (list or np.array): The vertex data or index data to load into the buffer.
            buffer_type (GLenum): The type of buffer (GL_ARRAY_BUFFER or GL_ELEMENT_ARRAY_BUFFER).

        Returns:
            GLuint: The buffer object ID.
        """
        debug_print("Creating buffer...")
        data = np.array(data, dtype=np.float32 if buffer_type == gl.GL_ARRAY_BUFFER else np.uint32)
        buffer_id = gl.glGenBuffers(1)
        gl.glBindBuffer(buffer_type, buffer_id)
        gl.glBufferData(buffer_type, data.nbytes, data, gl.GL_STATIC_DRAW)
        debug_print(f"Buffer created with ID: {buffer_id}")

        return buffer_id

    @staticmethod
    def set_uniform(shader_program, name, value, uniform_type='1f'):
        """
        Set a uniform value in the shader program.

        Args:
            shader_program (GLuint): The shader program ID.
            name (str): The name of the uniform.
            value (Union[float, tuple]): The value to set the uniform to.
            uniform_type (str): The type of the uniform ('1f', '3f', 'mat4', etc.).
        """
        location = gl.glGetUniformLocation(shader_program, name)
        if location == -1:
            raise ValueError(f"Uniform '{name}' not found in shader program.")

        debug_print(f"Setting uniform '{name}' to {value} on program {shader_program}")
        
        if uniform_type == '1f':
            gl.glUniform1f(location, value)
        elif uniform_type == '3f':
            gl.glUniform3f(location, *value)
        elif uniform_type == '4f':
            gl.glUniform4f(location, *value)
        elif uniform_type == '1i':
            gl.glUniform1i(location, value)
        elif uniform_type == 'mat4':
            gl.glUniformMatrix4fv(location, 1, gl.GL_TRUE, value)

    @staticmethod
    def setup_vertex_array(buffer_id, attribute_index, size, attribute_type=gl.GL_FLOAT, normalized=gl.GL_FALSE, stride=0, offset=None):
        """
        Set up a vertex attribute pointer and enable the vertex attribute array.

        Args:
            buffer_id (GLuint): The buffer ID.
            attribute_index (int): The attribute location in the shader.
            size (int): The number of components per attribute.
            attribute_type (GLenum): The data type of each component in the array.
            normalized (GLboolean): Whether fixed-point data values should be normalized.
            stride (int): The byte offset between consecutive vertex attributes.
            offset (ctypes.c_void_p): Offset of the first component in the array in the buffer.
        """
        debug_print(f"Setting up vertex array for buffer {buffer_id} at attribute {attribute_index}")
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer_id)
        gl.glVertexAttribPointer(attribute_index, size, attribute_type, normalized, stride, offset)
        gl.glEnableVertexAttribArray(attribute_index)

    @staticmethod
    def check_errors():
        """
        Check for any OpenGL errors and raise an exception if an error is found.
        """
        err = gl.glGetError()
        if err != gl.GL_NO_ERROR:
            raise RuntimeError(f'OpenGL error: {err}')
        else:
            debug_print("No OpenGL errors found.")

    @staticmethod
    def clear_screen():
        """
        Clear the color and depth buffers.
        """
        debug_print("Clearing screen...")
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    @staticmethod
    def set_viewport(x, y, width, height):
        """
        Set the viewport for rendering.

        Args:
            x (int): The lower left corner x-coordinate.
            y (int): The lower left corner y-coordinate.
            width (int): The width of the viewport.
            height (int): The height of the viewport.
        """
        debug_print(f"Setting viewport to x:{x}, y:{y}, width:{width}, height:{height}")
        gl.glViewport(x, y, width, height)

def main():
    # Initialize GLFW
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")
    debug_print("GLFW initialized.")

    # Create a window and its OpenGL context
    window = glfw.create_window(800, 600, "OpenGL Window", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")
    debug_print("GLFW window created.")

    # Make the OpenGL context current
    glfw.make_context_current(window)
    debug_print("OpenGL context made current.")

    # Initialize OpenGL
    OpenGLHelpers.initialize_opengl()

    # Vertex Shader
    vertex_shader_source = """
    #version 330 core
    layout (location = 0) in vec3 aPos;
    void main() {
        gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
    }
    """
    
    # Fragment Shader
    fragment_shader_source = """
    #version 330 core
    out vec4 FragColor;
    void main() {
        FragColor = vec4(1.0, 0.5, 0.2, 1.0);
    }
    """

    # Compile and link shaders
    shader_program = OpenGLHelpers.link_shader_program(vertex_shader_source, fragment_shader_source)
    gl.glUseProgram(shader_program)

    # Set up vertex data (and buffer(s)) and configure vertex attributes
    vertices = np.array([
        0.0,  0.5, 0.0,  # Top of the triangle (x, y, z)
        -0.5, -0.5, 0.0,  # Left corner
        0.5, -0.5, 0.0   # Right corner
    ], dtype=np.float32)

    # Create a buffer for the vertices
    vertex_buffer = OpenGLHelpers.create_buffer(vertices)

    # Set up the vertex array object
    vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vao)
    
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * vertices.itemsize, None)
    gl.glEnableVertexAttribArray(0)

    # Unbind the VAO first (it's a good practice)
    gl.glBindVertexArray(0)

    # Render loop
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        # Clear the screen at the start of each frame
        OpenGLHelpers.clear_screen()

        # Draw the triangle
        gl.glUseProgram(shader_program)
        gl.glBindVertexArray(vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    # Clean up
    gl.glDeleteVertexArrays(1, [vao])
    gl.glDeleteBuffers(1, [vertex_buffer])
    gl.glDeleteProgram(shader_program)
    glfw.terminate()

if __name__ == "__main__":
    main()
