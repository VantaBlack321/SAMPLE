import numpy as np

def pixel_to_3d(x_photopea, y_photopea, depth=1.0, camera_matrix=None):
    """
    Converts Photopea (x, y) pixel coordinates to OpenCV (X, Y, Z).
    """
    # 1. 2D coordinates are identical in layout (Top-Left origin)
    x_cv = x_photopea
    y_cv = y_photopea
    
    if camera_matrix is None:
        # Simple flat 3D projection where Z is a fixed depth/distance
        X, Y, Z = float(x_cv), float(y_cv), float(depth)
    else:
        # Unproject using camera intrinsics (Pinhole model)
        fx = camera_matrix[0, 0]
        fy = camera_matrix[1, 1]
        cx = camera_matrix[0, 2]
        cy = camera_matrix[1, 2]
        
        X = ((x_cv - cx) / fx) * depth
        Y = ((y_cv - cy) / fy) * depth
        Z = depth
        
    return np.array([X, Y, Z], dtype=np.float32)

# Example usage:
# Pixel from Photopea at x=500, y=300 with a depth of 50mm
point_3d = pixel_to_3d(500, 300, depth=50.0)
print(point_3d)
