import numpy as np
import matplotlib.pyplot as plt
from tifffile import imread
from scipy.optimize import curve_fit

def get_cloud_sigma(image_path):
    # --- Gaussian function ---
    def gaussian(x, A, x0, sigma, offset):
        return A * np.exp(-(x - x0)**2 / (2 * sigma**2)) + offset

    #First let's load all of the images. Let's not worry about the background images quite yet. 
    # --- Load image ---
    # image_path = "image_174049.tif"  # <-- change to your file name
    image = imread(image_path)

    # --- Display basic info ---
    print(f"Image shape: {image.shape}")
    print(f"Image dtype: {image.dtype}")
    print(f"Max pixel value: {np.max(image)}")

    # --- Display image ---
    plt.figure(figsize=(8, 6))
    plt.imshow(image, cmap='jet', vmin=0, vmax=np.max(image))
    plt.title("Click on a point to analyze")
    plt.xlabel("X pixels")
    plt.ylabel("Y pixels")
    plt.colorbar(label="Pixel value")

    # --- Use ginput to select a point ---
    print("Click on a point in the image...")
    x_click, y_click = plt.ginput(1)[0]
    x_click = int(round(x_click))
    y_click = int(round(y_click))
    plt.close()

    print(f"Selected pixel: x={x_click}, y={y_click}")

    # --- Extract cross sections ---
    x_line = image[y_click, :]  # horizontal pixel values
    y_line = image[:, x_click]  # vertical pixel values

    x_pixels = np.arange(image.shape[1])  #indepent
    y_pixels = np.arange(image.shape[0])

    # --- Fit Gaussians ---
    # Initial guess: A, x0, sigma, offset
    x_guess = [x_line.max(), x_click, 5, np.median(x_line)] #the initial guess for sigma is 5? 
    y_guess = [y_line.max(), y_click, 5, np.median(y_line)]

    popt_x, _ = curve_fit(gaussian, x_pixels, x_line, p0=x_guess)
    popt_y, _ = curve_fit(gaussian, y_pixels, y_line, p0=y_guess)

    # --- Plot results ---
    fig, axs = plt.subplots(1, 2, figsize=(12, 5)) #create a plot with one row and 2 columns. 

    # Horizontal line
    axs[0].plot(x_pixels, x_line, 'b', label='Data')
    axs[0].plot(x_pixels, gaussian(x_pixels, *popt_x), 'r--', label='Gaussian fit')
    axs[0].axvline(popt_x[1], color='k', linestyle=':', label='Center')
    axs[0].set_title("Horizontal cross section")
    axs[0].set_xlabel("X pixels")
    axs[0].set_ylabel("Pixel value")
    axs[0].legend()

    # Vertical line
    axs[1].plot(y_pixels, y_line, 'b', label='Data')
    axs[1].plot(y_pixels, gaussian(y_pixels, *popt_y), 'r--', label='Gaussian fit')
    axs[1].axvline(popt_y[1], color='k', linestyle=':', label='Center')
    axs[1].set_title("Vertical cross section")
    axs[1].set_xlabel("Y pixels")
    axs[1].set_ylabel("Pixel value")
    axs[1].legend()

    plt.tight_layout()
    plt.show()

    print(f"Horizontal fit center: {popt_x[1]:.2f}, sigma: {popt_x[2]:.2f}")
    print(f"Vertical fit center: {popt_y[1]:.2f}, sigma: {popt_y[2]:.2f}")
    sigmax = popt_x[2]
    sigmay = popt_y[2]
    
    return sigmax, sigmay

def fit_2d_gauss_sigma(image_path):
    def twoD_gaussian(coords, A, x0, y0, sigma_x, sigma_y, theta, offset):
        (x, y) = coords
        xo = x0
        yo = y0
        a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
        b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
        c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
        g = offset + A*np.exp(-(a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) + c*((y-yo)**2)))
        return g.ravel()


    # --- Load image ---
    # image_path = "image_174018.tif"  # <-- change to your file name
    image = imread(image_path)

    print(f"Image shape: {image.shape}, dtype: {image.dtype}, max: {np.max(image)}")

    # Step 1: Smooth
    smoothed = gaussian_filter(image, sigma=3)

    # Step 2: Rough center (pixel)
    y0, x0 = np.unravel_index(np.argmax(smoothed), smoothed.shape)

    # Step 3: Refine with center of mass in a local window
    window = image[y0-10:y0+10, x0-10:x0+10]
    dy, dx = center_of_mass(window)
    y0_refined = int(np.floor(y0 - 10 + dy))
    x0_refined = int(np.floor(x0 - 10 + dx))

    print(x0_refined,y0_refined)
    # --- Extract small sub-image around click for fitting ---
    half_size = 100   # size of ROI box around click
    x_min = max(0, x0_refined - half_size)
    x_max = min(image.shape[1], x0_refined + half_size)
    y_min = max(0, y0_refined- half_size)
    y_max = min(image.shape[0], y0_refined + half_size)
    sub_img = image[y_min:y_max, x_min:x_max]


    # coordinate grids
    y_indices, x_indices = np.indices(sub_img.shape)
    x_indices = x_indices + x_min
    y_indices = y_indices + y_min

    #Define array for the contour image plotting
    y_index, x_index = np.indices(sub_img.shape)

    # --- Initial guess ---
    A0 = sub_img.max() - np.median(sub_img)
    x0 = x0_refined #replaced the click input with a intial guess by searching for the maximum. 
    y0 = y0_refined
    sigma_x0 = sigma_y0 = 5
    theta0 = 0
    offset0 = np.median(sub_img)
    initial_guess = (A0, x0, y0, sigma_x0, sigma_y0, theta0, offset0)

    tinitial = time.time()
    # --- Fit ---
    popt, pcov = curve_fit(twoD_gaussian,
                        (x_indices, y_indices),
                        sub_img.ravel(),
                        p0=initial_guess)

    A, x0, y0, sigma_x, sigma_y, theta, offset = popt
    mod_theta = np.mod(theta, 2*np.pi)
    print("\n--- Fit results ---")
    print(f"Center: ({x0:.2f}, {y0:.2f})")
    print(f"Sigma_x: {sigma_x:.2f}, Sigma_y: {sigma_y:.2f}")
    print(f"Angle (rad): {mod_theta:.3f}, Angle (deg): {np.degrees(mod_theta):.2f}")
    print(f"Amplitude: {A:.1f}, Offset: {offset:.1f}")

    print(time.time()-tinitial)
    # --- Plot data and fit ---
    fit_img = twoD_gaussian((x_indices, y_indices), *popt).reshape(sub_img.shape)

    fig, axs = plt.subplots(1, 3, figsize=(15,5))
    axs[0].imshow(sub_img, cmap="jet", origin="lower")
    axs[0].contour(x_index,y_index,fit_img, levels=2, cmap = 'YlOrRd') #how do I change the contour's to be plotted on the 1 sigma and 2 sigma of the fit? 
    axs[0].set_title("Data (cropped)")
    axs[1].imshow(fit_img, cmap="jet", origin="lower")
    axs[1].set_title("2D Gaussian Fit")
    axs[2].imshow(sub_img - fit_img, cmap="bwr", origin="lower")
    axs[2].set_title("Residuals")
    plt.tight_layout()
    plt.show()