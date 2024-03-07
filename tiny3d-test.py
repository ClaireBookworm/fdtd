# %%
# standard python imports
import numpy as np
import matplotlib.pyplot as plt

# tidy3d imports
import tidy3d as td
import tidy3d.web as web
# %% 

# make the geometry object representing the circular solid
cylinder = td.Cylinder(
	center=(0, 0, 0),  # center of the cylinder
	radius=0.5,  # radius of the cylinder
	length=1.0,  # length of the cylinder
	axis=2,  # axis along which the cylinder is aligned
)

# define material properties of the cylinder
medium = td.Medium(permittivity=2)

# create a structure composed of the geometry and the medium
structure = td.Structure(geometry=cylinder, medium=medium)

# to make sure the simulation runs correctly, let's also make a reference cylinder the usual way
cylinder_ref = td.Cylinder(
	center=(0, 0, 0),  # center of the cylinder
	radius=0.5,  # radius of the cylinder
	height=1.0,  # height of the cylinder
	axis="z",  # axis along which the cylinder is aligned
)

# make the reference structure
structure_ref = td.Structure(geometry=cylinder_ref, medium=medium)

wavelength = 0.3
f0 = td.C_0 / wavelength / np.sqrt(medium.permittivity)

# set the domain size in x, y, and z
domain_size = 2.5

# construct simulation size array
sim_size = (domain_size, domain_size, domain_size)

# Bandwidth in Hz
fwidth = f0 / 40.0

# Gaussian source offset; the source peak is at time t = offset/fwidth
offset = 4.0

# time dependence of sources
source_time = td.GaussianPulse(freq0=f0, fwidth=fwidth, offset=offset)

# Simulation run time past the source decay (around t=2*offset/fwidth)
run_time = 40 / fwidth
# %%
# create a plane wave source
source = td.PlaneWave(
	center=(0, 0, -1),
	source_time=source_time,
	size=(td.inf, td.inf, 0),
	direction="+",
	medium=medium,  # specify the medium for the source
)

# these monitors will be used to plot fields on planes through the middle of the domain in the frequency domain
# STL simulation
sim = td.Simulation(
	size=sim_size,
	grid_spec=td.GridSpec.auto(min_steps_per_wvl=20),
	sources=[source],
	structures=[structure],
	monitors=[monitor_xz, monitor_yz, monitor_xy],
	run_time=run_time,
	boundary_spec=td.BoundarySpec.all_sides(td.PML()),
)

# reference simulation
sim_ref = td.Simulation(
	size=sim_size,
	grid_spec=td.GridSpec.auto(min_steps_per_wvl=20),
	sources=[td.PlaneWave(
		center=(0, 0, -1),
		source_time=source_time,
		size=(td.inf, td.inf, 0),
		direction="+",
		medium=medium,  # specify the medium for the source
	)],
	structures=[structure_ref],
	monitors=[monitor_xz, monitor_yz, monitor_xy],
	run_time=run_time,
	boundary_spec=td.BoundarySpec.all_sides(td.PML()),
)

# plot both simulations to make sure everything is set up correctly
_, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
sim.plot(y=0, ax=ax1)
sim_ref.plot(y=0, ax=ax2)
plt.show()
# %%
