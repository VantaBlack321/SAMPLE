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
])

def mouse_click_callback(event, u, v, flags, param):
    """Callback function triggered on mouse events."""
    # Check if the left mouse button was pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        # Append the new (x, y) tuple to our list
        # one clicked coordinate
        clicked_coordinates.append((u, v))
        
        # Display coordinate in console
        print(f"Stored Point {len(clicked_coordinates)}: U={u}, V={v}")
        
        # Draw a visual anchor (a small solid red circle) on the image
        cv2.circle(img=display_img, center=(u, v), radius=5, color=(0, 0, 255), thickness=-1)

        # One homogeneous coordinate 
        p = np.array([
            [u],
            [v],
            [1]
        ])

        # 3D viewing direction corresponding to that pixel 
        d = np.linalg.solve(K, p)

        # collection of all homogeneous coordinates 
        homogeneous_coordinates.append(p)

        # collection of all 3D viewing directions 
        viewing_directions.append(d)

        # P(t) = O + d
        O = (0,0,0)
        # t = 

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(
            display_img,
            f"{u},{v}",
            (u + 5, v - 5),
            font,
            3.0,
            (255, 0, 0),
            1
        )
        
        # Update the displayed window with the modified image
        cv2.imshow("Image Window", display_img)

# Load your image (replace with your file path)
# Learn more on the official OpenCV page or community guides like GeeksforGeeks
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

    # Print total coordinates collected
    print(f"\nSession finished. Total coordinates captured: {len(clicked_coordinates)}")
    print("Coordinates List:", clicked_coordinates)

    print("\nHomogeneous Coordinates:")

    for i, p in enumerate(homogeneous_coordinates, start=1):
        print(f"\nPoint {i}:")
        print(f"[[{p[0, 0]}]\n [{p[1, 0]}]\n [{p[2, 0]}]]")

    print("\n Viewing 3D Directions:")
    for i, d in enumerate(viewing_directions, start=1):
        print(f"\nPoint {i}:")
        print(f"[[{d[0, 0]}]\n [{d[1, 0]}]\n [{d[2, 0]}]]")






