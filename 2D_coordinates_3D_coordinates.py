import cv2
import numpy as np

# 1. Load the image
img = cv2.imread("/Users/ryanmondong/Downloads/IMG_2667.JPG")

if img is None:
    raise FileNotFoundError("Could not load image. Check the file path.")

# 2. Dimensions and physical constants
img_width = 3024
image_height = 4032
radius = 4.25       # cm
pipe_length = 43.3  # cm

# 3. Generate pixel grids
u_grid, v_grid = np.meshgrid(np.arange(img_width), np.arange(image_height))

# 4. Map to cylindrical coordinates
theta = (u_grid / img_width) * 2 * np.pi
Z = (v_grid / image_height) * pipe_length

# 5. Map to 3D Cartesian coordinates
X = radius * np.cos(theta)
Y = radius * np.sin(theta)

# 6. Print structural shape and the specific top-left pixel (Fixed syntax)
print("X grid shape:", X.shape)  
print(f"Top-left pixel 3D coordinate: ({X[0,0]:.2f}, {Y[0,0]:.2f}, {Z[0,0]:.2f})")

# 7. Bonus: Combine into a standard 3D Point Cloud array (Shape: 12192768 points, 3 coordinates)
# This flattens the grids so every row is one single point: [X, Y, Z]
point_cloud_3d = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T
print("Flattened 3D points shape:", point_cloud_3d.shape)

# fx = 3272.5
# fy = 3389.7

# cx = 1508
# cy = 2349

# Test_Matrix = np.array([fx, 0, cx],
#                        [0, fy, cy],
#                        [0, 0, 1])


