import tkinter as tk
from tkinter import Label, Button
from pyzbar.pyzbar import decode
import cv2
from PIL import Image, ImageTk
import threading
import numpy as np


class BarcodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Barcode Scanner")
        self.root.geometry("600x400")

        self.camera_on = False  # Flag to control the camera
        self.cap = None  # Video capture object

        # Create GUI elements
        self.start_button = Button(self.root, text="Start Scanning", command=self.start_camera)
        self.start_button.pack(pady=20)

        self.stop_button = Button(self.root, text="Stop Scanning", command=self.stop_camera, state="disabled")
        self.stop_button.pack(pady=20)

        self.label = Label(self.root, text="Scanned Barcode Data:", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.result_text = Label(self.root, text="", font=("Helvetica", 14), fg="blue")
        self.result_text.pack(pady=10)

        self.video_frame = Label(self.root)
        self.video_frame.pack(pady=10)

    def start_camera(self):
        if not self.camera_on:
            self.camera_on = True
            self.cap = cv2.VideoCapture(0)  # Open camera
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            threading.Thread(target=self.camera_loop, daemon=True).start()

    def stop_camera(self):
        self.camera_on = False
        if self.cap is not None:
            self.cap.release()  # Release the camera
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.video_frame.config(image="")  # Clear the video feed display

    def camera_loop(self):
        while self.camera_on:
            ret, frame = self.cap.read()
            if ret:
                # Process the frame and decode barcodes
                barcodes = decode(frame)
                for barcode in barcodes:
                    barcode_data = barcode.data.decode('utf-8')
                    barcode_type = barcode.type
                    self.result_text.config(text=f"Type: {barcode_type}, Data: {barcode_data}")

                    # Draw rectangle around the barcode
                    points = barcode.polygon
                    if len(points) == 4:
                        cv2.polylines(frame, [np.array(points, np.int32)], True, (0, 255, 0), 2)

                # Convert the frame to display in tkinter
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(image=img)

                # Update the video feed
                self.video_frame.config(image=img)
                self.video_frame.image = img

            # Delay for a bit to let the GUI update
            self.root.update_idletasks()
            self.root.update()

        # Release the camera when loop ends
        if self.cap is not None:
            self.cap.release()


# Create the main window and run the app
root = tk.Tk()
app = BarcodeScannerApp(root)
root.mainloop()
