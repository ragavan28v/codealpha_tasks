import cv2
import torch

# Load YOLOv5 model (lightweight nano version)
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')

# Ask user to choose input mode
print("Choose input mode:")
print("1. Video File")
print("2. Live Camera Stream")

choice = input("Enter your choice (1 or 2): ")

if choice == '1':
    video_path = input("Enter the video file path: ")
    cap = cv2.VideoCapture(video_path)
elif choice == '2':
    cap = cv2.VideoCapture(0)  # Default camera
else:
    print("Invalid choice.")
    exit()

if not cap.isOpened():
    print("Error: Cannot open video source.")
    exit()

# Process each frame from the selected input source
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model(frame)

    # Render the bounding boxes on the frame
    result_frame = results.render()[0]

    # Display the frame with detected objects
    cv2.imshow('Object Detection and Tracking', result_frame)

    # Press 'q' to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
