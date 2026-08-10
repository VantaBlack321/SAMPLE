import cv2
import numpy as np

# ==========================================
# 1. LOAD IMAGE
# ==========================================
# Replace 'your_image.jpg' with the path to your image file
image_path = '/Users/ryanmondong/Downloads/IMG_2667.JPG'
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(f"Could not load image from path: {image_path}")

# Get image dimensions
height, width, channels = image.shape
print(f"Loaded image size: {width}x{height}")

# ==========================================
# 2. DEFINE CAMERA INTRINSICS & DEPTH
# ==========================================
# If you don't have accurate calibration data, approximate using the image dimensions.
# Ideally, obtain these via cv2.calibrateCamera().
focal_length_x = width * 0.8  # fx
focal_length_y = width * 0.8  # fy
principal_point_x = width / 2.0  # cx
principal_point_y = height / 2.0  # cy

# Define the target 2D pixel coordinate (u, v)
pixel_u = 400  # Horizontal pixel coordinate
pixel_v = 300  # Vertical pixel coordinate

# Define the depth/distance (Z) of the target object from the camera lens
# (Must be known or estimated, e.g., via depth sensors or assumptions like Z=1)
depth_Z = 2.5  # distance in meters

# ==========================================
# 3. 2D TO 3D COORDINATE CONVERSION
# ==========================================
# Formula derived from inversion of the pinhole camera equation:
# X = (u - cx) * Z / fx
# Y = (v - cy) * Z / fy
camera_X = (pixel_u - principal_point_x) * depth_Z / focal_length_x
camera_Y = (pixel_v - principal_point_y) * depth_Z / focal_length_y

print(f"\n--- Conversion Results ---")
print(f"2D Pixel Input: (u={pixel_u}, v={pixel_v}) at Depth Z={depth_Z}m")
print(
    f"3D Camera Coordinates: (X={camera_X:.4f}m, Y={camera_Y:.4f}m, Z={depth_Z:.4f}m)"
)

# Optional: Draw a circle over the targeted 2D point and display the image
cv2.circle(image, (pixel_u, pixel_v), 7, (0, 0, 255), -1)
cv2.imshow("Targeted Point", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
