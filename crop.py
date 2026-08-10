import cv2
import numpy as np

# cropped_img = img[y_start:y_end, x_start:x_end]
 
# Load the image
img = cv2.imread("/Users/ryanmondong/Downloads/IMG_2667.JPG")
 
# Define the region of interest (ROI) - arbitrary coordinates
x_start, y_start, x_end, y_end = 400, 200, 850, 700  # Adjust as needed
 
# Crop the image using slicing
cropped_img = img[y_start:y_end, x_start:x_end]
 
# Show the original and cropped images
cv2.imshow("Original Image", img)
cv2.imshow("Cropped Image", cropped_img)
cv2.waitKey(0)
cv2.destroyAllWindows()