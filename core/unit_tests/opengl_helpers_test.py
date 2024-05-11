import unittest
from unittest.mock import patch, MagicMock
from utils import opengl_helpers

class TestOpenGLHelpers(unittest.TestCase):

    def setUp(self):
        """
        Set up any necessary data or state before each test is run.
        """
        # This is where you would initialize OpenGL context if needed,
        # but for unit testing, we are mocking these dependencies.
        pass

    def test_initialize_opengl(self):
        """
        Test the initialization of the OpenGL context and basic setup.
        """
        with patch('OpenGL.GL.glEnable') as mock_gl_enable:
            try:
                opengl_helpers.initialize_opengl()
                self.assertTrue(mock_gl_enable.called)
            except Exception as e:
                self.fail(f"OpenGL initialization failed with an unexpected error: {e}")

    def test_compile_shader(self):
        """
        Test compiling a shader from source.
        """
        with patch('OpenGL.GL.shaders.compileShader', return_value=MagicMock()) as mock_compile_shader:
            shader_source = "void main() { gl_Position = vec4(0.0); }"
            shader_type = opengl_helpers.GL_VERTEX_SHADER

            try:
                shader = opengl_helpers.compile_shader(shader_source, shader_type)
                self.assertIsNotNone(shader)
                mock_compile_shader.assert_called_once()
            except Exception as e:
                self.fail(f"Shader compilation failed with an unexpected error: {e}")

    def test_link_shader_program(self):
        """
        Test linking shaders into a shader program.
        """
        with patch('OpenGL.GL.shaders.compileShader', return_value=MagicMock()), \
             patch('OpenGL.GL.shaders.compileProgram', return_value=MagicMock()) as mock_compile_program:

            vertex_shader = "void main() { gl_Position = vec4(0.0); }"
            fragment_shader = "void main() { gl_FragColor = vec4(1.0); }"

            try:
                program = opengl_helpers.link_shader_program(vertex_shader, fragment_shader)
                self.assertIsNotNone(program)
                mock_compile_program.assert_called_once()
            except Exception as e:
                self.fail(f"Shader program linking failed with an unexpected error: {e}")

    def test_load_texture(self):
        """
        Test loading a texture from an image file.
        """
        with patch('OpenGL.GL.glGenTextures', return_value=1), \
             patch('PIL.Image.open'), \
             patch('OpenGL.GL.glBindTexture'), \
             patch('OpenGL.GL.glTexImage2D'), \
             patch('OpenGL.GL.glGenerateMipmap'):
            
            try:
                texture_id = opengl_helpers.load_texture("path/to/fake/image.png")
                self.assertIsNotNone(texture_id)
                self.assertEqual(texture_id, 1)
            except Exception as e:
                self.fail(f"Texture loading failed with an unexpected error: {e}")

    def test_create_buffer(self):
        """
        Test creating a vertex buffer object (VBO).
        """
        with patch('OpenGL.GL.glGenBuffers', return_value=1), \
             patch('OpenGL.GL.glBindBuffer'), \
             patch('OpenGL.GL.glBufferData'):
            
            try:
                buffer_id = opengl_helpers.create_buffer([0.0, 1.0, 2.0, 3.0])
                self.assertIsNotNone(buffer_id)
                self.assertEqual(buffer_id, 1)
            except Exception as e:
                self.fail(f"Buffer creation failed with an unexpected error: {e}")

    def test_set_uniform(self):
        """
        Test setting a uniform value in a shader program.
        """
        with patch('OpenGL.GL.glUseProgram'), \
             patch('OpenGL.GL.glGetUniformLocation', return_value=0), \
             patch('OpenGL.GL.glUniform1f'):
            
            try:
                success = opengl_helpers.set_uniform(1, "some_uniform", 1.0)
                self.assertTrue(success)
            except Exception as e:
                self.fail(f"Setting uniform failed with an unexpected error: {e}")

if __name__ == '__main__':
    unittest.main()
