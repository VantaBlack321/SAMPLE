import numpy as np

def compute_pipe_surface_area(pixel_contour, radius_mm, scale_mm_per_pixel):
    """
    Computes the true surface area on a curved pipe from a 2D pixel contour.
    
    Parameters:
    - pixel_contour: Nx2 array of (u, v) pixel coordinates outlining the region.
    - radius_mm: Known radius of the pipe in millimeters.
    - scale_mm_per_pixel: Calibration factor to convert pixels to mm.
    """
    # Convert pixel coordinates to local metric coordinates (y_linear, x_arc)
    contour_mm = pixel_contour * scale_mm_per_pixel
    
    # Extract longitudinal span (Z-axis along the pipe length)
    z_coords = contour_mm[:, 1]
    z_span = np.max(z_coords) - np.min(z_coords)
    
    # Extract transverse span (arc length along the curvature)
    # Arc length = R * theta, so delta_theta = arc_length / R
    arc_lengths = contour_mm[:, 0]
    arc_span = np.max(arc_lengths) - np.min(arc_lengths)
    theta_span = arc_span / radius_mm  # in radians
    
    # Recalculate true curved surface area strip
    true_surface_area = radius_mm * theta_span * z_span
    
    return true_surface_area

# Example usage:
# Dummy contour of 4 points in pixel space
sample_contour = np.array([[100, 50], [150, 50], [150, 200], [100, 200]])
pipe_radius = 75.0          # 75 mm pipe radius
pixel_scale = 0.25          # 0.25 mm per pixel scale factor

area = compute_pipe_surface_area(sample_contour, pipe_radius, pixel_scale)
print(f"True Curved Surface Area: {area:.2f} sq mm")
