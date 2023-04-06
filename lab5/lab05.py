# Joo Kai Tay, 22489437, Week 6 Lab05
# Comments and optimal values found in ReadMe.md
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import cv2
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.draw import circle_perimeter

class ImageGUI:
    # Size of the GUI
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

        # Create optimal segmentation button
        self.detect_edge = tk.Button(self.border, text="Optimal Segmentation - Iris", command=self.segment_image_1)
        self.detect_edge.grid(column=3, row = 3, padx=5, pady=5)

        # Create optimal segmentation button
        self.detect_edge = tk.Button(self.border, text="Optimal Segmentation - Peppers", command=self.segment_image_2)
        self.detect_edge.grid(column=3, row = 4, padx=5, pady=5)

        # Create lower threshold slider widget
        self.lower_threshold_slider = tk.Scale(self.border, label='Lower Threshold', from_=0, to=180, orient=tk.HORIZONTAL, length=255, showvalue=0, command=self.segment_image)
        self.lower_threshold_slider.set('0')
        self.lower_threshold_slider.grid(column=3, row=1, padx=5, pady=5) 

        # Create upper threshold slider widget
        self.upper_threshold_slider = tk.Scale(self.border, label='Upper Threshold', from_=0, to=180, orient=tk.HORIZONTAL, length=255, showvalue=1, command=self.segment_image)
        self.upper_threshold_slider.set('108')
        self.upper_threshold_slider.grid(column=3, row=2, padx=5, pady=5) 



    def load_image(self):
        # Open a file selection dialog box to choose an image file
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

        # Load the chosen image using PIL
        self.original_image = Image.open(file_path)
        np_image = np.array(self.original_image)

        # Placeholder for global variable holding the filtered image
        self.filtered_image = 0

        # Convert the image back to PIL format
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


    def segment_image(self, _event=None):

        # retrive the original image
        original_img = np.array(self.original_image)
        # Convert BGR to HSV
        hsv_image = cv2.cvtColor(original_img, cv2.COLOR_BGR2HSV)

        # Get the upper and lower threshold from the slider widgets
        lower = self.lower_threshold_slider.get()
        upper = self.upper_threshold_slider.get()

        lower_hsv = np.array([lower,0,0])
        upper_hsv = np.array([upper,255,255])
        # Threshold the HSV image
        mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)

        pil_image = Image.fromarray(mask)
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
        self.filtered_label.configure(image=photo)
        self.filtered_label.image = photo

    def segment_image_1(self):
        # Sets the lower and upper thresholds to the optimal level for the iris image
        self.lower_threshold_slider.set('0')
        self.upper_threshold_slider.set('81')
        self.segment_image()
    
    def segment_image_2(self):
        # Sets the low and upper thresholds to the optimal level for the peppers image
        self.lower_threshold_slider.set('0')
        self.upper_threshold_slider.set('108')
        self.segment_image()


        
            
if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageGUI(root)
    root.mainloop()
