import numpy as np
import matplotlib.pyplot as plt
from tifffile import imread
from pathlib import Path
import re
from scipy import ndimage
from get_cloud_sigma import *
from scipy.optimize import curve_fit


#Make sure we are using SI units for all of this stuff. 
kb = 1.38e-23 #J/K
mCs = 133*1.67e-27 #kg

pixel_size_mag = 25e-6/7.24 #meters


# Function to extract numbers from filenames
def numerical_sort(f):
    match = re.search(r'\d+', f.stem)  # f.stem is filename without extension
    return int(match.group()) if match else float('inf')

def diffusion_fit(Ts, offset_sigma, Temp):
    return offset_sigma**2 +  Temp*kb/mCs*Ts**2 #Ts is linear time. 
#First let's load all of the images. Let's not worry about the background images quite yet. 
folder = Path("C:\\Users\\matth\\Documents\\Github\\Python-GUI-test\\gaussian_fitting\\gaussian_fitting")

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
tof = np.arange(.005,.035,.005) #seconds. 
# use Python lists for efficient appending
sigma_x_list = []
sigma_y_list = []
sigma_2d_x_list = []
sigma_2d_y_list = []
theta_mod_list = []

for i in tif_files:
    x, y = get_cloud_sigma(i)
    sigma_x_list.append(x)
    sigma_y_list.append(y)
    
    x2, y2, theta = fit_2d_gauss_sigma(i)
    sigma_2d_x_list.append(x2)
    sigma_2d_y_list.append(y2)
    theta_mod_list.append(theta)

# convert to numpy arrays after loop
sigma_x = np.array(sigma_x_list)
sigma_y = np.array(sigma_y_list)
sigma_2d_x = np.array(sigma_2d_x_list)
sigma_2d_y = np.array(sigma_2d_y_list)
theta_mod_arr = np.array(theta_mod_list)

print(sigma_x)
print(sigma_y)

print("2d gaussian fit parameters in this order: x, y, theta")
print(sigma_2d_x)
print(sigma_2d_y)
print(theta_mod_arr)

#fit curves to the TOF traces
#Multiply by pixel Magnification factor
sigma_x = sigma_x*pixel_size_mag
sigma_y = sigma_y*pixel_size_mag
sigma_2d_x = sigma_2d_x*pixel_size_mag
sigma_2d_y = sigma_2d_y*pixel_size_mag
# --- Fit quadratics ---
# Initial guess:  offset sigma, temperature
x_guess = [ 1e-3, 10e-5] 
y_guess = [ 1e-3, 10e-5]

#indepent variable first then dependent variable. 
popt_x, _ = curve_fit(diffusion_fit, tof,sigma_x**2,  p0=x_guess)
popt_y, _ = curve_fit(diffusion_fit, tof,sigma_y**2,  p0=y_guess)


#Fit using the 2D Gaussian data
popt_x_2d, _ = curve_fit(diffusion_fit, tof, sigma_2d_x**2, p0 = x_guess)
popt_y_2d, _ = curve_fit(diffusion_fit, tof, sigma_2d_y**2, p0 = y_guess)


# --- Plot results ---
fig, axs = plt.subplots(2, 2, figsize=(12, 5)) #create a plot with one row and 2 columns. 


# Horizontal line
axs[0,0].plot(tof, sigma_x**2, 'b', label='Data')
axs[0,0].plot(tof, diffusion_fit(tof, *popt_x), 'r--', label='temp fit')
axs[0,0].set_title("Horizontal cross section")
axs[0,0].set_xlabel("Time of flight (ms)")
axs[0,0].set_ylabel("Sigma_x")
axs[0,0].legend()


# Horizontal line
axs[0,1].plot(tof, sigma_y**2, 'b', label='Data')
axs[0,1].plot(tof, diffusion_fit(tof, *popt_y), 'r--', label = 'temp fit')
axs[0,1].set_title("Horizontal cross section")
axs[0,1].set_xlabel("Time of flight (ms)")
axs[0,1].set_ylabel("Sigma_y")
axs[0,1].legend()

axs[1,0].plot(tof, sigma_2d_x**2, 'b', label='Data')
axs[1,0].plot(tof, diffusion_fit(tof, *popt_x_2d), 'r--', label='temp fit')
axs[1,0].set_title("Horizontal cross section")
axs[1,0].set_xlabel("Time of flight (ms)")
axs[1,0].set_ylabel("Sigma_x_2d fit")
axs[1,0].legend()

axs[1,1].plot(tof, sigma_2d_y**2, 'b', label='Data')
axs[1,1].plot(tof, diffusion_fit(tof, *popt_y_2d), 'r--', label='temp fit')
axs[1,1].set_title("Horizontal cross section")
axs[1,1].set_xlabel("Time of flight (ms)")
axs[1,1].set_ylabel("Sigma_x_2d fit")
axs[1,1].legend()

plt.tight_layout()
plt.show()
print(sigma_x)

print("Temperature along x is: ", popt_x[1])
print("Temeprature along y is: ", popt_y[1])

print("2D Gaussian fit, Temperature x: ", popt_x_2d[1])
print("2D Gaussian fit, Temperature x: ", popt_y_2d[1])