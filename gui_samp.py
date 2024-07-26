import tkinter as tk
from PIL import Image, ImageTk
import cv2
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import threading

# Configure the Google Generative AI API
genai.configure(api_key="AIzaSyAKi62cSIUc6fVt5XH0MZWN9G3WDkDCuCs")
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 1)

# Check if espeak is available and set properties
if 'espeak' in engine.getProperty('voices')[0].id:
    engine.setProperty('voice', 'en-us')
    engine.setProperty('pitch', 70)

# Function to capture a frame and save it as an image
def capture_frame():
    ret, frame = cap.read()
    if ret:
        image_path = "captured_frame.jpg"
        cv2.imwrite(image_path, frame)
        return image_path
    return None

# Function to upload an image and get the response from the AI model
def identify_object(image_path):
    sample_file = genai.upload_file(path=image_path, display_name="Captured Frame")
    response = model.generate_content([sample_file, "what product is this and where can I buy it"])
    return response.text

# Initialize webcam
esp32_cam_url = "http://192.168.208.229:81/stream"
cap = cv2.VideoCapture(esp32_cam_url)

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to listen for the keyword and capture a frame
def listen_for_keyword():
    with sr.Microphone() as source:
        print("Listening for the keyword 'product'...")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source)
                speech_text = recognizer.recognize_google(audio)
                print("You said: " + speech_text)
                if "product" in speech_text.lower():
                    image_path = capture_frame()
                    if image_path:
                        result = identify_object(image_path)
                        print("Identified Object:", result)
                        sentences = result.split('. ')
                        for sentence in sentences:
                            engine.say(sentence)
                            engine.runAndWait()
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

# Function to create the main window and display the background image
def create_window_with_background():
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

    # Draw a hexagon shape on the left half of the screen
    hexagon_coords = [50, 50, 150, 50, 200, 100, 200, 200, 150, 250, 50, 200]
    canvas.create_polygon(hexagon_coords, fill='white', outline='black')

    root.mainloop()

# Start the GUI in a separate thread
gui_thread = threading.Thread(target=create_window_with_background)
gui_thread.start()

# Start listening for the keyword
listen_for_keyword()

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
