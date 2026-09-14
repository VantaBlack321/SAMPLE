import cv2
import math
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

# Labels to assign sequentially
labels = ['P', 'Q', 'R', 'S']

# Collections
clicked_coordinates = []
homogeneous_coordinates = []
viewing_directions = []
d_hat = []

# Dictionary to look up specific points by letter: P, Q, R, S
points_dict = {}

# Camera Matrix
K = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
])

# Camera Ray
# P(t) = C + td

C = np.array([
    [0],
    [0],
    [0]
])

# Temporary estimated point on cylinder axis
# Real C_cyl goal:
# C_cyl = one 3D point on the cylinder's central axis
# Coordinates are measured relative to the camera center C = (0,0,0)
# Units should be cm
# Must be estimated from known pipe geometry / reference points,
# not guessed from the image
C_cyl = np.array([
    [0],
    [0],
    [10]
])

# Cylinder Surface Equation
# x(t) = t * d_hat
# y = t * d_hat

def mouse_click_callback(event, u, v, flags, param):
    """Callback function triggered on mouse events."""
    # Only capture up to 4 points (P, Q, R, S)
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_coordinates) < len(labels):
        idx = len(clicked_coordinates)
        letter = labels[idx]

        # 1. Store pixel coordinate
        clicked_coordinates.append((u, v))
        print(f"Stored Point {letter} ({idx + 1}): U={u}, V={v}")

        # 2. Compute Homogeneous Coordinate
        p = np.array([
            [u],
            [v],
            [1]
        ])
        homogeneous_coordinates.append(p)

        # 3. Compute 3D viewing direction vector: d = K^-1 * p
        d = np.linalg.solve(K, p)
        viewing_directions.append(d)

        dx = d[0][0]
        dy = d[1][0]
        dz = d[2][0]

        d_magnitude = math.sqrt(dx**2 + dy**2 + dz**2)

        d_hat = d / d_magnitude

        # Map directly to letter
        points_dict[letter] = {
            "pixel": (u, v),
            "homogeneous": p,
            "viewing_direction": d,
            "d_hat": d_hat,
            "C_cyl": C_cyl
        }

        # 4. Draw marker dot
        cv2.circle(display_img, (u, v), 5, (0, 0, 255), -1)

        # 5. Render clean labels (P, Q, R, S) and coordinate text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2.5
        thickness = 2
        gap = 35
        start_x = u + 25
        start_y = v - 15

        # Draw Yellow Letter
        letter_text = f"{letter}:"
        cv2.putText(display_img, letter_text, (start_x, start_y),
                    font, font_scale, (0, 255, 255), thickness, cv2.LINE_AA)

        # Measure text width to cleanly position coordinates
        (text_width, _), _ = cv2.getTextSize(letter_text, font, font_scale, thickness)

        # Draw White Coordinates
        coords_text = f"({u}, {v})"
        cv2.putText(display_img, coords_text, (start_x + text_width + gap, start_y),
                    font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

        # Draw Optical Center Marker
        cv2.drawMarker(display_img, (cx, cy), (0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=30, thickness=2)
        cv2.putText(display_img, f"Origin ({cx}, {cy})", (cx + 20, cy + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Image Window", display_img)

image_path = '/Users/ryanmondong/Downloads/IMG_2667.JPG'
original_img = cv2.imread(image_path)

if original_img is None:
    print("Error: Could not load image. Check the file path.")
else:
    display_img = original_img.copy()

    cv2.namedWindow("Image Window")
    cv2.setMouseCallback("Image Window", mouse_click_callback)
    cv2.imshow("Image Window", display_img)

    print("Click on the image to store coordinates (P, Q, R, S). Press 'ESC' or 'q' to exit.")

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cv2.destroyAllWindows()

    print(f"\nSession finished. Total coordinates captured: {len(clicked_coordinates)}")

    # Print out results organized by letter
    for letter, data in points_dict.items():
        print(f"\n================ Point {letter} ================")
        print(f"2D Pixel Coordinate: {data['pixel']}")
        print(f"Homogeneous Coordinates:\n{data['homogeneous']}")
        print(f"Viewing Direction vector (d):\n{data['viewing_direction']}")
        print(f"Normalized Viewing Direction (d_hat):\n{data['d_hat']}")
        print(f"Estimated Cylinder Axis Point (C_cyl):\n{data['C_cyl']}")