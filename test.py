import cv2
import numpy as np

# Load the image from your local directory
image_path = '/Users/ryanmondong/Downloads/IMG_2667.JPG'
img = cv2.imread(image_path)

# Check if image loaded successfully
if img is None:
    print("Error: Could not load image. Check the file path.")
else:
    # Display the image in a window
    cv2.imshow('iPhone Photo', img)
    
    # Wait until a key is pressed, then close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

