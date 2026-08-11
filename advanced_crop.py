import cv2
import os
 
# Load the image
img = cv2.imread("/Users/ryanmondong/Downloads/IMG_2667.JPG")
img_h, img_w, _ = img.shape  # Get image dimensions
 
# Patch size
patch_w, patch_h = 200, 200  # Adjust as needed
 
# Create output directory if it doesn't exist
output_dir = "/Users/ryanmondong/Downloads/patches"
os.makedirs(output_dir, exist_ok=True)
 
# Counter for patch numbering
patch_id = 0
 
# Loop through the image with step size = patch size
for y in range(0, img_h, patch_h):
    for x in range(0, img_w, patch_w):
 
        # Ensure patch does not exceed image boundaries
        x_end = min(x + patch_w, img_w)
        y_end = min(y + patch_h, img_h)
 
        # Crop the patch
        patch = img[y:y_end, x:x_end]
 
        # Save the patch
        patch_filename = f"{output_dir}/patch_{patch_id}.png"
        cv2.imwrite(patch_filename, patch)
 
        # Draw a rectangle on the original image (visualization)
        cv2.rectangle(img, (x, y), (x_end, y_end), (0, 255, 0), 2)
        patch_id += 1
 
# Show the original image with drawn patches
cv2.imshow("Patches", img)
cv2.waitKey(0)
cv2.destroyAllWindows()