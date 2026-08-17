import cv2
import numpy as np

# Load image FIRST
img = cv2.imread('/Users/ryanmondong/Downloads/IMG_2667.JPG')

if img is None:
    raise FileNotFoundError("Could not load image. Check the file path.")

# Get image dimensions
height, width, channels = img.shape
print(f"Loaded image size: {width}x{height}")

# Camera parameters
focal_length_x = 6.3
focal_length_y = 4.6

principal_point_x = width / 2.0
principal_point_y = height / 2.0

depth_Z = 5.0  # meters

# Initial target pixel
pixel_u = 400
pixel_v = 300


def pixel_to_3d(u, v):
    camera_X = (u - principal_point_x) * depth_Z / focal_length_x
    camera_Y = (v - principal_point_y) * depth_Z / focal_length_y

    return camera_X, camera_Y, depth_Z


# Convert initial pixel
camera_X, camera_Y, camera_Z = pixel_to_3d(pixel_u, pixel_v)

print("\n--- Conversion Results ---")
print(
    f"2D Pixel Input: (u={pixel_u}, v={pixel_v}) "
    f"at Depth Z={depth_Z}m"
)
print(
    f"3D Camera Coordinates: "
    f"(X={camera_X:.4f}m, "
    f"Y={camera_Y:.4f}m, "
    f"Z={camera_Z:.4f}m)"
)

def click_event(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"\nClicked Pixel Coordinates: (u={x}, v={y})")

        camera_X, camera_Y, camera_Z = pixel_to_3d(x, y)

        print(
            f"Converted 3D Coordinates: "
            f"(X={camera_X:.4f}m, "
            f"Y={camera_Y:.4f}m, "
            f"Z={camera_Z:.4f}m)"
        )

        # Draw clicked point
        cv2.circle(img, (x, y), 5, (255, 0, 0), -1)

        # Add coordinate text
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(
            img,
            f"{x},{y}",
            (x + 5, y - 5),
            font,
            3.0,
            (255, 0, 0),
            1
        )

        cv2.imshow("Targeted Point", img)

# Draw initial target
cv2.circle(img, (pixel_u, pixel_v), 7, (0, 0, 255), -1)

cv2.imshow("Targeted Point", img)
cv2.setMouseCallback("Targeted Point", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()