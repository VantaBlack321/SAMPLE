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

# Get image dimensions
height, width, channels = img.shape
print(f"Loaded image size: {width}x{height}")

def click_event(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"\nClicked Pixel Coordinates: (u={x}, v={y})")

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

u = 1219
v = 1342

fx = 3272.5
fy = 3389.7

cx = 1508
cy = 2349

xn = (u - cx) / fx
yn = (v - cx) / fy

K = np.array([fx, 0, cx],
             [0, fy, cy],
             [0, 0, 0])

cv2.imshow("Targeted Point", img)
cv2.setMouseCallback("Targeted Point", click_event)

cv2.imshow("Patches", img)
cv2.waitKey(0)
cv2.destroyAllWindows()



