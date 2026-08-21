import cv2
import numpy as np

# 2. Dimensions and physical constants
img_width = 3024
img_height = 4032
radius = 4.25       # cm
pipe_length = 43.3  # cm

fx = 3272.5
fy = 3389.7

cx = 1508
cy = 2349

# Get image dimensions
print(f"Loaded image size: {img_width}x{img_height}")

# Initialize an empty list to store unlimited coordinates
clicked_coordinates = []

def mouse_click_callback(event, u, v, flags, param):
    """Callback function triggered on mouse events."""
    # Check if the left mouse button was pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        # Append the new (x, y) tuple to our list
        clicked_coordinates.append((u, v))
        
        # Display coordinate in console
        print(f"Stored Point {len(clicked_coordinates)}: U={u}, V={v}")
        
        # Draw a visual anchor (a small solid red circle) on the image
        cv2.circle(img=display_img, center=(u, v), radius=5, color=(0, 0, 255), thickness=-1)

        p = np.array([
            [u],
            [v],
            [1]
        ])

        K = np.array([
            [fx, 0, cx],
            [0, fy, cy],
            [0, 0, 1]
        ])

        d = np.linalg.solve(K, p)

        for u, v in clicked_coordinates:
            p.append(([u], [v], [1]))

        print(p)

        # font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(
        #     display_img,
        #     f"{u},{v}",
        #     (u + 5, v - 5),
        #     font,
        #     3.0,
        #     (255, 0, 0),
        #     1
        # )
        
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
    print(p)






