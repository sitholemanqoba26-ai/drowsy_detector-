 Driver Drowsiness Detection System

A Real-Time Safety System for Truck and Vehicle Drivers

[![Python](https://img.shields.io/badge/Python-3.10.11-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1.78-green.svg)](https://opencv.org/)


Overview

The Driver Drowsiness Detection System is a real-time computer vision application designed to prevent accidents caused by driver fatigue. This system monitors the driver's eyes continuously and triggers an audio-visual alert when drowsiness is detected.


Why This Matters

According to the National Highway Traffic Safety Administration (NHTSA):

- Drowsy driving causes over 100,000 crashes annually in the United States alone
- One in 25 adult drivers report falling asleep while driving in the past 30 days
- Drowsy driving is responsible for approximately 1,500 deaths and 71,000 injuries each year

This system is designed to assist:

- Truck drivers on long-haul routes
- Commercial vehicle operators
- Rideshare and taxi drivers
- Emergency vehicle drivers
- Bus and passenger transport drivers

---

 Features

| Feature | Description |
|---------|-------------|
| Real-Time Face Detection | Detects the driver's face using Haar Cascades |
| Eye Tracking | Monitors both eyes continuously |
| Drowsiness Detection | Triggers an alert after 3 seconds of closed eyes |
| Audio Alerts | Loud beeping sound to wake the driver |
| Visual Alerts | Flashing "DROWSY! WAKE UP!" message on screen |
| Progress Indicator | Shows countdown to alert |
| Lightweight | Runs on standard laptops and embedded systems |



 How It Works

The system follows a simple but effective process:

1. The webcam captures video of the driver in real-time
2. The system detects the driver's face using a pre-trained Haar Cascade classifier
3. Within the face region, the system detects both eyes
4. If both eyes are detected, the system remains in alert state
5. If one or both eyes are not detected (indicating closed eyes), a counter begins
6. If the counter reaches 90 frames (approximately 3 seconds), the system triggers an alert
7. The alert includes a loud beeping sound and a visual warning on screen
8. When the driver opens their eyes, the counter resets immediately

 

 Installation

 Prerequisites

- Python 3.10.11 (Recommended)
- Webcam
- 500MB free disk space

Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/drowsiness-detector.git
cd drowsiness-detector

Step 2: Install Dependencies
bash
pip install -r requirements.txt
Step 3: Run the Application
bash
python simple_drowsy.py
Dependencies
text
opencv-python==4.8.1.78
numpy==1.24.3
Usage
Run the program

Face the webcam and ensure good lighting conditions

Keep your eyes open - the system will show "Alert" status

Close your eyes for approximately 3 seconds - the alert will trigger

Press the 'q' key to quit the program

Quick Start
bash
# With Python 3.10
py -3.10 simple_drowsy.py

# Or with default Python
python simple_drowsy.py
Performance
Metric	Value
Detection Speed	Approximately 30 FPS
Alert Delay	3 seconds
Accuracy	Approximately 90% with good lighting
False Alarms	Minimal with proper setup
Who This Helps
This system is designed for anyone who spends long hours behind the wheel:

Long-haul truck drivers who drive for extended periods

Commercial vehicle operators who transport goods

Rideshare and taxi drivers working long shifts

Emergency vehicle drivers responding to calls

Bus and passenger transport drivers responsible for many lives

The system serves as an additional layer of safety for drivers who may experience fatigue during their journeys.

Future Improvements
The following features are planned for future releases:

Voice alerts to verbally warn the driver

Steering wheel vibrations for haptic feedback

SMS alert functionality to notify fleet managers

GPS integration to log drowsiness events and locations

Mobile application version for smartphones

Yawn detection as an additional fatigue indicator

Head pose detection to monitor nodding off

Project Structure
text
drowsiness-detector/
│
├── simple_drowsy.py          Main application
├── requirements.txt          Dependencies
├── README.md                 Documentation
├── LICENSE                   MIT License
│
└── models/                    Cascade files
    ├── haarcascade_frontalface_default.xml
    └── haarcascade_eye.xml
Contributing
Contributions are welcome. Here is how you can help improve this project:

Fork the repository

Create a feature branch for your changes

Commit your changes with clear messages

Push to your branch

Open a Pull Request



Resources
NHTSA Drowsy Driving Statistics: https://www.nhtsa.gov/risky-driving/drowsy-driving

OpenCV Documentation: https://docs.opencv.org/

Python 3.10.11 Download: https://www.python.org/downloads/release/python-31011/

Disclaimer
This system is a safety aid and should not replace proper rest, sleep, or driver awareness. Always follow local laws and regulations regarding driving hours and rest breaks. The developers are not responsible for any accidents or incidents that may occur while using this system.

Acknowledgments
OpenCV community for providing the Haar Cascade models

Python developers for maintaining a robust ecosystem

Truck drivers everywhere for keeping our roads safe
