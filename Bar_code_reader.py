import cv2
from pyzbar.pyzbar import decode
from PIL import Image


# Function to decode the barcode from a camera frame
def decode_barcode(frame):
    # Convert the frame to grayscale for better processing
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode the barcode using pyzbar
    barcodes = decode(gray_frame)
    for barcode in barcodes:
        # Extract the barcode data as a string
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        print(f"Found {barcode_type} barcode: {barcode_data}")

        # Draw a rectangle around the detected barcode
        points = barcode.polygon
        if len(points) == 4:
            cv2.polylines(frame, [np.array(points, np.int32)], True, (0, 255, 0), 2)

    return frame


# Access the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame is captured successfully
    if ret:
        # Decode the barcode from the frame
        frame = decode_barcode(frame)

        # Display the resulting frame
        cv2.imshow('Barcode Scanner', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
