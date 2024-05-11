import numpy as np

class Camera:
  """
  Camera class to manage the camera's state and simplify the view and projection matrix generation.
  """
  def __init__(self, position, target, up_vector, fov, aspect_ratio, near_plane, far_plane):
    self.position = np.array(position)
    self.target = np.array(target)
    self.up_vector = np.array(up_vector)
    self.fov = fov
    self.aspect_ratio = aspect_ratio
    self.near_plane = near_plane
    self.far_plane = far_plane
  
  def get_view_matrix(self):
    """
    Generates a view matrix based on camera position, target, and up vector.
    """
    return look_at(self.position, self.target, self.up_vector)
  
  def get_projection_matrix(self):
    """
    Generates a perspective projection matrix based on FOV, aspect ratio, near, and far planes.
    """
    return perspective_projection(self.fov, self.aspect_ratio, self.near_plane, self.far_plane)

def look_at(eye, target, up):
    """
    Generate a view matrix using the eye position, the target and the up vector.
    Args:
        eye (list or np.array): The eye or camera position.
        target (list or np.array): The position where the camera looks at.
        up (list or np.array): The up vector.
    Returns:
        np.array: The view matrix.
    """
    eye = np.array(eye, dtype=np.float32)
    target = np.array(target, dtype=np.float32)
    up = np.array(up, dtype=np.float32)

    f = target - eye
    f /= np.linalg.norm(f)
    u = up
    u /= np.linalg.norm(u)
    s = np.cross(f, u)
    s /= np.linalg.norm(s)
    u = np.cross(s, f)

    return np.array([
        [s[0], s[1], s[2], -np.dot(s, eye)],
        [u[0], u[1], u[2], -np.dot(u, eye)],
        [-f[0], -f[1], -f[2], np.dot(f, eye)],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def perspective_projection(fov, aspect_ratio, near, far):
  """
  Generate a perspective projection matrix.

  Args:
    fov (float): Field of View angle in degrees.
    aspect_ratio (float): Aspect ratio of the viewport.
    near (float): Near clipping plane.
    far (float): Far clipping plane.

  Returns:
    np.array: The perspective projection matrix.
  """
  f = 1.0 / np.tan(np.radians(fov) / 2)
  return np.array([
    [f / aspect_ratio, 0, 0, 0],
    [0, f, 0, 0],
    [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
    [0, 0, -1, 0]
  ], dtype=np.float32)

if __name__ == '__main__':
    # Example usage
    camera = Camera(position=[0, 0, 3], target=[0, 0, 0], up_vector=[0, 1, 0], 
                    fov=45, aspect_ratio=1.0, near_plane=0.1, far_plane=100.0)

    view_matrix = camera.get_view_matrix()
    projection_matrix = camera.get_projection_matrix()

    print("View Matrix:\n", view_matrix)
    print("\nProjection Matrix:\n", projection_matrix)