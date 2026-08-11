import cv2
import numpy as np

def unwarp_pipe_surface(image_path, pipe_radius_mm, f_px, roi_x_range):
    """
    Unwarps a curved pipe surface from an image and computes the real-world 
    surface area corresponding to a region of interest (ROI).
    """
    img = cv2.imread("/Users/ryanmondong/Downloads/IMG_2667.JPG")
    h, w = img.shape[:2]
    
    # Define pixel range for the pipe width (horizontal limits of the visible cylinder)
    x_min, x_max = roi_x_range
    unwrapped_width = int(pipe_radius_mm * np.pi * (x_max - x_min) / (2 * pipe_radius_mm))
    unwrapped_height = h
    
    # Create coordinate grids for the target unwrapped flat view
    u_out, v_out = np.meshgrid(np.arange(unwrapped_width), np.arange(unwrapped_height))
    
    # Map unwrapped horizontal coordinate back to angle theta, then to original X-pixel
    theta = (u_out / unwrapped_width) * np.pi - (np.pi / 2)
    u_orig = pipe_radius_mm * np.sin(theta) # simplified orthographic/pinhole mapping model
    
    # Center mapping relative to region
    u_mapped = (u_orig / (pipe_radius_mm)) * (x_max - x_min) / 2 + (x_min + x_max) / 2
    v_mapped = v_out.astype(np.float32)
    
    # Remap image to cylindrical flat projection
    unwrapped_img = cv2.remap(img, u_mapped.astype(np.float32), v_mapped, 
                              interpolation=cv2.INTER_BILINEAR, borderMode=cv2.BORDER_CONSTANT)
    
    # Real-world scale calculation (mm per pixel at the given radius)
    mm_per_pixel_x = (np.pi * pipe_radius_mm) / unwrapped_width
    mm_per_pixel_y = pipe_radius_mm / f_px  # approximate vertical scale factor
    pixel_surface_area_mm2 = mm_per_pixel_x * mm_per_pixel_y
    
    return unwrapped_img, pixel_surface_area_mm2

# Example Usage:
# unwrapped, scale_factor = unwarp_pipe_surface('pipe.jpg', pipe_radius_mm=82.5, f_px=1000, roi_x_range=(200, 800))
# measured_pixel_count = 5400  # number of defect/object pixels in unwrapped view
# total_area_mm2 = measured_pixel_count * scale_factor