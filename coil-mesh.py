# %%
import numpy as np
import trimesh 
import pickle
import fdtd
# %%
# attach to logger so trimesh messages will be printed to console
# trimesh.util.attach_to_log()

mesh = trimesh.load_mesh('cable.stl')
# %%
mesh.is_watertight # should be True

# the convex hull is another Trimesh object that is available as a property
# lets compare the volume of our mesh with the volume of its convex hull
print(mesh.volume / mesh.convex_hull.volume)

# since the mesh is watertight, it means there is a
# volumetric center of mass which we can set as the origin for our mesh
mesh.vertices -= mesh.center_mass
# %%
mesh.split()
# facets are groups of coplanar adjacent faces
# set each facet to a random color
# colors are 8 bit RGBA by default (n, 4) np.uint8
for facet in mesh.facets:
    mesh.visual.face_colors[facet] = trimesh.visual.random_color()


mesh.show()
# %%
CALCULATE = False
if CALCULATE:
	volume = mesh.voxelized(pitch=1)
	mat = volume.matrix
	# mesh.contains(points)
	print(volume)
	#xport mat to pickle
	with open('cable-pitch1.pkl', 'wb') as f:
		pickle.dump(mat, f)

LOAD = True
# load pickle file 
if LOAD:
	with open('cable-pitch1.pkl', 'rb') as f:
		mat = pickle.load(f)
	# print(mat)

# %%
# Grid parameters
length = 126e-9  # length of the coaxial cable (126 mm)
grid_resolution = 1e-9  # grid resolution in millimeters
grid_size_x = 150
grid_size_yz = 150  # assuming a square cross-section for simplicity
# %%
# Create the FDTD grid
grid = fdtd.Grid(
    shape=(grid_size_x, grid_size_yz, grid_size_yz), grid_spacing=grid_resolution
)
print(grid)
print(mat.shape)
# %%
fdtd.set_backend("numpy")

frequency = 400e6  # Frequency in Hz
periods = 10  # Number of periods

# grid[50:100, 115:120, 0] = fdtd.LineSource(name="source")
# poinrt source in middle 
grid[55, 55, 0] = fdtd.PointSource(name="source")
# create object from mat into fdtd (trimesh object)
# Material parameters
permittivity_conductor = 0.1

mx, my, mz = mat.shape
print(mat.shape)
# grid[0:mx, 0:my, 0:mz] = fdtd.Object(permittivity=permittivity_conductor, name="cables")
# %%

refractive_index = 1.7
x = y = np.linspace(-1,1,150)
X, Y = np.meshgrid(x, y)
circle_mask = X**2 + Y**2 < 1
permittivity = np.ones((150,150, 1))
permittivity += circle_mask[:,:,None]*(refractive_index**2 - 1)
grid[0:mx, 0:my, 0:mz] = fdtd.Object(permittivity=permittivity, name="outer")


# grid[mx//2:mx, 0:my//2, 0:mz] = fdtd.Object(permittivity=permittivity, name="inner")


# grid.add_object(coils)
# %%
# Boundary conditions
# pml_thickness = 10
# grid[0:pml_thickness, :].pml(1)
# grid[-pml_thickness:, :].pml(1)
# grid[:, 0:pml_thickness].pml(1)
# grid[:, -pml_thickness:].pml(1)
# %%
# Run simulation
grid.run(total_time=5e-17) 
# %%
import matplotlib.pyplot as plt
grid.visualize(z=0, show=False)
# %%
