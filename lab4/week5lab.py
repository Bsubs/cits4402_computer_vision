# Joo Kai Tay, 22489437, Week 5 Lab

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import cv2

class ImageGUI:
    maxsize=500
   
    def __init__(self, master):
        self.master = master
        self.master.title("Image GUI")

        # Create a frame for the GUI and center it
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True, padx=10, pady=10)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Create a border for the GUI
        self.border = tk.Frame(self.frame, borderwidth=2, relief="groove")
        self.border.grid(row=0, column=0, sticky="nsew")

        # Create a "Load Image" button
        self.load_button = tk.Button(self.border, text="Load Image", command=self.load_image)
        self.load_button.grid(column=0, row=1, padx=5, pady=5)
        # Create a label to display the chosen image
        self.image_label = tk.Label(self.border)
        self.image_label.grid(column=0, row=0, padx=5, pady=5)

        # Create a label to display the filtered image
        self.filtered_label = tk.Label(self.border)
        self.filtered_label.grid(column=3, row=0, padx=5, pady=5)

        # Create detect edge button
        self.detect_edge = tk.Button(self.border, text="Detect Edge")
        self.detect_edge.grid(column=1, row = 1, padx=5, pady=5)

        # Create edge detection drop down menu
        variable = tk.StringVar(self.border)
        variable.set("one") # default value
        self.algo_select = tk.OptionMenu(self.border, variable, "one", "two", "three")
        self.algo_select.grid(column=1, row=2, padx=5, pady=5)

        # Create edge detection slider
        self.edge_detection_slider_label = tk.Label(self.border, text="Threshold for edge detection")
        self.edge_detection_slider_label.grid(column=3, row=1, padx=5, pady=5)
        self.edge_detection_slider = tk.Scale(self.border, from_=0, to=200, orient=tk.HORIZONTAL)
        self.edge_detection_slider.grid(column=3, row=2, padx=5, pady=5)
        



    def load_image(self):
        # Open a file selection dialog box to choose an image file
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

        # Load the chosen image using PIL
        self.original_image = Image.open(file_path)
        grayscale_image = self.original_image.convert('L')
        np_image = np.array(grayscale_image)

        # Convert the equalized image back to PIL format
        pil_image = Image.fromarray(np_image)

        # Resize the image to fit in the label
        width, height = pil_image.size
        max_size = self.maxsize
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        pil_image = pil_image.resize((new_width, new_height))

        # Convert the image to Tkinter format and display it on the left side
        photo = ImageTk.PhotoImage(pil_image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
        
            
if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageGUI(root)
    root.mainloop()
