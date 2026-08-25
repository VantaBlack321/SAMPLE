import cv2
import numpy as np

# 2. Dimensions and physical constants
img_width = 3024
img_height = 4032
radius = 4.25       # cm
pipe_length = 43.3  # cm

# focal length width
fx = 3272.5
# focal length height
fy = 3389.7

# Central coordiantes x axis
cx = 1508
# Central coordiantes y axis
cy = 2349

# Get image dimensions
print(f"Loaded image size: {img_width}x{img_height}")

# collection of all clicked coordinates
clicked_coordinates = []
# collection of all homogeneous coordinates 
homogeneous_coordinates = []
# collection of all 3D viewing directions 
viewing_directions = []

# Camera Matrix 
K = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
], dtype=np.float32)

# Assume zero lens distortion for an uncalibrated matrix frame
dist_coeffs = np.zeros((4, 1), dtype=np.float32)

def mouse_click_callback(event, u, v, flags, param):
    """Callback function triggered on mouse events."""
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_coordinates.append((u, v))
        print(f"Stored Point {len(clicked_coordinates)}: U={u}, V={v}")
        
        cv2.circle(img=display_img, center=(u, v), radius=5, color=(0, 0, 255), thickness=-1)

        p = np.array([[u], [v], [1]])
        d = np.linalg.solve(K, p)

        homogeneous_coordinates.append(p)
        viewing_directions.append(d)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(display_img, f"{u},{v}", (u + 5, v - 5), font, 3.0, (255, 0, 0), 2)
        cv2.imshow("Image Window", display_img)

# Load your image
image_path = '/Users/ryanmondong/Downloads/IMG_2667.JPG'
original_img = cv2.imread(image_path)

if original_img is None:
    print("Error: Could not load image. Check the file path.")
else:
    display_img = original_img.copy()
    cv2.namedWindow("Image Window")
    cv2.setMouseCallback("Image Window", mouse_click_callback)
    cv2.imshow("Image Window", display_img)

    print("Click exactly 4 points in this specific order: A, B, C, D. Press 'ESC' or 'q' to exit.")
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cv2.destroyAllWindows()

    print(f"\nSession finished. Total coordinates captured: {len(clicked_coordinates)}")

    # -------------------------------------------------------------------------
    # 3D CYLINDER AXIS CALCULATION BLOCK
    # -------------------------------------------------------------------------
    if len(clicked_coordinates) == 4:
        # Convert clicked 2D coordinates into a numpy array for OpenCV PnP
        image_points = np.array(clicked_coordinates, dtype=np.float32)

        # Map 3D object points based on your cylinder physical properties (radius=4.25, length=43.3)
        # Let center axis be X=0, Y=0. Z extends into depth.
        # Format: [X, Y, Z]
        # Adjust depth values (Z) for B and D based on where your inside markings are!
        object_points = np.array([
            [0.0,  radius,  0.0],          # Point A: Outer bottom rim (Z = 0)
            [0.0,  radius,  pipe_length],  # Point B: Inner bottom edge/marker (Z = depth)
            [0.0, -radius,  0.0],          # Point C: Outer top rim (Z = 0)
            [0.0, -radius,  pipe_length]   # Point D: Inner top edge/marker (Z = depth)
        ], dtype=np.float32)

        # Run PnP solver using your true K matrix
        success, rvec, tvec = cv2.solvePnP(
            object_points, image_points, K, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
        )

        if success:
            # Convert rotation vector to 3x3 matrix
            rotation_matrix, _ = cv2.Rodrigues(rvec)
            
            # The 3rd column is the 3D unit direction vector of the cylinder's longitudinal axis
            cylinder_axis_vector = rotation_matrix[:, 2]

            print("\n=== AXIS EXTRACTION RESULTS ===")
            print(f"Cylinder Location (X, Y, Z in cm relative to camera focal point):\n{tvec.flatten()}")
            print(f"Cylinder Axis 3D Direction Vector:\n{cylinder_axis_vector}")
            
            # Compute tilt relative to camera's forward optical axis [0, 0, 1]
            tilt_rad = np.arccos(np.dot(cylinder_axis_vector, np.array([0, 0, 1])))
            tilt_deg = np.degrees(tilt_rad)
            print(f"Cylinder Axis Tilt Angle: {tilt_deg:.2f} degrees away from camera center.")
        else:
            print("\nPnP optimization failed. Make sure your 3D points line up logically with 2D clicks.")
    else:
        print(f"\nSkipped axis estimation: You must select exactly 4 points (Got {len(clicked_coordinates)}).")
