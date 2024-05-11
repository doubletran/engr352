# Earth Projection onto a Weather Balloon: Technical Documentation

This project aims to simulate the projection of a modified representation of the Earth onto a weather balloon using two projectors from different angles. This technical documentation describes the structure of the project and the purpose of each component. The setup uses Python and PyQt for the user interface, with OpenGL for rendering and GeoPandas for geographic computations.

## Project Structure

Here is an overview of the directory and file structure of the project:

```
earth_projection/
│
├── application.py          # Entry point of the application, manages main PyQt window
├── control_panel.py        # Manages the control panel UI and interactions
├── display_manager.py      # Manages the displays for the projectors and control panel mini-displays
├── earth_simulation.py     # Contains the base and modified Earth simulation logic
├── projection_settings.py  # Data structures and logic to manage projection settings
├── earth_element.py        # Manages specific Earth elements (e.g., continents, clouds) for rendering
│
├── utils/
│   ├── geo_transforms.py   # Geographical transformations and mapping functions
│   ├── opengl_helpers.py   # OpenGL helpers for Earth rendering and manipulations
│   └── camera_transforms.py    # Manages camera states and matrix generation for 3D transformations
│
└── resources/
    ├── ui/                 # UI layout files if using Qt Designer
    └── shaders/            # GLSL shaders for rendering Earth and other effects
```

### Detailed Component Descriptions

#### camera_transforms.py

- **Purpose:** Manages the camera's state and simplifies the generation of view and projection matrices for 3D transformations.
- **Functionality:**
  - `Camera` class to encapsulate the state and operations of a camera in 3D space.
  - `get_view_matrix()`: Generates a view matrix based on the camera's position, target, and up vector.
  - `get_projection_matrix()`: Generates a perspective projection matrix based on the camera's field of view, aspect ratio, near, and far planes.
  - `look_at()`: A static function to generate a view matrix using the eye position, the target, and the up vector.
  - `perspective_projection()`: A static function to generate a perspective projection matrix.

#### earth_element.py

- **Purpose:** Represents and manages a specific layer or type of data on the Earth's surface, such as continents, clouds, or paths of hurricanes.
- **Functionality:**
  - Manages vertex and index data for rendering.
  - Supports both color and texture-based rendering.
  - Can be updated dynamically based on time or other parameters.
  - `load_data()`: Loads vertex and optionally index data into OpenGL buffers.
  - `initialize_buffers()`: Initializes vertex and index buffers in OpenGL.
  - `update()`: Updates the element's data based on its update interval.
  - `render()`: Renders the element using OpenGL based on the provided projection and view matrices.

#### application.py

- **Purpose:** This is the main script that initializes and controls the main PyQt application window. It serves as the integration point for all other modules, orchestrating the user interface and the projection logic.
- **Functionality:**
  - Initialize the main PyQt application and the main window.
  - Integrate modules like `control_panel.py`, `display_manager.py`, and `earth_simulation.py` to create a cohesive application.
  - Handle the main event loop and ensure responsive UI interactions.

#### control_panel.py

- **Purpose:** Manages the UI and logic of the control panel, providing interactive controls to adjust both projector settings and global simulation parameters.
- **Functionality:**
  - Create and manage UI components such as sliders, buttons, and mini-display panels.
  - Implement signal and slot mechanisms to react to user inputs and adjust simulation parameters.
  - Provide mechanisms to save and load projection settings using JSON serialization.

#### display_manager.py

- **Purpose:** Manages the displays that the projectors use to project onto the balloon and updates the control panel mini-displays.
- **Functionality:**
  - Calculate what should be displayed by each projector based on the current settings and the Earth simulation data.
  - Adjust projections to prevent overlaps and manage the unlit 'night' section of the balloon.
  - Update mini-displays within the control panel to reflect the current projection status.

#### earth_simulation.py

- **Purpose:** Contains logic to manage the Earth simulation data, including the base and modified representations.
- **Functionality:**
  - `BaseEarthSimulation` class to load and hold the original Earth data, possibly from GeoPandas.
  - `ModifiedEarthSimulation` class to apply modifications (artistic or otherwise) to the base Earth data.
  - Support for real-time manipulation of the Earth data based on global settings adjusted via the control panel.

- **Updates:**
  - Now includes the management of `EarthElement` instances to modularize different layers or features of the Earth.
  - `load_geographic_data()`: Updated to create `EarthElement` instances from geographic data.
  - `add_element()`: Adds an `EarthElement` to the simulation for rendering.
  - `render()`: Updated to render all `EarthElement` instances using their specified projection and view settings.

#### projection_settings.py

- **Purpose:** Manages the data structures and logic to maintain and manipulate projection settings.
- **Functionality:**
  - Define data structures or classes to store settings like light distances, texture sizes, and other parameters relevant to the projection.
  - Implement functions to load and save these settings to facilitate persistence across sessions.

#### utils/geo_transforms.py

- **Purpose:** Provides geographic and Cartesian coordinate transformations necessary for projecting the Earth onto a spherical surface.
- **Functionality:**
  - `lon_lat_to_xyz(lon, lat)`: Function to convert geographic coordinates (longitude, latitude) into 3D Cartesian coordinates.
  - `mapper(x, oldMin, oldMax, newMin, newMax)`: Function to map a value from one range to another, useful in adjusting projection coordinates.

#### utils/opengl_helpers.py

- **Purpose:** Contains helper functions and classes for common OpenGL operations to support Earth rendering and other graphical manipulations.
- **Functionality:**
  - Setup and management of the OpenGL context.
  - Loading and compiling GLSL shaders from the `resources/shaders/` directory.
  - Utility functions for common OpenGL tasks like setting up viewports, handling textures, etc.


#### resources/ui/ and resources/shaders/

- **Potential Update:** You might need to update or add new shaders in `resources/shaders/` to support the rendering functionalities in `earth_element.py`, especially if there are specific visual effects or texturing needed for different Earth elements.

This structure provides a comprehensive overview of your enhanced project. Each component and utility now works towards creating a dynamic, interactive simulation of Earth projection onto a spherical surface.
### Resources Directory

#### resources/ui/

- **Purpose:** Contains UI layout files if using Qt Designer to design the application's user interface.
- **Usage:** These files are typically `.ui` files that PyQt can load, which describe the layout and properties of the UI components.

#### resources/shaders/

- **Purpose:** Contains GLSL shaders for rendering the Earth and implementing other visual effects in the OpenGL context.
- **Details:**
  - Vertex shaders and fragment shaders for various rendering effects.
  - Shaders might include simple texturing shaders, lighting computation shaders, or shaders for special effects like simulating day and night on the Earth's surface.

## Order to do stuff

To build a well-structured application for projecting the Earth onto a weather balloon using Python and PyQt, you should develop your codebase in a logical sequence that allows you to test and validate functionality as you go. Here’s a suggested order for working on the files, with explanations for each step:

### 1. **utils/geo_transforms.py**
   - **Why start here?** This module will contain all the geographic and Cartesian coordinate transformations. Starting with this allows you to define fundamental operations that other parts of your project will rely on, such as converting longitude and latitude to 3D coordinates on the globe.
   - **Key functions to implement:**
     - `lon_lat_to_xyz(lon, lat)`: Convert geographic coordinates to 3D Cartesian coordinates.
     - `mapper(x, oldMin, oldMax, newMin, newMax)`: Scale or map values from one range to another, useful for adjusting projections.

### 2. **utils/opengl_helpers.py**
   - **Why?** Before diving into rendering and projection logic, setting up utility functions for OpenGL will help in creating and managing the rendering context, shaders, and other OpenGL-specific operations.
   - **Key functionalities:**
     - Setting up an OpenGL context.
     - Loading and compiling shaders from the `resources/shaders/` directory.
     - Commonly used OpenGL functions like setting up viewports, handling textures, etc.

### 3. **projection_settings.py**
   - **Why?** This module will manage the projection settings, and having this done early makes it easier to adjust the settings interactively later on. It’s foundational because it will define how projections are manipulated and saved.
   - **Key structures to define:**
     - Data classes or structures to hold projection parameters like `LIGHT_TO_SPHERE`, `LIGHT_TO_IMAGE`, and `TEXTURE_SIZE`.
     - Functions for loading and saving these settings to a JSON file.

### 4. **earth_simulation.py**
   - **Why?** This module builds on the transformations and settings to create and manage Earth simulation data. You need the base and modified data ready before you can display them.
   - **Key classes and methods:**
     - `BaseEarthSimulation`: Load and maintain the base geographic data, potentially using GeoPandas as shown in your initial script.
     - `ModifiedEarthSimulation`: Apply artistic or other modifications to the base simulation.

### 5. **display_manager.py**
   - **Why?** Now that you have the data and settings, you can manage how the Earth is projected onto the sphere through the displays. This module will use the settings and transformed data to calculate what each projector should display.
   - **Key responsibilities:**
     - Manage the two main projector displays, calculating overlaps and ensuring correct projection based on the settings.
     - Update mini-displays in the control panel based on the current projections.

### 6. **control_panel.py**
   - **Why?** With most of the backend ready, you can now build the interactive control panel. This GUI will allow you to control the simulation parameters in real-time.
   - **Key features to implement:**
     - Sliders, dropdowns, or other widgets to adjust projection and simulation settings.
     - Buttons and functionality to load and save settings.
     - Miniature displays showing what each projector is outputting.

### 7. **application.py**
   - **Why last?** This is the main entry point of your application, and it ties everything together. By developing this last, you ensure all components are ready to be integrated.
   - **Main tasks:**
     - Initialize the main PyQt window.
     - Integrate the control panel and display outputs.
     - Set up the main application loop and ensure that all parts work together harmoniously.

### Resources and Shaders

- **resources/shaders/**: Can be developed in parallel with `opengl_helpers.py` as you will need shaders for rendering. Basic shaders for projecting the Earth would include vertex and fragment shaders for texture mapping and lighting.

- **resources/ui/**: If you use Qt Designer for your UI, you can design `.ui` files at any point, but you’ll integrate them when you work on `control_panel.py`.

By following this sequence, you ensure that each part of your application is ready when needed by subsequent parts, reducing the need for rework and allowing for incremental testing and development. This approach helps maintain a clear development flow and ensures that foundational components support more complex operations as you progress.