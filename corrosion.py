import cv2
import numpy as np

# 1. Load image and convert to grayscale
image = cv2.imread('/Users/ryanmondong/Downloads/IMG_2667.JPG')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 2. Define a polygonal or free-form ROI mask for the target feature on the pipe
# (e.g., a corrosion patch hand-drawn or detected via thresholding)
mask = np.zeros_like(gray)
pts = np.array([[150, 200], [250, 190], [260, 310], [140, 320]], dtype=np.int32)
cv2.fillPoly(mask, [pts], 255)

# 3. Extract the feature pixels inside the ROI mask
masked_image = cv2.bitwise_and(gray, gray, mask=mask)
_, thresh = cv2.threshold(masked_image, 100, 255, cv2.THRESH_BINARY)

# 4. Find contours and compute pixel area
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if contours:
    target_contour = max(contours, key=cv2.contourArea)
    pixel_area = cv2.contourArea(target_contour)
    
    # 5. Correct for surface curvature (Cylindrical compensation)
    # Estimate pipe center X-coordinate and radius R in pixels
    pipe_center_x = 300  
    pipe_radius_px = 120 
    
    # Get centroid of the target feature to evaluate radial angle (theta)
    M = cv2.moments(target_contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        # Normalized distance from center (-1 to 1)
        dx = (cx - pipe_center_x) / pipe_radius_px
        dx = np.clip(dx, -1.0, 1.0)
        
        # Surface angle adjustment factor (1 / cos(theta))
        # Account for apparent compression of area near the curved edges
        correction_factor = 1.0 / np.cos(np.arcsin(dx))
    else:
        correction_factor = 1.0

    # 6. Convert to real-world units (e.g., mm^2 per pixel scale)
    scale_mm_per_pixel = 0.05  # Calibrated physical size factor
    real_surface_area = pixel_area * (scale_mm_per_pixel ** 2) * correction_factor
    
    print(f"Corrected Surface Area: {real_surface_area:.2f} mm²")

### Key Steps in the Process
### Mask Generation:** Define the bounding coordinates or polygon tracking the defect area.
### Contour Extraction:** Use `cv2.findContours` and `cv2.contourArea` to count the precise number of pixels within the feature boundaries.
### Curvature Compensation:** Apply a trigonometric inverse-cosine adjustment ($1/\cos\theta$) corresponding to the horizontal shift from the cylinder's central meridian to offset the perspective shrinking of the curved pipe edges.
