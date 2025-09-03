import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
def rotated_gaussian_2d(x, y, x0, y0, sigma_x, sigma_y, amplitude, theta):
    """
    2D rotated Gaussian with different sigmas along x and y.
    theta: rotation angle (radians).
    """
    a = (np.cos(theta)**2) / (2*sigma_x**2) + (np.sin(theta)**2) / (2*sigma_y**2)
    b = -np.sin(2*theta) / (4*sigma_x**2) + np.sin(2*theta) / (4*sigma_y**2)
    c = (np.sin(theta)**2) / (2*sigma_x**2) + (np.cos(theta)**2) / (2*sigma_y**2)
    return amplitude * np.exp(-(a*(x-x0)**2 + 2*b*(x-x0)*(y-y0) + c*(y-y0)**2))

# Image parameters
size = 256
num_frames = 7
sigma_start = 3
sigma_step = 2
amplitude = 200
background_level = 10
noise_level = 5

# Coordinate grid
x = np.arange(size)
y = np.arange(size)
X, Y = np.meshgrid(x, y)

# Gaussian center
x0, y0 = size // 2, size // 2

# Pick random orientation for the first Gaussian
theta = np.random.uniform(0, np.pi)
print(f"Random orientation theta = {theta:.2f} rad")

# Different widths to make orientation visible
sigma_x0 = sigma_start
sigma_y0 = sigma_start / 2   # start elliptical

for i in range(num_frames):
    sigma_x = sigma_x0 + i * sigma_step
    sigma_y = sigma_y0 + i * sigma_step

    gaussian = rotated_gaussian_2d(X, Y, x0, y0, sigma_x, sigma_y, amplitude, theta)

    background = background_level + np.random.normal(0, noise_level, (size, size))
    image = gaussian + background

    image = np.clip(image, 0, 65535).astype(np.uint16)
    # plt.imshow(image)
    # plt.show()

    filename = f"gaussian_{i+1}.tif"
    tiff.imwrite(filename, image)
    print(f"Saved {filename}")
