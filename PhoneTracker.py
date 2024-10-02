# Need to have these all downloaded
import cv2
import torch
import os
import warnings
import time
import osascript
import matplotlib.pyplot as plt

# Replace with path to beep alert desired
def show_alert():
    osascript.osascript("set volume output volume 30")
    os.system(f'afplay "/Users/julianambrose/PycharmProjects/yolov5/124895__greencouch__beeps-15.wav"')

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Load the YOLOv5 model with the local weights, use your path
model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path='/Users/julianambrose/PycharmProjects/yolov5/yolov5m.pt')


# Get from webcam
cap = cv2.VideoCapture(0)

monitoring_objects = ['cell phone', 'remote']
confidence_threshold = 0.3
monitor_duration = 60  # time in seconds
leeway_duration = 5
detected_time = 0  # Time in seconds for which the object is detected
last_detected_time = 0
is_alerted = False
start_time = None
missed_frames = 0
max_frames = 150 # You need to change this to max time (sec) * FPS (30 FPS for Mac)
total_time_on = 0
time_on_current = 0

if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    detected = False
    results = model(frame)


    for *box, conf, cls in results.xyxy[0]:
        label = model.names[int(cls)]

        if label in monitoring_objects and conf > confidence_threshold:
            detected = True
            current_time = time.time()

            # If we just started detecting, set start_time
            if start_time is None:
                start_time = current_time

            # Update detected time
            detected_time = current_time - start_time

            # Check if the object has been detected for the required duration
            if detected_time >= monitor_duration:
                show_alert()
                detected_time = 0
                start_time = None

        elif detected and conf < confidence_threshold:
            # If detected but confidence drops, check if we should allow leeway
            current_time = time.time()
            if start_time != None:
                if not ((current_time - start_time) <= leeway_duration) and missed_frames > max_frames:
                    start_time = None
                    detected_time = 0
                    detected = False

            # Reset timer if the object is not detected
        if detected:
            missed_frames = 0
        else:
            missed_frames += 1
            if start_time is not None and (time.time() - start_time) >= leeway_duration and missed_frames > max_frames:
                start_time = None  # Reset start time if not detected for leeway
                detected_time = 0
                missed_frames = 0

    results.render()

    # Convert the frame to RGB (for matplotlib)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the frame with detections (Comment this out to run smoother and without background window)
    # cv2.imshow("Webcam", rgb_frame)
    plt.axis('off')  # Turn off axis
    plt.show(block=False)
    plt.pause(0.001)  # Pause to allow the display to update

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Release the capture when done
cv2.destroyAllWindows()  # Close any OpenCV windows

print(total_time_on)