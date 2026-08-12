import cv2
import numpy as np


def unwarp_pipe_surface(image_path, r, xc):
    """Unwarps a 2D image of a cylindrical pipe into a flat 2D plane.

    Parameters:
    image_path (str): Path to the input image.
    r (float): Radius of the pipe in pixels.
    xc (float): The X-coordinate of the pipe's center axis in pixels.
    """
    # Load the image
    img = cv2.imread("/Users/ryanmondong/Downloads/IMG_2667.JPG")
    if img is None:
        raise FileNotFoundError("Input image not found.")

    h, w, c = img.shape

    # Calculate the width of the flattened surface (arc length)
    # Full semi-cylinder width = pi * r
    flat_w = int(np.pi * r)

    # Initialize the blank flattened image
    flat_img = np.zeros((h, flat_w, c), dtype=np.uint8)

    # Generate coordinate maps for remapping
    # map_x and map_y will store the source coordinates for each target pixel
    map_x = np.zeros((h, flat_w), dtype=np.float32)
    map_y = np.zeros((h, flat_w), dtype=np.float32)

    for y in range(h):
        for x_flat in range(flat_w):
            # Calculate the angle theta based on the flattened position
            theta = x_flat / r

            # Map back to the original 2D distorted image coordinates
            x_orig = xc + r * np.sin(theta - (np.pi / 2))
            y_orig = y

            # Store coordinates in maps
            map_x[y, x_flat] = x_orig
            map_y[y, x_flat] = y_orig

    # Remap the original image to the flat plane using linear interpolation
    flat_img = cv2.remap(
        img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT
    )

    return flat_img


# --- Execution Example ---
if __name__ == "__main__":
    # Example parameters (adjust these to match your specific image scale)
    PIPE_RADIUS_PX = 300  # Pipe radius in pixels
    CENTER_AXIS_X = 300  # X-coordinate where the pipe center sits

    # Run the unwarping function
    try:
        flattened_surface = unwarp_pipe_surface(
            "pipe_surface.jpg", PIPE_RADIUS_PX, CENTER_AXIS_X
        )

        # Save the result
        cv2.imwrite("flattened_pipe_surface.jpg", flattened_surface)
        print("Success: Image flattened and saved.")

    except Exception as e:
        print(f"Error: {e}")
