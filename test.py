import cv2
import numpy as np

image = np.zeros((500, 500, 3), dtype=np.uint8)

cv2.rectangle(image, (50, 50), (200, 150), (0, 255, 0), thickness=2)

cv2.circle(image, (300,100), 30, (0, 0, 225), thickness=-1)

cv2.imshow('OpenCV Example', image)

cv2.waitKey(0)
cv2.destroyAllWindows()

