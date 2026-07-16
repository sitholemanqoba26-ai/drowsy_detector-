import cv2

# Open the webcam (0 = default camera)
cap = cv2.VideoCapture(0)

# Check if it opened
if not cap.isOpened():
    print("ERROR: Cannot access webcam")
    exit()

print("Webcam working! Press 'q' to quit.")

while True:
    # Grab a single frame
    ret, frame = cap.read()
    
    if not ret:
        print("ERROR: Failed to grab frame")
        break

    # Show the frame in a window
    cv2.imshow("My Webcam", frame)

    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()