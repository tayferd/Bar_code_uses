import tkinter as tk
from tkinter import messagebox
from barcode import ISBN13
from barcode.writer import ImageWriter
from PIL import Image, ImageTk


# Function to generate and display barcode
def generate_and_display_barcode():
    number = entry.get()
    if len(number) != 12:
        messagebox.showerror("Input Error", "Please enter a 12-digit number.")
        return

    try:
        # Generate barcode and save as PNG
        bar_code = ISBN13(number, writer=ImageWriter())
        file_name = "bar_code"
        bar_code.save(file_name)

        # Open and display the barcode image
        img = Image.open(f"{file_name}.png")
        img = img.resize((300, 100))  # Resize the image to fit the window
        img = ImageTk.PhotoImage(img)

        # Update the label to display the image
        barcode_label.config(image=img)
        barcode_label.image = img
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create the main window
root = tk.Tk()
root.title("Barcode Generator")

# Create and place widgets
tk.Label(root, text="Enter 12-digit number:").pack(pady=10)
entry = tk.Entry(root)
entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate Barcode", command=generate_and_display_barcode)
generate_button.pack(pady=10)

# Label to display the barcode image
barcode_label = tk.Label(root)
barcode_label.pack(pady=10)

# Run the tkinter main loop
root.mainloop()
