import tkinter as tk

import PIL.Image
import PIL.ImageTk
import cv2
import time
import RPi.GPIO as GPIO


class HaarCascadeClassifier:
    def __init__(self, master):
        # Load the cascade classifier
        # self.nut_cascade = cv2.CascadeClassifier("nutz.xml")
        self.defect_cascade = cv2.CascadeClassifier("defect.xml")

        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(17, GPIO.OUT)
        self.servo = GPIO.PWM(17, 50)
        self.servo.start(0)

        # Open the video capture
        self.cap = cv2.VideoCapture(0)

        # Create a label to display the video
        self.label = tk.Label(master)
        self.label.grid(row=0, column=0, columnspan=2)

        # Create a slider to adjust the minNeighbors parameter
        self.min_neighbors_slider = tk.Scale(master, from_=1, to=10, orient="horizontal", label="minNeighbors")
        self.min_neighbors_slider.grid(row=1, column=0)
        self.min_neighbors_slider.set(3)

        # Create a slider to adjust the scaleFactor parameter
        self.scale_factor_slider = tk.Scale(master, from_=1.1, to=2, resolution=0.1, orient="horizontal",
                                            label="scaleFactor")
        self.scale_factor_slider.grid(row=1, column=1)
        self.scale_factor_slider.set(1.3)

        # Start the video loop
        self.update_frame()

    def move_servo(self):
        servo.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        servo.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        servo.ChangeDutyCycle(7.5)

    def update_frame(self):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        roi = gray[0:height, int(width / 2):width]
        min_neighbors = int(self.min_neighbors_slider.get())
        scale_factor = float(self.scale_factor_slider.get())
        # nuts = self.nut_cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors)
        # for (x, y, w, h) in nuts:
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cv2.putText(frame, "NUTZ", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        defects = self.defect_cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors)
        for (x, y, w, h) in defects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "DEFECT", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        # cv2.rectangle(frame, (int(width / 2), 0), (width, height), (0, 0, 255), 2)
            self.move_servo()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(frame)
        image = PIL.ImageTk.PhotoImage(image)
        self.label.config(image=image)
        self.label.image = image
        root.after(30, self.update_frame)
        self.servo.stop()
        self.GPIO.cleanup()


# Create the main window
root = tk.Tk()
root.title("Haar Cascade Classifier")

# Create an instance of the HaarCascadeClassifier class
app = HaarCascadeClassifier(root)

root.mainloop()
