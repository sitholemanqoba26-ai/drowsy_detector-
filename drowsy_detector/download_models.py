import urllib.request
import os

# Create models folder if it doesn't exist
if not os.path.exists('models'):
    os.makedirs('models')

# Download the facial landmark predictor (68 points)
print("Downloading facial landmark model (98MB)...")
url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
urllib.request.urlretrieve(url, "models/shape_predictor_68_face_landmarks.dat.bz2")

print("Download complete! You need to extract the .bz2 file.")
print("Use 7-Zip or WinRAR to extract it to: models/shape_predictor_68_face_landmarks.dat")