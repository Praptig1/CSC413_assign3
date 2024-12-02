import serial
from PIL import Image, ImageTk
import os
import shutil  # To copy files
import tkinter as tk

# Configuration
serial_port = "COM3"  # Replace with the Arduino's port
baud_rate = 9600
image_folder = r"C:\Users\af34j\OneDrive\Desktop\School\CSC413\A3\IRLED\images\today"  # Replace with the folder containing your images
accepted_folder = r"C:\Users\af34j\OneDrive\Desktop\School\CSC413\A3\IRLED\images\all"  # Folder to save all accepted images
favorited_folder = r"C:\Users\af34j\OneDrive\Desktop\School\CSC413\A3\IRLED\images\favorites"  # Folder to save favorited images

# Ensure folders exist
os.makedirs(accepted_folder, exist_ok=True)
os.makedirs(favorited_folder, exist_ok=True)

# Load images
images = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith(('.png', '.jpg', '.jpeg'))]
favorites = []  # List to store paths of favorited images
deleted = []    # List to store paths of deleted images
current_image_index = 0

# Tkinter setup
root = tk.Tk()
root.title("Image Viewer")

# *** Enable fullscreen mode ***
root.attributes("-fullscreen", True)
root.configure(bg="black")  # Set background to black for better viewing

# Image display label
image_label = tk.Label(root, bg="black")  # Set background for the image label
image_label.pack(fill="both", expand=True)

# Update the displayed image
def show_image(index):
    global image_label
    img = Image.open(images[index])
    
    # *** Resize to fit the fullscreen ***
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    
    tk_image = ImageTk.PhotoImage(img)
    image_label.configure(image=tk_image)
    image_label.image = tk_image

# Serial communication setup
ser = serial.Serial(serial_port, baud_rate)

# Command handler
def handle_command(command):
    global current_image_index, favorites, deleted

    if command == "NEXT":
        current_image_index = (current_image_index + 1) % len(images)
    elif command == "PREVIOUS":
        current_image_index = (current_image_index - 1) % len(images)
    elif command == "FAVORITE":
        if images[current_image_index] not in favorites:
            favorites.append(images[current_image_index])
        print(f"Favorited: {images[current_image_index]}")
    elif command == "DELETE":
        if images[current_image_index] not in deleted:
            deleted.append(images[current_image_index])
        print(f"Marked for deletion: {images[current_image_index]}")
    elif command == "ENTER":
        save_images()
        print("Images saved! Exiting.")
        root.quit()

    # Show updated image
    if images:
        show_image(current_image_index)

# Function to save images to folders
def save_images():
    for image_path in images:
        if image_path in deleted:
            continue  # Skip deleted images
        elif image_path in favorites:
            save_image_to_folder(image_path, favorited_folder)
        else:
            save_image_to_folder(image_path, accepted_folder)

# Function to save a single image to a folder
def save_image_to_folder(image_path, folder):
    filename = os.path.basename(image_path)
    destination = os.path.join(folder, filename)
    shutil.copy(image_path, destination)

# Continuously listen for commands
def listen_to_arduino():
    if ser.in_waiting > 0:
        command = ser.readline().decode('utf-8').strip()
        handle_command(command)
    root.after(100, listen_to_arduino)

# Start the application
if images:
    show_image(current_image_index)
    root.after(100, listen_to_arduino)  # Start listening to Arduino
    root.mainloop()
else:
    print("No images found in the folder!")
