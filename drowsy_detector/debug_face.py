import cv2

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

if face_cascade.empty():
    print("ERROR: Could not load face detector")
    exit()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Cannot open webcam")
    exit()

print("Face detection debug. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Try different preprocessing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Try adjusting the detection parameters (more sensitive)
    # scaleFactor=1.1 makes it more sensitive but slower
    # minNeighbors=3 detects more faces (but might have false positives)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
    
    # Print number of faces detected
    print(f"Faces detected: {len(faces)}", end="\r")
    
    # Draw rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.putText(frame, "FACE DETECTED", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()