import tkinter as tk

import PIL.Image
import PIL.ImageTk
import cv2

# Load the Haar cascade classifier
defect_cascade = cv2.CascadeClassifier("defect.xml")
nut_cascade = cv2.CascadeClassifier("nutz.xml")

# Start the video capture
cap = cv2.VideoCapture(0)

# Create the Tkinter GUI
root = tk.Tk()
root.title("Live Video Stream - Haar Cascade Defective Nuts Detection")
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


# Function to update the video frame
def update_frame():
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect nuts in the frame using the Haar cascade classifier
    nuts = nut_cascade.detectMultiScale(gray, scaleFactor=scaleFactor_scale.get(),
                                        minNeighbors=minNeighbors_scale.get(), minSize=(30, 30))

    defect = defect_cascade.detectMultiScale(gray, scaleFactor=scaleFactor_scale.get(),
                                             minNeighbors=minNeighbors_scale.get(), minSize=(30, 30))

    # Draw rectangles around the nuts
    for (x, y, w, h) in nuts:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, "NON-DEFECT", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

    #for (x, y, w, h) in defect:
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #cv2.putText(frame, "DEFECT", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

    # Convert the frame to a PhotoImage object
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

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
