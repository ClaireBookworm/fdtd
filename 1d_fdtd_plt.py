# fd3d 1 1 py 1d fdtd

import numpy as np 
from math import exp
from matplotlib import pyplot as plt

ke = 200 # number of cells
ex = np.zeros(ke)
hy = np.zeros(ke)

# pulse parameters
kc = int(ke / 2)
t0 = 40
spread = 12

# add boundary conditions
boundary_low = [0, 0]
boundary_high = [0, 0]

nsteps = 250

plotting_points = [
	{'num_steps': 100, 'data_to_plot': None, 'label': ''}, 
	{'num_steps': 225, 'data_to_plot': None, 'label': ''}, 
	{'num_steps': 250, 'data_to_plot': None, 'label': 'FDTD cells'}
]

# main fdtd loop
for time_step in range(1, nsteps+1):
	# calc the Ex field
	for k in range(1, ke):
		ex[k] = ex[k] + 0.5 * (hy[k-1] - hy[k]) # difference equation
	
	# put gaussian pulse in the middle
	pulse = exp(-0.5 * ((t0 - time_step) / spread) ** 2)
	ex[kc] = pulse # put pulse in the middle
    
	# Absorbing Boundary Conditions
	ex[0] = boundary_low.pop(0)
	boundary_low.append(ex[1])
	ex[ke - 1] = boundary_high.pop(0)
	boundary_high.append(ex[ke - 2])

	# calc the Hy field
	for k in range(ke-1):
		hy[k] = hy[k] + 0.5 * (ex[k] - ex[k+1]) # difference equation

	# Save data at certain points for later plotting
	for plotting_point in plotting_points:
		if time_step == plotting_point['num_steps']:
			plotting_point['data_to_plot'] = np.copy(ex)

# Plot the outputs as shown in Fig. 1.3
plt.rcParams['font.size'] = 12
fig = plt.figure(figsize=(8, 5.25))
def plot_e_field(data, timestep, label):
    """Plot of E field at a single time step"""
    plt.plot(data, color='k', linewidth=1)
    plt.ylabel('E$_x$', fontsize='14')
    plt.xticks(np.arange(0, 199, step=20))
    plt.xlim(0, 199)
    plt.yticks(np.arange(0, 1.2, step=1))
    plt.ylim(-0.2, 1.2)
    plt.text(100, 0.5, 'T = {}'.format(timestep),
             horizontalalignment='center')
    plt.xlabel('{}'.format(label))
# Plot the E field at each of the time steps saved earlier
for subplot_num, plotting_point in enumerate(plotting_points):
    ax = fig.add_subplot(3, 1, subplot_num + 1)
    plot_e_field(plotting_point['data_to_plot'],
                 plotting_point['num_steps'],
                 plotting_point['label'])
plt.tight_layout()
plt.show()