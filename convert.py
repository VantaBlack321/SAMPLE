import numpy as np
from PIL import Image

# Load image and convert to RGB
img = Image.open('/Users/ryanmondong/Downloads/IMG_2667.JPG').convert("RGB")
arr = np.array(img)

# Define target RGB color (e.g., pure red)
target_color = np.array([255, 0, 0])

# Find all coordinates where pixel matches target color
y_indices, x_indices = np.where(np.all(arr == target_color, axis=-1))

# Combine into (x, y) pairs
coordinates = list(zip(x_indices, y_indices))

# Print out the coordinates
for coord in coordinates:
  print(coord)
