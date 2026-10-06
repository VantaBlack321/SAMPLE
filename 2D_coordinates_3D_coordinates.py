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

# Target patch labels - use later for P, Q, R, S reconstruction
# labels = ['P', 'Q', 'R', 'S']

# Current reference measurement labels
labels = ['m_0', 'm_1', 'm_2', 'm_3']

# Collections
clicked_coordinates = []
homogeneous_coordinates = []
viewing_directions = []

# Dictionary to look up specific points by letter: P, Q, R, S
points_dict = {}

# After four clicks, have:
# points_dict["P"]["d_hat"] → P's normalized direction
# points_dict["Q"]["d_hat"] → Q's normalized direction
# points_dict["R"]["d_hat"] → R's normalized direction
# points_dict["S"]["d_hat"] → S's normalized direction

measurement_labels = ['m_0', 'm_1', 'm_2', 'm_3']

measurement_coordinates = []

axial_positions = [40.0, 35.0, 30.0, 25.0]  # cm

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

# Cylinder pose still to determine:
#
# A = one known/estimated point on cylinder center axis
# a_hat = unit direction vector of cylinder axis
#
# Determine A and a_hat using:
# - radius = 4.25 cm
# - longitudinal reference lines
# - known 5-cm markings
#
# Do NOT estimate cylinder pose from P, Q, R, S.

reference_spacing = 5.0  # cm

# For two consecutive points on the same longitudinal reference line:
#
# M_i     = t_i * d_hat_i
# M_next  = t_next * d_hat_next
#
# M_i - M_next = reference_spacing * a_hat
#
# Therefore:
# t_i * d_hat_i - t_next * d_hat_next
#     = reference_spacing * a_hat

# Known physical constraint:
# ||M_1 - M_0|| = reference_spacing

# Cylinder center axis:
# L(s) = A + s * a_hat
# A     = a 3D point on the cylinder center axis
# a_hat = unit direction vector of the cylinder center axis
# s     = parameter that moves along the cylinder axis

def mouse_click_callback(event, u, v, flags, param):
    """Callback function triggered on mouse events."""
    # Only capture up to 4 points (P, Q, R, S)
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_coordinates) < len(labels):
        idx = len(clicked_coordinates)
        letter = labels[idx]
        axial_position = axial_positions[idx]

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

        measurement_idx = len(measurement_coordinates)
        measurement_label = measurement_labels[measurement_idx] 
        measurement_coordinates.append((u, v))

        # 3. Compute 3D viewing direction vector: d = K^-1 * p
        d = np.linalg.solve(K, p)
        viewing_directions.append(d)

        dx = d[0][0]
        dy = d[1][0]
        dz = d[2][0]

        d_magnitude = math.sqrt(dx**2 + dy**2 + dz**2)

        d_hat = d / d_magnitude

        # A is a 3D point on the cylinder's center axis
        # a_hat is the unit direction vector of the cylinder's center axis
        
        # Next goal:
        # Determine A and a_hat using the known pipe geometry,
        # longitudinal reference lines, and known 5-cm markings.

        # Map directly to letter
        points_dict[letter] = {
            "pixel": (u, v),
            "homogeneous": p,
            "viewing_direction": d,
            "d_hat": d_hat,
            # "C_cyl": C_cyl
            "axial_position": axial_position
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

image_path = '/Users/ryanmondong/Desktop/IMG_2667.JPG'
original_img = cv2.imread(image_path)

if original_img is None:
    print("Error: Could not load image. Check the file path.")
else:
    display_img = original_img.copy()

    cv2.namedWindow("Image Window")
    cv2.setMouseCallback("Image Window", mouse_click_callback)
    cv2.imshow("Image Window", display_img)

    # print("Click on the image to store coordinates (P, Q, R, S). Press 'ESC' or 'q' to exit.")
    print("Click known 5-cm reference markings m_0, m_1, m_2, m_3. Press 'ESC' or 'q' to exit.")

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cv2.destroyAllWindows()

    print(f"\nSession finished. Total coordinates captured: {len(clicked_coordinates)}")

    # Get normalized viewing directions after all 4 points have been clicked
    d0 = points_dict['m_0']['d_hat'].flatten()
    d1 = points_dict['m_1']['d_hat'].flatten()
    d2 = points_dict['m_2']['d_hat'].flatten()
    d3 = points_dict['m_3']['d_hat'].flatten()

    B1 = np.column_stack((
    d0,
    -2 * d1,
    d2,
    np.zeros(3)
    ))

    B2 = np.column_stack((
        np.zeros(3),
        d1,
        -2 * d2,
        d3
    ))

    B = np.vstack((B1, B2))

    # Solve for relative depths using SVD
    U, S, Vt = np.linalg.svd(B)

    t_relative = Vt[-1]

    # SVD can return the same solution with either sign.
    # Camera points should be in front of the camera.
    if np.mean(t_relative) < 0:
        t_relative = -t_relative

    # 1. Scale relative depths to true physical scale (cm)
    diff_01_rel = t_relative[1] * d1 - t_relative[0] * d0
    k_scale = reference_spacing / np.linalg.norm(diff_01_rel)
    t_metric = t_relative * k_scale

    # 2. Compute 3D surface points M_0 through M_3
    M0 = t_metric[0] * d0
    M1 = t_metric[1] * d1
    M2 = t_metric[2] * d2
    M3 = t_metric[3] * d3
    M_points = np.vstack([M0, M1, M2, M3])

    # 3. Estimate cylinder axis direction a_hat
    axis_vector = M3 - M0
    a_hat = axis_vector / np.linalg.norm(axis_vector)

    print("\n================ Metric Surface Points (cm) ================")
    for idx, M in enumerate(M_points):
        print(f"M_{idx}: X={M[0]:.2f}, Y={M[1]:.2f}, Z={M[2]:.2f}")

    print("\n================ Cylinder Axis Direction (a_hat) ===========")
    print(f"a_hat: [{a_hat[0]:.4f}, {a_hat[1]:.4f}, {a_hat[2]:.4f}]")

    # 4. Verify spacing consistency across intervals
    print("\n================ Spacing Verification ================")
    print(f"||M1 - M0|| = {np.linalg.norm(M1 - M0):.2f} cm")
    print(f"||M2 - M1|| = {np.linalg.norm(M2 - M1):.2f} cm")
    print(f"||M3 - M2|| = {np.linalg.norm(M3 - M2):.2f} cm")

    # print("\n================ Depth Constraint Matrix ================")
    # print(B)

    # print("\n================ Viewing Directions ================")
    # print("d0:", d0)
    # print("d1:", d1)
    # print("d2:", d2)
    # print("d3:", d3)

    # Print out results organized by letter
    # for letter, data in points_dict.items():
    #     print(f"\n================ Point {letter} ================")
    #     print(f"2D Pixel Coordinate: {data['pixel']}")
    #     print(f"Homogeneous Coordinates:\n{data['homogeneous']}")
    #     print(f"Viewing Direction vector (d):\n{data['viewing_direction']}")
    #     print(f"Normalized Viewing Direction (d_hat):\n{data['d_hat']}")
    #     print(f"Estimated Cylinder Axis Point (C_cyl):\n{data['C_cyl']}")

    # Print reference measurement coordinates
    # print("\n================ Reference Measurements ================")

    # for measurement_label, coordinate in zip(measurement_labels, measurement_coordinates):
    #     u, v = coordinate
    #     print(f"{measurement_label}: U={u}, V={v}")

    # print(f"Known Physical Spacing: {reference_spacing} cm")

    # print("\n================ Axial Reference Spacing ================")

    # for i in range(len(axial_positions) - 1):
    #     current_position = axial_positions[i]
    #     next_position = axial_positions[i + 1]

    #     spacing = abs(current_position - next_position)

    #     print(
    #         f"{measurement_labels[i]} ({current_position} cm) -> "
    #         f"{measurement_labels[i + 1]} ({next_position} cm): "
    #         f"{spacing} cm"
    #     )
