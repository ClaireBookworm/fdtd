"""
F = 400MHz
Simulation time: 10 periods (in terms of the EM waves)
Spatial configuration:
                2D plane only (you can also do a thin 3D slab instead if that’s what you prefer)
                FOV: 300cm x 300cm
                There is a 50cm x 50cm copper plate in the middle (if getting the right permissivity/permittivity values are difficult, just make it different from those of vacuum space)
                The rest of the space is filled by vacuum space
Dynamic configuration:
Incident plane EM waves are entering from left edge of the FOV for the first 3 periods, then no longer coming in – the rest of the dynamics is purely determined by the evolution of these incident waves.
Misc. notes:
                Use perfectly matched layer (PML) if possible for the boundaries
"""

# %% 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# %% 

# Simulation parameters
f = 400e6  # Frequency of EM wave (400 MHz)
c = 3e8  # Speed of light in vacuum (m/s)
lambda_ = c / f  # Wavelength (m) ( c0 = f * lambda0)
dx = lambda_ / 20  # Spatial resolution (m)
dt = dx / (2*c)  # Temporal resolution (s), Courant condition
size_x = 300  # Size of the FOV in cm
size_y = 300  # Size of the FOV in cm
nx = int(size_x / dx)  # Number of grid points in x
ny = int(size_y / dx)  # Number of grid points in y
simulation_time = 10 / f  # Total simulation time in seconds
nsteps = int(simulation_time / dt)  # Number of time steps

# %%
C = np.zeros((4,1))
N = C*C
print(C.shape)

# %%
# Material properties
epsilon_r = np.ones((nx, ny))  # Relative permittivity # (8000, 8000)
mu_r = np.ones((nx, ny))  # Relative permeability # (8000,8000)

# Place a copper plate in the middle with different permittivity (simplified)
plate_start_x = nx // 2 - int(50 / dx) // 2 # 3334
plate_end_x = nx // 2 + int(50 / dx) // 2  # 4666
plate_start_y = ny // 2 - int(50 / dx) // 2
plate_end_y = ny // 2 + int(50 / dx) // 2
epsilon_r[plate_start_x:plate_end_x, plate_start_y:plate_end_y] = 10  # Arbitrary higher permittivity

# %%

# Initialize fields
Ez = np.zeros((nx, ny)) # represents the electric field in the z direction
Hx = np.zeros((nx, ny)) # represents the magnetic field in the x direction
Hy = np.zeros((nx, ny)) # represents the magnetic field in the y direction
# all 8000 x 8000
# transverse magnetic field TM mode - we only want these fields because mag field is perpendicular to the plane of simulation, so Hz is 0; Ez, transverse to x-y 
# transverse electric mode (TE mode) - E field is perpendicular to x-y plane

def update_fields(Ez, Hx, Hy, n):
    """
    Update equations: 
    H (t+dt/2) = H (t-dt/2) - (dt / mu) * curl E (t)
    E (t+dt) = E (t) + (dt / epsilon) * curl H (t+dt/2)
    """

    # Update H fields
    Hx[:-1, :] -= dt / mu_r[:-1, :] * (Ez[1:, :] - Ez[:-1, :]) / dx
    Hy[:, :-1] += dt / mu_r[:, :-1] * (Ez[:, 1:] - Ez[:, :-1]) / dx
    
    # Update E field
    Ez[1:-1, 1:-1] += dt / epsilon_r[1:-1, 1:-1] * (
        (Hy[1:-1, 1:-1] - Hy[1:-1, :-2]) -
        (Hx[1:-1, 1:-1] - Hx[:-2, 1:-1])
    ) / dx
    
    # Incident wave for the first 3 periods
    if n < 3 * int(f / dt):
        Ez[:, 0] += np.sin(2 * np.pi * f * n * dt)
    
    return Ez, Hx, Hy

a, b, c = update_fields(Ez, Hx, Hy, 1)
print(a.shape, b.shape, c.shape)

# %%

# Visualization setup
fig, ax = plt.subplots(figsize=(8, 8))
img = ax.imshow(Ez.T, cmap='RdBu', animated=True, extent=[0, size_x, 0, size_y])

def animate(i):
    global Ez, Hx, Hy
    Ez, Hx, Hy = update_fields(Ez, Hx, Hy, i)
    img.set_array(Ez.T)
    return img,

ani = FuncAnimation(fig, animate, frames=nsteps, interval=20, blit=True)

plt.colorbar(img, ax=ax)
ax.set_xlabel('X (cm)')
ax.set_ylabel('Y (cm)')
ax.set_title('FDTD Simulation of EM Wave Interaction with Copper Plate')
plt.show()
# %%

"""
PML
- surrounding the simulation area with a layer of material that is designed to absorb EM waves
- as waves enter this layer they are gradaully attenuated until the yare completely absorbed, which minimal reflection back into simulation domain 
- desinging pML with spatially varying absorption coefficeint that increases with depth into the PML 
- key is its electrical properites are tailored so that for any angle of incidence and for any frequency, the waves are perfectly 

"""
# %%
import fdtd
fdtd.set_backend("numpy")
# Simulation parameters
frequency = 400e6  # Frequency in Hz
periods = 10  # Number of periods
fov = (300e-2, 300e-2)  # Field of view in meters
plate_size = (50e-2, 50e-2)  # Size of the copper plate in meters

# Spatial configuration
grid = fdtd.Grid(shape=(300, 300), grid_spacing=1e-2)
grid[125:175, 125:175].material = fdtd.Medium(epsilon_r=1, mu_r=1)  # Copper plate
grid.material = fdtd.Medium(epsilon_r=1, mu_r=1)  # Vacuum

# Dynamic configuration
sources = [
    fdtd.PointSource(
        (1, 150), 
        fdtd.GaussianPulse(frequency, cycles=3),
        component='ez'
    )
]

# Boundary conditions
pml_thickness = 10
grid[0:pml_thickness, :].pml(1)
grid[-pml_thickness:, :].pml(1)
grid[:, 0:pml_thickness].pml(1)
grid[:, -pml_thickness:].pml(1)

# Run simulation
sim = fdtd.Simulation(grid)
sim.add_sources(sources)
sim.run(total_time=periods / frequency)

# Visualization
sim.viz.field()


# %%
for _ in range(periods):
    grid.update()
# %%
import matplotlib.pyplot as plt

plt.imshow(grid.Ez.transpose(), cmap='RdBu', extent=[0, fov[0], 0, fov[1]])
plt.colorbar(label='Electric Field (Ez)')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('Electric Field Distribution')
plt.show()
