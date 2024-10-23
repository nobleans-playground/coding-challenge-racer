from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from math import ceil

def resize_image(image, window):
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate maximum dimensions while maintaining aspect ratio
    max_width = int(screen_width * 0.95)  # Use 95% of screen width
    max_height = int(screen_height * 0.95)  # Use 95% of screen height

    # Calculate scaling factor
    width_ratio = max_width / image.width
    height_ratio = max_height / image.height
    scale_factor = min(width_ratio, height_ratio)
    track_width = 25

    print(f"scale = {scale_factor}")
    print(f"track_width = {track_width}")
    print("lines = [")

    # Calculate new dimensions
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)

    # Resize image
    return image.resize((new_width, new_height), Image.LANCZOS), scale_factor, track_width

def on_click(event):
    global last_point, temp_line
    x, y = event.x, event.y

    # Adjust coordinates back to original scale
    orig_x = int(x / scale_factor)
    orig_y = int(y / scale_factor)

    print(f"    ({orig_x}, {orig_y}),")

    if last_point:
        line = canvas.create_line(last_point[0], last_point[1], x, y, fill="red", width=2)
        lines.append(line)

    last_point = (x, y)

    if temp_line:
        canvas.delete(temp_line)
    temp_line = canvas.create_line(x, y, x, y, fill="blue", dash=(4, 4))

def update_cursor(event):
    global temp_line, track_width
    x, y = event.x, event.y

    canvas.delete("circle")
    canvas.create_oval(x-track_width, y-track_width, x+track_width, y+track_width,
                       outline="red", width=2, tags="circle")

    if last_point and temp_line:
        canvas.coords(temp_line, last_point[0], last_point[1], x, y)

def on_closing():
    window.quit()
    window.destroy()

# Open an image file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
if not file_path:
    print("No file selected. Exiting.")
    root.quit()
    exit()

# Create main window first to get screen dimensions
window = tk.Toplevel()

# Open and resize image
original_image = Image.open(file_path)
image, scale_factor, track_width = resize_image(original_image, window)
rgb_image = image.convert('RGB')

# Create PhotoImage
photo = ImageTk.PhotoImage(rgb_image)

# Create a canvas and display the image on it
canvas = tk.Canvas(window, width=image.width, height=image.height)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Initialize variables
lines = []
last_point = None
temp_line = None

# Bind events to the canvas
canvas.bind("<Button-1>", on_click)
canvas.bind("<Motion>", update_cursor)

# Set up the window close event
window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
window.mainloop()
print("]")

