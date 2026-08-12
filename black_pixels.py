import cv2
import numpy as np

# 1. Load the image in grayscale
img = cv2.imread('/Users/ryanmondong/Downloads/IMG_2667.JPG', cv2.IMREAD_GRAYSCALE)

# 2. Find all coordinates where pixel value is black (0)
# Note: np.argwhere returns a list of [y, x] (row, col) indices
black_pixels = np.argwhere(img == 0)

# Optional: If you strictly need (x, y) format instead of (y, x)
# black_pixels_xy = black_pixels[:, [1, 0]]

# 3. Write down/save coordinates to a text file
np.savetxt('black_pixel_coordinates.txt', black_pixels, fmt='%d')

print(f'Total black pixels found: {len(black_pixels)}')
