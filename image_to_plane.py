import cv2
import numpy as np
import open3d as o3d

# Load the image
img = cv2.imread('image.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert to RGB for visualization

h, w, _ = img.shape

# Create a mesh grid of x and y coordinates
x = np.arange(w)
y = np.arange(h)
xx, yy = np.meshgrid(x, y)

# Set Z to 0 for a flat plane (or modify Z using a depth map)
zz = np.zeros_like(xx)

# Reshape coordinates and colors into point cloud data
points = np.stack((xx, -yy, zz), axis=-1).reshape(-1, 3) # Negative y to keep right-side up
colors = img.reshape(-1, 3) / 255.0 # Normalize colors to [0, 1]

# Create Open3D Point Cloud object
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)

# Visualize the 3D plane
o3d.visualization.draw_geometries([pcd])
