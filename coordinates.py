import numpy as np
import cv2

# Define the mouse click callback function
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: X={x}, Y={y}")
        
        # Draw a small circle on the image where clicked
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        
        # Show coordinates text on the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f"{x},{y}", (x + 5, y - 5), font, 0.5, (255, 0, 0), 1)
        cv2.imshow("Image", img)

# Load the image from your folder
img = cv2.imread('/Users/ryanmondong/Downloads/IMG_2667.JPG')

# Check if image loaded correctly
if img is None:
    print("Error: Could not load image. Check file name and path.")
else:
    cv2.imshow("Image", img)
    
    # Set mouse handler for the window
    cv2.setMouseCallback("Image", click_event)
    
    # Wait until any key is pressed to exit
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# def pixel_to_3d_with_depth(u, v, Z, K, dist_coeffs=None):
#     """
#     Converts 2D pixel coordinates to 3D camera coordinates using a known depth Z.
#     """
#     # 1. Undistort the pixel point if distortion coefficients are provided
#     if dist_coeffs is not None:
#         # cv2.undistortPoints expects shape (N, 1, 2)
#         pixel_pt = np.array([[[u, v]]], dtype=np.float32)
#         undistorted_pt = cv2.undistortPoints(pixel_pt, K, dist_coeffs, P=K)
#         u, v = undistorted_pt[0][0]
    
#     # 2. Extract intrinsic parameters from matrix K
#     fx = K[0, 0]
#     fy = K[1, 1]
#     cx = K[0, 2]
#     cy = K[1, 2]
    
#     # 3. Calculate 3D coordinates in the camera reference frame
#     X = (u - cx) * Z / fx
#     Y = (v - cy) * Z / fy
    
#     return np.array([X, Y, Z])

# # --- Example Usage ---
# # Dummy Intrinsic Matrix (K) from camera calibration
# K = np.array([[800,   0, 320],
#               [  0, 800, 240],
#               [  0,   0,   1]], dtype=np.float32)

# # Assuming no lens distortion for simplicity
# dist_coeffs = np.zeros(5) 

# # Pixel coordinate (u, v) and known depth Z = 2.5 meters
# pixel_u, pixel_v = 400, 300
# depth_z = 2.5 

# point_3d = pixel_to_3d_with_depth(pixel_u, pixel_v, depth_z, K, dist_coeffs)
# print(f"3D Point (Camera Frame): {point_3d}")

