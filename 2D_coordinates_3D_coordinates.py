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

# Current reference measurement labels
labels = ['m_0', 'm_1', 'm_2', 'm_3', 'P', 'Q', 'R', 'S']

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
    # Only capture up to 8 points (m_0..m_3, P..S)
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_coordinates) < len(labels):
        idx = len(clicked_coordinates)
        letter = labels[idx]

        # 1. Store pixel coordinate
        clicked_coordinates.append((u, v))
        print(f"Stored Point {letter} ({idx + 1}): U={u}, V={v}")

        # Compute Homogeneous Coordinate & viewing ray
        p = np.array([[u], [v], [1]], dtype=np.float64)
        d = np.linalg.solve(K, p)
        d_hat = d / np.linalg.norm(d)

        # Store in dictionary
        points_dict[letter] = {
            "pixel": (u, v),
            "homogeneous": p,
            "viewing_direction": d,
            "d_hat": d_hat
        }

        # 4. Draw marker dot (Red for reference line, Green for Box 1)
        dot_color = (0, 0, 255) if idx < 4 else (0, 255, 0)
        cv2.circle(display_img, (u, v), 5, dot_color, -1)

        # 5. Render clean labels and coordinate text (Original Styling)
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
        cv2.drawMarker(display_img, (int(cx), int(cy)), (0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=30, thickness=2)
        cv2.putText(display_img, f"Origin ({int(cx)}, {int(cy)})", (int(cx) + 20, int(cy) + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Image Window", display_img)

        # Prompt user after completing calibration marks
        if len(clicked_coordinates) == 4:
            print("\n>>> Reference points m_0 to m_3 recorded!")
            print(">>> Now click the 4 corners of Box 1 (P -> Q -> R -> S in order)...\n")

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

    print("\n================ Cylinder Axis Direction (a_hat) ===========")
    print(f"a_hat: [{a_hat[0]:.4f}, {a_hat[1]:.4f}, {a_hat[2]:.4f}]")

    # Normal vector pointing inward from surface point M0 to the central axis
    n_dir = -M0 - np.dot(-M0, a_hat) * a_hat
    n_hat = n_dir / np.linalg.norm(n_dir)

    # Walk inward from surface marker M0 by radius (4.25 cm) to reach center axis A
    A = M0 + radius * n_hat

    print("\n================ Cylinder Axis Anchor (A) ================")
    print(f"A: X = {A[0]:.2f}, Y = {A[1]:.2f}, Z = {A[2]:.2f}")

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

    # ========================================================
    # Next Step: Ray-Cylinder Intersection & Patch Unwrapping
    # ========================================================

    # Reference orthogonal basis on the cylinder cross-section
    u_axis = -n_hat
    u_axis = u_axis - np.dot(u_axis, a_hat) * a_hat
    u_axis = u_axis / np.linalg.norm(u_axis)
    v_axis = np.cross(a_hat, u_axis)

    def intersect_ray_cylinder(d_hat, A_anchor, a_hat_dir, R_cyl):
        """Calculates the 3D surface intersection for a camera ray."""
        v = np.cross(d_hat, a_hat_dir)
        w = np.cross(-A_anchor, a_hat_dir)

        c2 = np.dot(v, v)
        c1 = 2.0 * np.dot(v, w)
        c0 = np.dot(w, w) - (R_cyl ** 2)

        discriminant = c1**2 - 4.0 * c2 * c0
        if discriminant < 0:
            raise ValueError("Ray does not intersect cylinder.")

        t1 = (-c1 - np.sqrt(discriminant)) / (2.0 * c2)
        t2 = (-c1 + np.sqrt(discriminant)) / (2.0 * c2)

        # Pick the positive root facing the pipe surface
        t_candidates = [t for t in (t1, t2) if t > 0]
        t_val = max(t_candidates)
        P_3d = t_val * d_hat
        return P_3d

    # Target patch reconstruction from live user clicks (P, Q, R, S)
    patch_3d = {}
    patch_unwrapped = {}

    print("\n================ Reconstructed Patch Corners (P, Q, R, S) ================")
    for label in ['P', 'Q', 'R', 'S']:
        d_hat = points_dict[label]['d_hat'].flatten()

        # 1. 3D point on cylinder surface
        P_xyz = intersect_ray_cylinder(d_hat, A, a_hat, radius)
        patch_3d[label] = P_xyz

        # 2. Convert to cylindrical coordinates (s = R * theta, z)
        rel_vec = P_xyz - A
        z_axial = np.dot(rel_vec, a_hat)
        radial_proj = rel_vec - z_axial * a_hat
        theta = np.arctan2(np.dot(radial_proj, v_axis), np.dot(radial_proj, u_axis))
        s_arc = radius * theta

        patch_unwrapped[label] = (s_arc, z_axial)
        print(f"{label}: 3D = [{P_xyz[0]:6.2f}, {P_xyz[1]:6.2f}, {P_xyz[2]:6.2f}] cm | Unwrapped (s, z) = ({s_arc:6.2f}, {z_axial:6.2f}) cm")

# 3. Compute 2D unwrapped polygon area via Shoelace formula
    pts_2d = np.array([patch_unwrapped[lbl] for lbl in ['P', 'Q', 'R', 'S']])
    
    # Sort vertices counter-clockwise around their geometric centroid to prevent crossing diagonals
    centroid = np.mean(pts_2d, axis=0)
    angles = np.arctan2(pts_2d[:, 1] - centroid[1], pts_2d[:, 0] - centroid[0])
    sort_order = np.argsort(angles)
    sorted_pts = pts_2d[sort_order]

    s_pts = sorted_pts[:, 0]
    z_pts = sorted_pts[:, 1]
    calc_area = 0.5 * np.abs(np.dot(s_pts, np.roll(z_pts, 1)) - np.dot(z_pts, np.roll(s_pts, 1)))

    # Ground truth comparison from Notion for Box I (9.3 cm * 6.9 cm)
    actual_area_cm2 = 64.2
    abs_area_err = abs(calc_area - actual_area_cm2)
    pct_area_err = (abs_area_err / actual_area_cm2) * 100.0

    print("\n================ Patch Area Result ================")
    print(f"Calculated Unwrapped Surface Area: {calc_area:.2f} cm^2")
    print(f"Ground Truth Flat Area           : {actual_area_cm2:.2f} cm^2")
    print(f"Absolute Area Error              : {abs_area_err:.2f} cm^2")
    print(f"Percentage Error                 : {pct_area_err:.2f}%")

    # ========================================================
    # Save Figures for Report / Advisor Deliverables
    # ========================================================
    import matplotlib.pyplot as plt

    # Figure 1: Unwrapped Surface (s = R*theta vs z)
    plt.figure(figsize=(7, 6))
    patch_poly = np.vstack([sorted_pts, sorted_pts[0]])
    plt.plot(patch_poly[:, 0], patch_poly[:, 1], 'r-o', label=f'Patch (Area: {calc_area:.2f} cm²)')
    plt.fill(patch_poly[:, 0], patch_poly[:, 1], 'red', alpha=0.15)

    # Plot the reference line (s = 0)
    ref_z = [np.dot(M - A, a_hat) for M in M_points]
    plt.plot([0]*4, ref_z, 'b--s', label='5-cm Axis Markers')

    for lbl in ['P', 'Q', 'R', 'S']:
        s_val, z_val = patch_unwrapped[lbl]
        plt.annotate(lbl, (s_val, z_val), textcoords="offset points", xytext=(6, 6))

    plt.title('Unwrapped Cylindrical Surface ($s = R\\theta$ vs $z$)')
    plt.xlabel('Circumferential Arc Length $s$ (cm)')
    plt.ylabel('Axial Depth $z$ (cm)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.axis('equal')
    plt.savefig('unwrapped_patch.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Figure 2: 3D Scene (Camera Origin, Cylinder Axis, 3D Points)
    fig3d = plt.figure(figsize=(8, 7))
    ax3d = fig3d.add_subplot(111, projection='3d')

    ax3d.scatter(0, 0, 0, color='black', marker='^', s=80, label='Camera Origin (C)')

    axis_s = np.linspace(-2, 35, 30)
    axis_line = np.array([A + s * a_hat for s in axis_s])
    ax3d.plot(axis_line[:, 0], axis_line[:, 1], axis_line[:, 2], 'g--', label='Cylinder Axis')

    ax3d.scatter(M_points[:, 0], M_points[:, 1], M_points[:, 2], color='blue', s=50, label='Markers (m0-m3)')
    patch_coords = np.array([patch_3d[lbl] for lbl in ['P', 'Q', 'R', 'S']])
    ax3d.scatter(patch_coords[:, 0], patch_coords[:, 1], patch_coords[:, 2], color='red', s=50, label='Patch Corners')

    ax3d.set_xlabel('X (cm)')
    ax3d.set_ylabel('Y (cm)')
    ax3d.set_zlabel('Z (cm)')
    ax3d.set_title('3D Pose and Reconstructed Surface Points')
    ax3d.legend()
    plt.savefig('reconstructed_3d_pose.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("\nSaved deliverable plots to 'unwrapped_patch.png' and 'reconstructed_3d_pose.png'")

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
