import numpy as np
from scipy.spatial import KDTree
import pandas as pd

Rc = 8.0      # Radius in which we compute delta
L = 1000.0    # Simulation size (LBox)

file_path = '/path/to/simulation/file.h5'
columns_to_load = ['X', 'Y', 'Z', 'PID', 'M200c']
data = pd.read_hdf(file_path, key='rockstar_catalog', columns=columns_to_load)
x = data['X'].to_numpy()
y = data['Y'].to_numpy()
z = data['Z'].to_numpy()
main_halos = data['PID'].to_numpy()
mass = data['M200c'].to_numpy()

sel_mass = np.where((mass >= 2e10) & (main_halos==-1))[0]
x = x[sel_mass]
y = y[sel_mass]
z = z[sel_mass]

print("x min:", np.min(x), "x max:", np.max(x))
print("y min:", np.min(y), "y max:", np.max(y))
print("z min:", np.min(z), "z max:", np.max(z))

# Correction to ensure the position values remain inside the box
x = np.mod(x, L)
y = np.mod(y, L)
z = np.mod(z, L)

# Construction of the KDTree
tree = KDTree(np.column_stack((x, y, z)), boxsize=L)

# Function to find the neighbouring halos at a distance <= Rc
def compute_neighbors_batch(start, end):
    idx_list = tree.query_ball_point(np.column_stack((x[start:end], y[start:end], z[start:end])), Rc, p=2, workers=-1, return_length=True)
    return idx_list - 1     # Not counting the halo for which we compute

# Batch size, to save memory
batch_size = 50000
n_halos = np.zeros(len(x), dtype=int)

for i in range(0, len(x), batch_size):
    print(f"Processing batch {i} to {min(i + batch_size, len(x))}...")
    n_halos[i:i + batch_size] = compute_neighbors_batch(i, min(i + batch_size, len(x)))
    print("Total progress:", (i + batch_size) / len(x) * 100, "%")

# Computation of the average number of neighbouring halos and delta
N_mean = np.mean(n_halos)
delta = (n_halos - N_mean) / N_mean 

output = "/path/to/save/delta.csv"
np.savetxt(output, np.column_stack((x, y, z, delta)), delimiter=" ", header="x y z delta")