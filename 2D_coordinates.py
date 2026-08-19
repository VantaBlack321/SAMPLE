import cv2
import numpy as np

# 1. Load the image
img = cv2.imread('/Users/ryanmondong/Downloads/IMG_2667.JPG')

if img is None:
    raise FileNotFoundError("Could not load image. Check the file path.")

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

cv2.imshow("Targeted Point", img)
cv2.setMouseCallback("Targeted Point", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()