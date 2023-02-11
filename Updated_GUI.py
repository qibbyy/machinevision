import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import RPi.GPIO as GPIO
import time
import threading

# Load the Haar cascade classifier
nut_cascade = cv2.CascadeClassifier("defect2.xml")

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the servo motor
servo_pin = 17

# Initialize the GPIO pin as an output
GPIO.setup(servo_pin, GPIO.OUT)

# Create a PWM instance for the servo motor
servo = GPIO.PWM(servo_pin, 50)

# Start the PWM with a duty cycle of 7.5% (neutral position)
servo.start(12.5)

# Start the video capture
cap = cv2.VideoCapture(0)

# Create the Tkinter GUI
root = tk.Tk()
root.title("Live Video Stream - Haar Cascade Detection")
root.geometry("800x600")

# Create a label to display the video frame
frame_label = tk.Label(root)
frame_label.pack(side=tk.LEFT, padx=10, pady=10)

# Create a frame to hold the controls
controls_frame = tk.Frame(root)
controls_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Create a label for the minNeighbors scale
minNeighbors_label = tk.Label(controls_frame, text="minNeighbors")
minNeighbors_label.pack()

# Create a scale to control the minNeighbors parameter
minNeighbors_scale = tk.Scale(controls_frame, from_=1, to=10, orient=tk.HORIZONTAL, resolution=1)
minNeighbors_scale.pack()
minNeighbors_scale.set(5)

# Create a label for the scaleFactor scale
scaleFactor_label = tk.Label(controls_frame, text="scaleFactor")
scaleFactor_label.pack()

# Create a scale to control the scaleFactor parameter
scaleFactor_scale = tk.Scale(controls_frame, from_=1.1, to=2, orient=tk.HORIZONTAL, resolution=0.1)
scaleFactor_scale.pack()
scaleFactor_scale.set(1.1)


# Function to control the servo motor
def control_servo(position):
    # Set the duty cycle for the servo motor
    servo.ChangeDutyCycle(position)


# Function to update the video frame
def update_frame():
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    height, width = gray.shape
    roi = gray[0:height, int(width / 2):width]

    # Detect faces in the frame using the Haar cascade classifier
    defect = nut_cascade.detectMultiScale(roi, scaleFactor=scaleFactor_scale.get(),
                                          minNeighbors=minNeighbors_scale.get(), minSize=(30, 30))

    # Draw rectangles around the faces
    for (x, y, w, h) in defect:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Check if a face was detected
    if len(defect) > 0:
        # Start a new thread to perform the servo motor movements
        servo_thread = threading.Thread(target=move_servo)
        servo_thread.start()

    # Convert the frame to a PhotoImage object
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

    # Update the frame label with the new frame
    frame_label.config(image=frame)
    frame_label.image = frame

    # Repeat this function after a delay of 15 milliseconds
    root.after(15, update_frame)


# Function to move the servo motor
def move_servo():
    # Move the servo motor to 180 degrees
    servo.ChangeDutyCycle(7.5)
    time.sleep(1)

    # Move the servo motor back to 0 degrees
    servo.ChangeDutyCycle(12.5)


# Start updating the video frame
update_frame()

# Start the Tkinter GUI event loop
root.mainloop()

# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
