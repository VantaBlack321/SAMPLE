import cv2
import numpy as np

class CylinderPoseEstimator:
    def __init__(self):
        # 1. Physical Dimensions and Calibration Constants
        self.img_width = 3024
        self.img_height = 4032
        self.radius = 4.25       # cm
        self.pipe_length = 43.3  # cm

        # Camera Intrinsic Properties
        self.fx, self.fy = 3272.5, 3389.7
        self.cx, self.cy = 1508.0, 2349.0

        # Build Camera Matrix K and assume zero distortion
        self.K = np.array([
            [self.fx, 0.0,     self.cx],
            [0.0,     self.fy, self.cy],
            [0.0,     0.0,     1.0]
        ], dtype=np.float32)
        self.dist_coeffs = np.zeros((4, 1), dtype=np.float32)

        # 2. Data Containers
        self.clicked_coordinates = []
        self.homogeneous_coordinates = []
        self.viewing_directions = []
        
        # Image buffer targets
        self.image_path = '/Users/ryanmondong/Downloads/IMG_2667.JPG'
        self.display_img = None

    def mouse_click_callback(self, event, u, v, flags, param):
        """Monitors mouse events and captures spatial coordinates."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.clicked_coordinates.append((u, v))
            print(f"Stored Point {len(self.clicked_coordinates)}: U={u}, V={v}")
            
            # Render a visual anchor node
            cv2.circle(img=self.display_img, center=(u, v), radius=5, color=(0, 0, 255), thickness=-1)

            # Map Homogeneous 2D coordinate array
            p = np.array([[u], [v], [1.0]], dtype=np.float32)
            self.homogeneous_coordinates.append(p)

            # Compute raw 3D projection viewing vector line
            d = np.linalg.solve(self.K, p)
            self.viewing_directions.append(d)

            # Annotate coordinate feedback directly over image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(self.display_img, f"{u},{v}", (u + 5, v - 5), font, 3.0, (255, 0, 0), 2)
            cv2.imshow("Image Window", self.display_img)

    def calculate_cylinder_axis(self):
        """Uses OpenCV PnP solver optimization to derive the 3D axis vector."""
        if len(self.clicked_coordinates) != 4:
            print(f"\nEstimation aborted: Requires exactly 4 targeted clicks (Received: {len(self.clicked_coordinates)}).")
            return

        print(f"\nProcessing execution window logic using true focal length profiles...")
        image_points = np.array(self.clicked_coordinates, dtype=np.float32)

        # Map exact physical boundaries relative to the target's geometric origin center
        object_points = np.array([
            [0.0,  self.radius,  0.0],               # Point A: Front Rim Base
            [0.0,  self.radius,  self.pipe_length],    # Point B: Back Depth Base 
            [0.0, -self.radius,  0.0],               # Point C: Front Rim Ceiling
            [0.0, -self.radius,  self.pipe_length]     # Point D: Back Depth Ceiling
        ], dtype=np.float32)

        # Parse geometric translation and rotation vector components
        success, rvec, tvec = cv2.solvePnP(
            object_points, image_points, self.K, self.dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
        )

        if success:
            rotation_matrix, _ = cv2.Rodrigues(rvec)
            # Extrapolate longitudinal Z-vector relative to system camera axis space
            cylinder_axis_vector = rotation_matrix[:, 2]

            print("\n" + "="*35 + "\n=== 3D SPATIAL ESTIMATION RESULTS ===\n" + "="*35)
            print(f"Translation Vector (X, Y, Z coordinates in cm from lens):\n{tvec.flatten()}")
            print(f"\nCylinder 3D Axis Direction Profile:\n{cylinder_axis_vector}")
            
            # Compute angular variance offset vs optical alignment standard center line [0, 0, 1]
            tilt_rad = np.arccos(np.dot(cylinder_axis_vector, np.array([0.0, 0.0, 1.0], dtype=np.float32)))
            tilt_deg = np.degrees(tilt_rad)
            print(f"\nCalculated Tilt Offset from Lens Horizon: {tilt_deg:.2f}° degrees")
        else:
            print("\nPnP Engine Failed to reach structural convergence. Verify structural coordinates.")

    def run(self):
        """Initializes application capture routine."""
        original_img = cv2.imread(self.image_path)
        if original_img is None:
            print(f"IO Error: Location invalid or image structural data unreadable at {self.image_path}")
            return

        self.display_img = original_img.copy()
        print(f"Loaded source image window size successfully: {self.img_width}x{self.img_height}")
        
        cv2.namedWindow("Image Window")
        cv2.setMouseCallback("Image Window", self.mouse_click_callback)
        cv2.imshow("Image Window", self.display_img)

        print("\nINSTRUCTIONS: Click targets accurately inside image window in order: A -> B -> C -> D")
        print("Exit input acquisition window at any point by hitting 'ESC' or 'q'.")

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):
                break

        cv2.destroyAllWindows()
        
        # Trigger spatial axis calculation engine post input window cleanup
        self.calculate_cylinder_axis()

if __name__ == "__main__":
    estimator = CylinderPoseEstimator()
    estimator.run()
