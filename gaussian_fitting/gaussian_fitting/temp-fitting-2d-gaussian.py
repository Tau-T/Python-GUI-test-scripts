import numpy as np
import matplotlib.pyplot as plt
from tifffile import imread
from pathlib import Path
import re
from scipy import ndimage
from get_cloud_sigma import get_cloud_sigma
from scipy.optimize import curve_fit


kb = 1.38**-23
mCs = 133*1.67**-27

# Function to extract numbers from filenames
def numerical_sort(f):
    match = re.search(r'\d+', f.stem)  # f.stem is filename without extension
    return int(match.group()) if match else float('inf')

def diffusion_fit(Ts, offset_sigma, Temp):
    return offset_sigma**2 +  Temp*kb/mCs*Ts #Ts is time squared. 
#First let's load all of the images. Let's not worry about the background images quite yet. 
folder = Path(".")

# Get all .tif files except the background, sorted numerically
tif_files = sorted(
    [f for f in folder.iterdir() if f.suffix == ".tif" and f.name != "bkgd-image.tif"],
    key=numerical_sort
)

images = [
    imread(f) 
    for f in tif_files 
    if f.suffix == ".tif" and f.name != "bkgd-image.tif"
]

#create arrays to plot
tof = np.arange(5,35,5)
sigma_x = []
sigma_y = []

for i in tif_files:
    x, y = get_cloud_sigma(i)
    sigma_x.append(x)
    sigma_y.append(y)

print(sigma_x)
print(sigma_y)

#fit curves to the TOF traces

# --- Fit quadratics ---
# Initial guess:  offset sigma, temperature
x_guess = [ 50, 10e-5] 
y_guess = [ 50, 10e-5]

#indepent variable first then dependent variable. 
popt_x, _ = curve_fit(diffusion_fit, tof**2,sigma_x**2,  p0=x_guess)
popt_y, _ = curve_fit(diffusion_fit, tof**2,sigma_y**2,  p0=y_guess)

# --- Plot results ---
fig, axs = plt.subplots(1, 2, figsize=(12, 5)) #create a plot with one row and 2 columns. 


# Horizontal line
axs[0].plot(tof, np.array(sigma_x)**2, 'b', label='Data')
axs[0].plot(tof, diffusion_fit(tof**2, *popt_x), 'r--', label='temp fit')
axs[0].set_title("Horizontal cross section")
axs[0].set_xlabel("Time of flight (ms)")
axs[0].set_ylabel("Sigma_x")
axs[0].legend()


# Horizontal line
axs[1].plot(tof, np.array(sigma_y)**2, 'b', label='Data')
axs[1].set_title("Horizontal cross section")
axs[1].set_xlabel("Time of flight (ms)")
axs[1].set_ylabel("Sigma_y")
axs[1].legend()

plt.tight_layout()
plt.show()
print(sigma_x)