import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Make sure we are using SI units for all of this stuff. 
kb = 1.38e-23 #J/K
mCs = 133*1.67e-27 #kg

pixel_size_mag = 25e-6/7.24 #meters

tof = np.arange(.005,.035,.005) #seconds

sigma_x = np.array([64.5, 73.6, 89.6, 101.9, 127.5, 161.0])*pixel_size_mag
sigma_y = np.array([48.2, 64.0, 81.0, 99.6, 113.7, 128.8])*pixel_size_mag

def diffusion_fit(Ts, offset_sigma, Temp):
    return offset_sigma**2 +  Temp*kb/mCs*Ts #Ts is time squared. 

# --- Fit quadratics ---
# Initial guess:  offset sigma, temperature
x_guess = [ 50e-6, 10e-5] 
y_guess = [ 50e-6, 10e-5]

popt_x, _ = curve_fit(diffusion_fit, tof**2,sigma_x**2,  p0=x_guess)
popt_y, _ = curve_fit(diffusion_fit, tof**2,sigma_y**2,  p0=y_guess)

print("Startin cloud sigma_x is: ", popt_x[0])
print("Startin cloud sigma_y is: ", popt_y[0])

print("Temperature along gravity is: ", popt_x[1], "K")
print("Temperature perpendicular to gravity is ", popt_y[1], "K")

# Residuals
residuals_x = (sigma_x - np.sqrt(diffusion_fit(tof, *popt_x)))/sigma_x
residuals_y = (sigma_y - np.sqrt(diffusion_fit(tof, *popt_y)))/sigma_y

print("Relative X residuals are: ", residuals_x)
print("Relative Y residuals are: ", residuals_y)


# --- Plot results ---
fig, axs = plt.subplots(1, 2, figsize=(12, 5)) #create a plot with one row and 2 columns. 

# Horizontal line
axs[0].plot(tof, np.array(sigma_x)**2, 'b', label='Data')
axs[0].plot(tof, diffusion_fit(tof**2, *popt_x), 'r--', label='temp fit')
axs[0].set_title("Horizontal cross section")
axs[0].set_xlabel("Time of flight (s)")
axs[0].set_ylabel("Sigma_x")
axs[0].legend()

# Horizontal line
axs[1].plot(tof, np.array(sigma_y)**2, 'b', label='Data')
axs[1].plot(tof, diffusion_fit(tof**2, *popt_y), 'r--', label='temp fit')
axs[1].set_title("Horizontal cross section")
axs[1].set_xlabel("Time of flight (s)")
axs[1].set_ylabel("Sigma_y")
axs[1].legend()

plt.tight_layout()
plt.show()

print("Temperature along x is: ", popt_x[1])
print("Temeprature along y is: ", popt_y[1])
