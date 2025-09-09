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
    return offset_sigma**2 +  Temp*kb/mCs*Ts**2 #Ts is time squared. 

#Let's try to reverse engineer this. Given a 1 mm cloud initially, what is the expansion for a cloud at 50 uK? 

sigma_initial = 1e-3  #1 mm cloud

sigma_t_sq = diffusion_fit(tof, sigma_initial, 50e-6)

print(np.sqrt(sigma_t_sq))

plt.scatter(tof, sigma_t_sq)
plt.show()

