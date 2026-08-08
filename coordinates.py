import cv2

# Define the mouse click callback function
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: X={x}, Y={y}")
        
        # Draw a small circle on the image where clicked
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        
        # Show coordinates text on the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f"{x},{y}", (x + 5, y - 5), font, 0.5, (255, 0, 0), 1)
        cv2.imshow("Image", img)

# Load the image from your folder
img = cv2.imread('/Users/ryanmondong/Downloads/IMG_2667.JPG')

# Check if image loaded correctly
if img is None:
    print("Error: Could not load image. Check file name and path.")
else:
    cv2.imshow("Image", img)
    
    # Set mouse handler for the window
    cv2.setMouseCallback("Image", click_event)
    
    # Wait until any key is pressed to exit
    cv2.waitKey(0)
    cv2.destroyAllWindows()
