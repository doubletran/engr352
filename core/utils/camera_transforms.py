import numpy as np

DEBUG_MODE = True

def debug_print(message):
    if DEBUG_MODE:
        print(message)

class Camera:
    """
    Camera class to manage the camera's state and simplify the view and projection matrix generation.
    """
    def __init__(self, position, target, up_vector, fov, aspect_ratio, near_plane, far_plane):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up_vector = np.array(up_vector, dtype=np.float32)
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near_plane = near_plane
        self.far_plane = far_plane
        
        debug_print(f"Camera initialized with position: {self.position}, target: {self.target}, up: {self.up_vector}")

    def get_view_matrix(self):
        """
        Generates a view matrix based on camera position, target, and up vector.
        """
        return self.look_at(self.position, self.target, self.up_vector)
  
    def get_projection_matrix(self):
        """
        Generates a perspective projection matrix based on FOV, aspect ratio, near, and far planes.
        """
        return self.perspective_projection(self.fov, self.aspect_ratio, self.near_plane, self.far_plane)

    def look_at(self, eye, target, up):
        """
        Generate a view matrix using the eye position, the target and the up vector.
        """
        f = np.subtract(target, eye)
        f /= np.linalg.norm(f)
        u = up / np.linalg.norm(up)
        s = np.cross(f, u)
        s /= np.linalg.norm(s)
        u = np.cross(s, f)

        view = np.array([
            [s[0], u[0], -f[0], 0],
            [s[1], u[1], -f[1], 0],
            [s[2], u[2], -f[2], 0],
            [-np.dot(s, eye), -np.dot(u, eye), np.dot(f, eye), 1]
        ], dtype=np.float32)

        debug_print(f"View Matrix:\n{view}")
        return view

    def perspective_projection(self, fov, aspect_ratio, near, far):
        """
        Generate a perspective projection matrix.
        """
        f = 1.0 / np.tan(np.radians(fov) / 2)
        proj = np.array([
            [f / aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), -1],
            [0, 0, (2 * far * near) / (near - far), 0]
        ], dtype=np.float32)

        debug_print(f"Projection Matrix:\n{proj}")
        return proj

    def update_position(self, new_position):
        """
        Update the camera position.
        """
        self.position = np.array(new_position, dtype=np.float32)
        debug_print(f"Camera position updated to: {self.position}")

    def update_target(self, new_target):
        """
        Update the camera target.
        """
        self.target = np.array(new_target, dtype=np.float32)
        debug_print(f"Camera target updated to: {self.target}")

if __name__ == '__main__':
    # Example usage
    camera = Camera(position=[0, 0, 3], target=[0, 0, 0], up_vector=[0, 1, 0], 
                    fov=45, aspect_ratio=800 / 600, near_plane=0.1, far_plane=100.0)

    view_matrix = camera.get_view_matrix()
    projection_matrix = camera.get_projection_matrix()

    debug_print("View Matrix:\n" + str(view_matrix))
    debug_print("\nProjection Matrix:\n" + str(projection_matrix))
