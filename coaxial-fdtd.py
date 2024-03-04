# %%
import fdtd
import numpy as np
# %%
# Grid parameters
length = 200e-6  # length of the coaxial cable in meters
grid_resolution = 1e-6  # grid resolution in meters
grid_size_x = int(length / grid_resolution)
grid_size_yz = 100  # assuming a square cross-section for simplicity

# Create the FDTD grid
grid = fdtd.Grid(
    shape=(grid_size_x, grid_size_yz, grid_size_yz), grid_spacing=grid_resolution
)

# Material parameters
permittivity_conductor = -1e5  # Using a negative permittivity for conductors

# Coaxial cable parameters
radius_inner = 20  # grid cells
radius_outer = 40  # grid cells
center_yz = grid_size_yz // 2

# Define the coaxial cable structure
for x in range(grid_size_x):
    for y in range(grid_size_yz):
        for z in range(grid_size_yz):
            distance_from_center = np.sqrt((y - center_yz)**2 + (z - center_yz)**2)
            if distance_from_center <= radius_inner or (radius_outer >= distance_from_center > radius_inner):
                grid[x, y, z].permittivity = permittivity_conductor

# Source and simulation parameters
source_position = (10, center_yz, center_yz)  # Position of the source in the grid
frequency = 1e9  # Frequency of the source in Hz
wavelength = grid.grid_spacing * grid.c / frequency
source = fdtd.PointSource(position=source_position, period=1/frequency, name="coax_source")
grid.add_source(source)

# Boundary conditions
grid.xlow_bc = grid.xhigh_bc = "open"
grid.ylow_bc = grid.yhigh_bc = grid.zlow_bc = grid.zhigh_bc = "open"

# Run the simulation
grid.run(total_time=1e-9)  # Run for a specific total time in seconds

# Visualization
# This would need customization based on what you want to visualize (E-field, H-field, etc.)

# %%
