import cv2
import numpy as np

# Example Photopea 2D coordinates
u = 450  # X-pixel from Photopea
v = 300  # Y-pixel from Photopea

# Assume image width and height
width, height = 1920, 1080

# Approximate Intrinsic Matrix (K)
fx = fy = max(width, height) * 0.9  # Standard approximation field of view
cx, cy = width / 2, height / 2
K = np.array([[fx, 0, cx],
              [0, fy, cy],
              [0,  0,  1]], dtype=np.float32)

# Create the homogeneous 2D pixel vector
pixel_2d = np.array([u, v, 1.0], dtype=np.float32)

# Compute the inverse matrix of K
K_inv = np.linalg.inv(K)

# Get the normalized 3D direction vector (X_norm, Y_norm, 1)
normalized_ray = K_inv.dot(pixel_2d)
print("Normalized 3D Ray:", normalized_ray) 
# Output structure: [X_norm, Y_norm, 1.0]

# Example: Assume the object is known to be exactly 2.5 meters away
Z_actual = 2.5  

X_3d = normalized_ray[0] * Z_actual
Y_3d = normalized_ray[1] * Z_actual
Z_3d = Z_actual

print(f"3D Position in Camera Space: X={X_3d}, Y={Y_3d}, Z={Z_3d}")
