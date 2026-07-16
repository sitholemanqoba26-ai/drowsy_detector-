import cv2
import time
import winsound
import threading

print("Starting Drowsiness Detector with Sound Alerts...")
print("Press 'q' to quit")

# Load face and eye detectors
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Cannot access webcam")
    exit()

# Alert settings
ALERT_SECONDS = 3  # Alert after 3 seconds of eyes closed
FRAME_RATE = 30    # Frames per second
ALERT_FRAMES = ALERT_SECONDS * FRAME_RATE  # ~90 frames

# Variables
closed_counter = 0
alert_playing = False
last_alert_time = 0
alert_cooldown = 5  # Don't repeat alert for 5 seconds

def play_alarm():
    """Play sound alert"""
    global alert_playing
    
    # Play 5 beeps
    for i in range(5):
        winsound.Beep(1000, 300)  # 1000 Hz for 300ms
        time.sleep(0.1)
        winsound.Beep(1500, 300)  # 1500 Hz for 300ms
        time.sleep(0.1)
    
    alert_playing = False

print("Webcam opened! Looking for faces...")
print(f"Alert will sound after {ALERT_SECONDS} seconds of closed eyes")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip for mirror view
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # If no face detected, show warning
    if len(faces) == 0:
        cv2.putText(frame, "No face detected!", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    for (x, y, w, h) in faces:
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Get face region for eyes
        roi_gray = gray[y:y+h//2, x:x+w]
        roi_color = frame[y:y+h//2, x:x+w]
        
        # Detect eyes
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3, minSize=(20, 20))
        
        # Draw eye rectangles
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

        # ---------- DROWSINESS LOGIC ----------
        
        # If less than 2 eyes detected -> eyes are closed
        if len(eyes) < 2:
            closed_counter += 1
            
            # Calculate seconds closed
            seconds_closed = closed_counter / FRAME_RATE
            
            # Show progress bar
            progress = min(closed_counter / ALERT_FRAMES, 1.0)
            bar_length = 30
            filled = int(bar_length * progress)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            cv2.putText(frame, f"Eyes closed: {seconds_closed:.1f}s", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, f"[{bar}]", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            # Check if eyes closed for long enough
            if closed_counter >= ALERT_FRAMES:
                # Show alert on screen
                cv2.putText(frame, "!!! DROWSY! WAKE UP !!!", (100, 200), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 6)
                cv2.putText(frame, "!!! DROWSY! WAKE UP !!!", (100, 250), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 6)
                
                # Play sound alert (only if not already playing and cooldown over)
                current_time = time.time()
                if not alert_playing and (current_time - last_alert_time > alert_cooldown):
                    alert_playing = True
                    threading.Thread(target=play_alarm, daemon=True).start()
                    last_alert_time = current_time
                
                status = "DROWSY!"
                color = (0, 0, 255)
            else:
                status = f"Eyes closing... {seconds_closed:.1f}s/{ALERT_SECONDS}s"
                color = (0, 255, 255)
        else:
            # Eyes open - reset counter
            if closed_counter > 0:
                print(f"Eyes opened after {closed_counter/FRAME_RATE:.1f} seconds")
            closed_counter = 0
            status = "Alert"
            color = (0, 255, 0)
            alert_playing = False

        # Show status
        cv2.putText(frame, f"Status: {status}", (10, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, f"Eyes detected: {len(eyes)}", (10, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show the frame
    cv2.imshow("Drowsiness Detector with Sound", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Program ended.")