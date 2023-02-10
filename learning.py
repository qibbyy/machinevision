import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import RPi.GPIO as GPIO
import time

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
servo.start(7.5)

# Start the video capture
cap = cv2.VideoCapture(0)

# Create the Tkinter GUI
root = tk.Tk()
root.title("Live Video Stream - Haar Cascade Detection")
root.geometry("600x400")

# Create a label to display the video frame
frame_label = tk.Label(root)
frame_label.pack()


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

    # Detect faces in the frame using the Haar cascade classifier
    defect = nut_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the faces
    for (x, y, w, h) in defect:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Check if a face was detected
    if len(defect) > 0:
        # Move the servo motor to the full right position (12.5%)
        control_servo(12.5)

        # Wait for 5 seconds
        time.sleep(5)

        # Move the servo motor back to the neutral position (7.5%)
        control_servo(7.5)

    # Convert the frame to a PhotoImage object
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

    # Update the frame label with the new frame
    frame_label.config(image=frame)
    frame_label.image = frame

    # Repeat this function after a delay of 15 milliseconds
    root.after(15, update_frame)


# Start updating the video frame
update_frame()

# Start the Tkinter GUI event loop
root.mainloop()

# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
