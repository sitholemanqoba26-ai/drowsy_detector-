import cv2
import dlib
import numpy as np
from scipy.spatial import distance

# ----------------------------
# CONFIGURATION
# ----------------------------
EYE_AR_THRESH = 0.25          # EAR threshold (below = eyes closed)
EYE_AR_CONSEC_FRAMES = 20     # Number of frames eyes must be closed
YAWN_THRESH = 0.7             # Mouth aspect ratio threshold
HEAD_TILT_THRESH = 25         # Head tilt angle threshold

# ----------------------------
# LOAD MODELS
# ----------------------------
print("Loading face detector...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def eye_aspect_ratio(eye):
    """Calculate Eye Aspect Ratio (EAR)"""
    # Compute the euclidean distances between the two sets of vertical eye landmarks
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    # Compute the euclidean distance between the horizontal eye landmark
    C = distance.euclidean(eye[0], eye[3])
    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear

def mouth_aspect_ratio(mouth):
    """Calculate Mouth Aspect Ratio (MAR)"""
    A = distance.euclidean(mouth[2], mouth[10])  # vertical distance
    B = distance.euclidean(mouth[4], mouth[8])   # vertical distance
    C = distance.euclidean(mouth[0], mouth[6])   # horizontal distance
    mar = (A + B) / (2.0 * C)
    return mar

def get_eye_landmarks(shape, eye_indices):
    """Extract eye landmarks from shape predictor"""
    eye = []
    for i in eye_indices:
        eye.append((shape.part(i).x, shape.part(i).y))
    return eye

# Eye indices in the 68-point model
LEFT_EYE_INDICES = list(range(42, 48))
RIGHT_EYE_INDICES = list(range(36, 42))
MOUTH_INDICES = list(range(48, 68))

# ----------------------------
# MAIN LOOP
# ----------------------------
print("Starting drowsiness detector...")
print("Press 'q' to quit")

# Initialize counters
eye_closed_counter = 0
yawn_counter = 0
drowsy_alert = False

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for faster processing
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector(gray, 0)

    for face in faces:
        # Get facial landmarks
        shape = predictor(gray, face)

        # Get left and right eye landmarks
        left_eye = get_eye_landmarks(shape, LEFT_EYE_INDICES)
        right_eye = get_eye_landmarks(shape, RIGHT_EYE_INDICES)
        mouth = get_eye_landmarks(shape, MOUTH_INDICES)

        # Calculate EAR for both eyes
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # Calculate MAR (yawn detection)
        mar = mouth_aspect_ratio(mouth)

        # Draw eye and mouth landmarks
        for (x, y) in left_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        for (x, y) in right_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        for (x, y) in mouth:
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

        # Display EAR value
        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"MAR: {mar:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # ---------- DROWSINESS DETECTION LOGIC ----------
        
        # Check if eyes are closed (EAR below threshold)
        if ear < EYE_AR_THRESH:
            eye_closed_counter += 1
            
            # If eyes closed for too many frames -> DROWSY
            if eye_closed_counter >= EYE_AR_CONSEC_FRAMES:
                cv2.putText(frame, "*** DROWSY! WAKE UP! ***", (150, 200), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
                cv2.putText(frame, "*** DROWSY! WAKE UP! ***", (150, 250), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
                drowsy_alert = True
        else:
            eye_closed_counter = 0
            drowsy_alert = False

        # Check for yawn (MAR above threshold)
        if mar > YAWN_THRESH:
            yawn_counter += 1
            if yawn_counter > 5:  # Only show if yawn lasts a few frames
                cv2.putText(frame, "*** YAWN DETECTED ***", (200, 300), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 3)
        else:
            yawn_counter = 0

        # Display status
        if drowsy_alert:
            status = "STATUS: DROWSY!"
            color = (0, 0, 255)
        elif eye_closed_counter > 0:
            status = f"STATUS: Eyes closing ({eye_closed_counter}/{EYE_AR_CONSEC_FRAMES})"
            color = (0, 255, 255)
        else:
            status = "STATUS: Alert"
            color = (0, 255, 0)
            
        cv2.putText(frame, status, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # Show the frame
    cv2.imshow("Drowsiness Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()