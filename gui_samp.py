import tkinter as tk
from PIL import Image, ImageTk
import random

# Function to create the main window and display the background image
def create_window_with_background():
    # Create the main window
    root = tk.Tk()
    root.title("Fullscreen Background Image")

    # Set the window to fullscreen
    root.attributes('-fullscreen', True)

    # Create a Canvas widget to draw the background image and shapes
    canvas = tk.Canvas(root, bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)  # Make the canvas fill the entire window

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Load and display the background image
    bg_image = Image.open("agr.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)  # Resize image to fit window
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, anchor='nw', image=bg_photo)

    # Generate a random integer
    random_integer = random.randint(0, 100)

    # Define font and color for the text
    font = ('Pacifico', 30)
    color = 'white'

    # Define padding from the right edge and top edge
    padding_right = 1800
    padding_top = 750

    # Generate random coordinates within the top-right area
    text_x = screen_width - padding_right - 100  # Adjust 100 as needed for text width
    text_y = padding_top + random.randint(0, 50)  # Random vertical position within the padding

    # Display the random integer on the canvas
    canvas.create_text(text_x, text_y, text=str(random_integer), font=font, fill=color, anchor='ne')

    root.mainloop()

# Run the function to create the window
create_window_with_background()
