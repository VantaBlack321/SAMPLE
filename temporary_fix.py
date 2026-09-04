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

# Central coordinates x axis
cx = 1508
# Central coordinates y axis
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
])

labels = ['P', 'Q', 'R', 'S']

def mouse_click_callback(event, u, v, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_coordinates) < 4:
        idx = len(clicked_coordinates)
        letter = labels[idx]
        
        # Store the point
        clicked_coordinates.append((u, v))
        
        # Draw a clean high-contrast dot
        cv2.circle(display_img, (u, v), 5, (0, 0, 255), -1)  # Red dot
        
        # Render clear label with vertex letter and coordinates
        text = f"{letter}: ({u}, {v})"
        cv2.putText(display_img, text, (u + 10, v - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA) # Yellow text with thickness 2

        cv2.imshow("Image Window", display_img)
        
image_path = '/Users/ryanmondong/Downloads/IMG_2667.JPG'
original_img = cv2.imread(image_path)

if original_img is None:
    print("Error: Could not load image. Check the file path.")
else:
    # Create a copy so we don't permanently alter the source data
    display_img = original_img.copy()

    # Create a named window (essential for binding the callback)
    cv2.namedWindow("Image Window")

    # Bind our custom callback function to the window
    cv2.setMouseCallback("Image Window", mouse_click_callback)

    # Initial image display
    cv2.imshow("Image Window", display_img)

    print("Click on the image to store coordinates. Press 'ESC' or 'q' to exit.")
    
    # Keep the window open until a termination key is pressed
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):  # 27 is the ASCII code for ESC
            break

    # Clean up and close all GUI windows safely
    cv2.destroyAllWindows()