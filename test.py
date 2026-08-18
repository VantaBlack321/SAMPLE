import cv2
import numpy as np

# Global variables for mouse callback
clicked_points_3d = []
camera_matrix = None
distortion_coeffs = None
pipe_radius = 0.0
R_cam_to_pipe = None
T_cam_to_pipe = None

def init_camera_and_pipe():
    """Initializes dummy calibration data and pipe geometry.
    Replace these with your actual calibration metrics.
    """
    global camera_matrix, distortion_coeffs, pipe_radius, R_cam_to_pipe, T_cam_to_pipe
    
    # Camera Intrinsic Matrix (from calibration)
    camera_matrix = np.array([[800.0,   0.0, 320.0],
                              [  0.0, 800.0, 240.0],
                              [  0.0,   0.0,   1.0]], dtype=np.float32)
    
    # Distortion coefficients
    distortion_coeffs = np.zeros((5, 1), dtype=np.float32)
    
    # Pipe configuration (in meters)
    pipe_radius = 0.15  # 15 cm radius
    
    # Extrinsic alignment: Pipe axis aligns with Z-axis, shifted 1 meter away in Y
    R_cam_to_pipe = np.eye(3, dtype=np.float32)
    T_cam_to_pipe = np.array([0.0, 1.0, 0.0], dtype=np.float32)

def pixel_to_ray(pixel_x, pixel_y):
    """Undistorts the pixel point and converts it to a 3D unit ray directional vector."""
    # Undistort point to account for lens curvature
    pts_distorted = np.array([[[pixel_x, pixel_y]]], dtype=np.float32)
    pts_undistorted = cv2.undistortPoints(pts_distorted, camera_matrix, distortion_coeffs)
    
    # Normalized coordinates
    u_norm = pts_undistorted[0][0][0]
    v_norm = pts_undistorted[0][0][1]
    
    # Ray vector in camera coordinate system
    ray_cam = np.array([u_norm, v_norm, 1.0], dtype=np.float32)
    return ray_cam / np.linalg.norm(ray_cam)

def ray_cylinder_intersection(ray_cam):
    """Calculates intersection of the camera ray with the curved cylinder surface."""
    # Transform ray origin (camera is at 0,0,0) and direction to Pipe Space
    # P_pipe = R * P_cam + T
    ray_origin_pipe = T_cam_to_pipe
    ray_dir_pipe = R_cam_to_pipe @ ray_cam
    
    # Assuming infinite cylinder along the Z-axis: X^2 + Y^2 = R^2
    # Quadratic equation setup: a*t^2 + b*t + c = 0
    a = ray_dir_pipe[0]**2 + ray_dir_pipe[1]**2
    b = 2 * (ray_origin_pipe[0] * ray_dir_pipe[0] + ray_origin_pipe[1] * ray_dir_pipe[1])
    c = ray_origin_pipe[0]**2 + ray_origin_pipe[1]**2 - (pipe_radius ** 2)
    
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None  # Ray missed the pipe
        
    # Get closest intersection distance (t)
    t1 = (-b - np.sqrt(discriminant)) / (2 * a)
    t2 = (-b + np.sqrt(discriminant)) / (2 * a)
    t = min(t1, t2) if min(t1, t2) > 0 else max(t1, t2)
    
    if t < 0:
        return None  # Pipe is behind camera
        
    # Compute 3D point in Pipe Space
    point_3d_pipe = ray_origin_pipe + t * ray_dir_pipe
    return point_3d_pipe

def click_event(event, x, y, flags, param):
    """Mouse callback function to handle image clicks."""
    if event == cv2.EVENT_LBUTTONDOWN:
        ray = pixel_to_ray(x, y)
        point_3d = ray_cylinder_intersection(ray)
        
        if point_3d is not None:
            clicked_points_3d.append(point_3d)
            print(f"Clicked Pixel: ({x}, {y}) -> 3D Pipe Coords: X={point_3d[0]:.4f}, Y={point_3d[1]:.4f}, Z={point_3d[2]:.4f}")
        else:
            print(f"Clicked Pixel: ({x}, {y}) -> Out of pipe bounds!")

# --- Main Execution ---
if __name__ == "__main__":
    init_camera_and_pipe()
    
    # Create blank canvas representing image window
    # img = np.zeros((480, 640, 3), dtype=np.uint8) + 50
    img = cv2.imread("/Users/ryanmondong/Downloads/IMG_2667.JPG")

    # cv2.putText(img, "Click on the surface to output 3D coordinates", (30, 240), 
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cv2.imshow("Pipe Measurement Window", img)
    cv2.setMouseCallback("Pipe Measurement Window", click_event)
    
    print("Click inside the window. Press 'q' to exit.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()
    print(f"\nCaptured {len(clicked_points_3d)} total 3D surface points.")
