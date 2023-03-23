# Joo Kai Tay, 22489437, Week 4, lab03
# python week4lab.py

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

        # Create a "Histogram Equalize" button
        self.histogram_button = tk.Button(self.border, text="Histogram Equalize", command=self.histogram_equalize)
        self.histogram_button.grid(column=1, row=1, padx=5, pady=5)

        # Create low pass widget
        self.low_pass_frame = tk.Frame(self.border)
        tk.Button(self.low_pass_frame, text="Low Pass", command=self.low_pass_filter).pack(side=tk.LEFT, padx=5, pady=5)
        self.kernel_size_var = tk.Entry(self.low_pass_frame, width=1)
        self.kernel_size_var.insert(0, "3")
        self.kernel_size_var.pack(side=tk.LEFT, padx=5, pady=5)
        self.sigma_var = tk.Entry(self.low_pass_frame, width=1)
        self.sigma_var.insert(0,"2")
        self.sigma_var.pack(side=tk.LEFT, padx=5, pady=5)
        self.low_pass_frame.grid(column=1, row=2, padx=5, pady=5)

        # Create a "High Pass" button
        self.high_pass_button = tk.Button(self.border, text="High Pass", command=self.high_pass_filter)
        self.high_pass_button.grid(column=1, row=3, padx=5, pady=5)

        # Create high boost widget
        self.boost_frame = tk.Frame(self.border)
        tk.Button(self.boost_frame, text="High boost", command=self.high_boost_filter).pack(side=tk.LEFT, padx=5, pady=5)
        self.boost_factor = tk.Entry(self.boost_frame, width=2)
        self.boost_factor.insert(0, "10")
        self.boost_factor.pack(side=tk.LEFT, padx=5, pady=5)
        self.boost_frame.grid(column=3, row=1, padx=5, pady=5)



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
        
    def histogram_equalize(self):
        # Convert the original image to grayscale
        grayscale_image = self.original_image.convert('L')

        # Perform histogram equalization using OpenCV
        np_image = np.array(grayscale_image)
        equalized_image = cv2.equalizeHist(np_image)

        # Convert the equalized image back to PIL format
        pil_image = Image.fromarray(equalized_image)

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

        # Convert the image to Tkinter format and display it on the right side
        photo = ImageTk.PhotoImage(pil_image)
        self.filtered_label.configure(image=photo)
        self.filtered_label.image = photo

    def high_pass_filter(self):
        # Fixed kernel size
        ksize = 3
        # Convert the original image to grayscale
        grayscale_image = self.original_image.convert('L')
    
        # Convert the grayscale image to a numpy array
        np_image = np.array(grayscale_image)

        high_pass = cv2.subtract(np_image,cv2.GaussianBlur(np_image, (3,3), 0))
        high_pass= cv2.add(high_pass, 127)
    
        # Convert the filtered image back to PIL format
        pil_image = Image.fromarray(high_pass)
    
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
    
        # Convert the image to Tkinter format and display it on the right side
        photo = ImageTk.PhotoImage(pil_image)
        self.filtered_label.configure(image=photo)
        self.filtered_label.image = photo
        
        
    def low_pass_filter(self):
        # Get the kernel size and sigma from the scale widgets
        ksize = int(self.kernel_size_var.get())
        sigma = int(self.sigma_var.get())

        # Convert the original image to grayscale
        grayscale_image = self.original_image.convert('L')

        # Convert the grayscale image to a numpy array
        np_image = np.array(grayscale_image)

        # Apply a Gaussian filter to the image
        filtered_image = cv2.GaussianBlur(np_image, (ksize, ksize), sigma)

        # Convert the filtered image back to PIL format
        pil_image = Image.fromarray(filtered_image)

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

        # Convert the image to Tkinter format and display it on the right side
        photo = ImageTk.PhotoImage(pil_image)
        self.filtered_label.configure(image=photo)
        self.filtered_label.image = photo
    
    def high_boost_filter(self):
        # Get the boosting factor from the widget
        bf = int(self.boost_factor.get())

        # Convert the original image to grayscale
        grayscale_image = self.original_image.convert('L')

        # Convert the grayscale image to a numpy array
        np_image = np.array(grayscale_image)

        # Apply high pass filter
        high_pass = cv2.subtract(np_image,cv2.GaussianBlur(np_image, (3,3), 0))
        high_pass= cv2.add(high_pass, 127)
        # Multiply original image by boosting factor
        boosted_img = cv2.multiply((bf-1), np_image)
        # Add high pass and multiplited image
        high_boost = cv2.add(boosted_img, high_pass)

        # Convert the filtered image back to PIL format
        pil_image = Image.fromarray(high_boost)

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

        # Convert the image to Tkinter format and display it on the right side
        photo = ImageTk.PhotoImage(pil_image)
        self.filtered_label.configure(image=photo)
        self.filtered_label.image = photo

            
if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageGUI(root)
    root.mainloop()
